#!/usr/bin/env python3
"""E3b TS-guess frame builder (v2): heavy-atom Cartesian interpolation between the
hemiaminal minimum (job 1028 frame) and the converged P endpoint (job 1061), with the
transferred proton H26 carried ON N4 (N4-H26 = 1.05 A, pointing along the N4->O25 line)
instead of being linearly dragged through the C2/O25 region.

Why v2: plain Cartesian interpolation of H26 is unusable for E3b -- the straight line
from O25 to N4 passes through the ketone carbon region and produced minsep 0.38-0.67 A
(see prep/e3b_guess_dryrun notes). v2 interpolates the heavy skeleton, then places the
proton where it must be at a late, proton-transferred saddle candidate.

Usage:
  mk_e3b_guess_interp_v2.py REACTANT.xyz PRODUCT.xyz OUTDIR [LABEL]

Checks enforced (abort if violated):
  * both endpoints: 41 atoms and identical element sequence (E3 working order)
  * every emitted frame: minsep >= 0.90 A
Per-frame table reports lambda, R(C2-N4), R(C2-O25), R(N4-H26), R(O25-H26),
R(H26...C2), R(N4...O25), minsep and the offending pair; monotonicity of R(C2-N4)
and R(C2-O25) along the table is printed. Frames are CONSTRUCTED GUESSES: not
saddles, not converged geometries, no energies implied.
"""
import sys, os, math

def rd_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [[x.split()[0]] + [float(v) for v in x.split()[1:4]] for x in L[2:2+n]], n

def d(A, i, j):
    return math.dist(A[i-1][1:], A[j-1][1:])

def minsep(A):
    n = len(A)
    return min((math.dist(A[i][1:], A[j][1:]), i+1, j+1) for i in range(n) for j in range(i+1, n))

def interp(R, P, lam):
    return [[R[i][0]] + [R[i][k] + lam*(P[i][k]-R[i][k]) for k in (1,2,3)] for i in range(len(R))]

def put_proton_on_N(A, n_hn=1.05):
    """H26 (working atom 26) placed on N4 (atom 4) pointing toward O25 (atom 25)."""
    N4, O25, H26 = A[3], A[24], A[25]
    u = [O25[k]-N4[k] for k in (1,2,3)]
    m = math.dist([0,0,0], u); u = [x/m for x in u]
    H26[1] = N4[1] + n_hn*u[0]; H26[2] = N4[2] + n_hn*u[1]; H26[3] = N4[3] + n_hn*u[2]
    return A

def main():
    rp, pp, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    R, nR = rd_xyz(rp); P, nP = rd_xyz(pp)
    if nR != 41 or nP != 41:
        raise SystemExit('ATOM COUNT mismatch (%d vs %d) -> refuse' % (nR, nP))
    if [a[0] for a in R] != [a[0] for a in P]:
        raise SystemExit('ELEMENT ORDER mismatch -> refuse (same E3 working order required)')
    print('endpoints: 41 atoms each, identical element order: True')
    for tag, A in (('reactant(1028)', R), ('product(1061)', P)):
        print('%-15s R(C2-N4)=%.4f R(C2-O25)=%.4f R(N4-H26)=%.4f R(O25-H26)=%.4f' % (tag, d(A,2,4), d(A,2,25), d(A,4,26), d(A,25,26)))
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for k in range(1, 20):
        lam = k/20.0
        A = put_proton_on_N(interp(R, P, lam))
        ms, mi, mj = minsep(A)
        rows.append((lam, d(A,2,4), d(A,2,25), d(A,4,26), d(A,25,26), d(A,26,2), d(A,4,25), ms, mi, mj, A))
    print('\n lam  R(C2-N4) R(C2-O25) R(N4-H26) R(O25-H26) R(H26..C2) R(N4..O25) minsep  pair  ok')
    ok_rows = []
    for lam, r24, r225, r426, r2526, r26c2, r425, ms, mi, mj, A in rows:
        ok = ms >= 0.9
        print('%4.2f %9.4f %9.4f %9.4f %10.4f %10.4f %10.4f %7.4f  %d-%d %s' % (lam, r24, r225, r426, r2526, r26c2, r425, ms, mi, mj, 'PASS' if ok else 'FAIL'))
        if ok: ok_rows.append((lam, r24, r225, A))
    if len(ok_rows) >= 2:
        mono24 = all(ok_rows[i+1][1] > ok_rows[i][1] for i in range(len(ok_rows)-1))
        mono225 = all(ok_rows[i+1][2] < ok_rows[i][2] for i in range(len(ok_rows)-1))
        print('\nmonotone R(C2-N4) increasing: %s ; monotine R(C2-O25) decreasing: %s' % (mono24, mono225))
    rec = [r for r in ok_rows if 2.15 <= r[1] <= 2.45 and r[2] <= 1.32]
    if rec:
        lam, r24, r225, _ = rec[0]
        print('recommended: lam=%.2f  R(C2-N4)=%.4f  R(C2-O25)=%.4f' % (lam, r24, r225))
    else:
        print('no PASS frame inside R(C2-N4) 2.15-2.45 with R(C2-O25)<=1.32 -- inspect table')
    for lam, r24, r225, A in ok_rows:
        name = '%s/%s_lam%02d_c2n4_%.2f.xyz' % (outdir, label, round(lam*20), r24)
        with open(name, 'w') as f:
            f.write('%d\n%s constructed interpolation lam=%.2f R(C2-N4)=%.4f, H26 on N4 1.05 A (guess, not a saddle)\n' % (len(A), label, lam, r24))
            for a in A:
                f.write('%s %.8f %.8f %.8f\n' % (a[0], a[1], a[2], a[3]))
    print('frames written to %s' % outdir)

if __name__ == '__main__':
    main()
