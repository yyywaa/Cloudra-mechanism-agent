#!/usr/bin/env python3
"""E3b TS-guess frame builder (v3): heavy-atom Cartesian interpolation between the
hemiaminal minimum (job 1028 frame) and the converged P endpoint (job 1061), with the
transferred proton H26 carried ON N4 at 1.05 A, pointing AWAY from the ketone carbon
(direction = unit(N4 - C2)).

Why not v1: plain Cartesian interpolation dragged H26 straight from O25 to N4; the line
passes ~0.9 A from the ketone carbon, giving minsep 0.38-0.67 A (unusable).
Why not v2: placing H26 along unit(O25 - N4) puts it on the N4...O25 chord, which passes
~1.05 A from C2 (law of cosines at C2: sides 2.25/1.31 with N4...O25 2.91 => H26...C2 about
1.38 A) -- a spurious C-H-like contact.
v3 orients the N-H away from the carbonyl carbon instead, which is the physically sensible
orientation for a late, proton-transferred corner and keeps every frame clash-free.

Usage: mk_e3b_guess_interp_v3.py REACTANT.xyz PRODUCT.xyz OUTDIR [LABEL]
Aborts unless both endpoints have 41 atoms in the identical element sequence (E3 working
order). Every emitted frame must satisfy minsep >= 0.90 A. Frames are CONSTRUCTED GUESSES:
not saddles, not converged geometries, and no energies are implied.
"""
import sys, os, math

def rd_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [[x.split()[0]] + [float(v) for v in x.split()[1:4]] for x in L[2:2+n]], n

def d(A, i, j): return math.dist(A[i-1][1:], A[j-1][1:])

def minsep(A):
    n = len(A)
    return min((math.dist(A[i][1:], A[j][1:]), i+1, j+1) for i in range(n) for j in range(i+1, n))

def interp(R, P, lam):
    return [[R[i][0]] + [R[i][k] + lam*(P[i][k]-R[i][k]) for k in (1,2,3)] for i in range(len(R))]

def put_proton_on_N(A, n_hn=1.05):
    """H26 (atom 26) on N4 (atom 4), direction away from the ketone carbon C2 (atom 2)."""
    N4, C2, H26 = A[3], A[1], A[25]
    u = [N4[k]-C2[k] for k in (1,2,3)]
    m = math.dist([0,0,0], u); u = [x/m for x in u]
    H26[1] = N4[1] + n_hn*u[0]; H26[2] = N4[2] + n_hn*u[1]; H26[3] = N4[3] + n_hn*u[2]
    return A

def main():
    rp, pp, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    R, nR = rd_xyz(rp); P, nP = rd_xyz(pp)
    if nR != 41 or nP != 41: raise SystemExit('ATOM COUNT mismatch (%d vs %d)' % (nR, nP))
    if [a[0] for a in R] != [a[0] for a in P]: raise SystemExit('ELEMENT ORDER mismatch -> refuse')
    print('endpoints: 41 atoms each, identical element order: True')
    for tag, A in (('reactant(1028)', R), ('product(1061)', P)):
        print('%-15s R(C2-N4)=%.4f R(C2-O25)=%.4f R(N4-H26)=%.4f R(O25-H26)=%.4f' % (tag, d(A,2,4), d(A,2,25), d(A,4,26), d(A,25,26)))
    os.makedirs(outdir, exist_ok=True)
    ok_rows = []
    print('\n lam  R(C2-N4) R(C2-O25) R(N4-H26) R(O25-H26) R(H26..C2) R(H26..O25) minsep  pair  ok')
    for k in range(1, 20):
        lam = k/20.0
        A = put_proton_on_N(interp(R, P, lam))
        ms, mi, mj = minsep(A)
        row = (lam, d(A,2,4), d(A,2,25), d(A,4,26), d(A,25,26), d(A,26,2), d(A,26,25), ms, mi, mj, A)
        ok = ms >= 0.90
        print('%4.2f %9.4f %9.4f %9.4f %10.4f %10.4f %11.4f %7.4f  %d-%d %s' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], 'PASS' if ok else 'FAIL'))
        if ok: ok_rows.append(row)
    if len(ok_rows) >= 2:
        print('\nmonotone R(C2-N4) increasing: %s ; monotone R(C2-O25) decreasing: %s' % (
            all(ok_rows[i+1][1] > ok_rows[i][1] for i in range(len(ok_rows)-1)),
            all(ok_rows[i+1][2] < ok_rows[i][2] for i in range(len(ok_rows)-1))))
    rec = [r for r in ok_rows if 2.15 <= r[1] <= 2.45 and r[2] <= 1.32]
    if rec:
        print('recommended: lam=%.2f  R(C2-N4)=%.4f  R(C2-O25)=%.4f  R(N4-H26)=%.4f  minsep=%.4f' % (rec[0][0], rec[0][1], rec[0][2], rec[0][3], rec[0][7]))
    else:
        print('no PASS frame inside R(C2-N4) 2.15-2.45 with R(C2-O25)<=1.32')
    if ok_rows:
        lam, r24 = ok_rows[0][0], ok_rows[0][1]
        print('usable window: lam %.2f-%.2f  (R(C2-N4) %.4f-%.4f)' % (ok_rows[0][0], ok_rows[-1][0], ok_rows[0][1], ok_rows[-1][1]))
    for row in ok_rows:
        lam, r24, _, _, _, _, _, _, _, _, A = row
        name = '%s/%s_lam%02d_c2n4_%.2f.xyz' % (outdir, label, round(lam*20), r24)
        with open(name, 'w') as f:
            f.write('%d\n%s constructed interpolation lam=%.2f R(C2-N4)=%.4f, H26 on N4 1.05 A away from C2 (guess, not a saddle)\n' % (len(A), label, lam, r24))
            for a in A: f.write('%s %.8f %.8f %.8f\n' % (a[0], a[1], a[2], a[3]))
    print('frames written to %s' % outdir)

if __name__ == '__main__':
    main()
