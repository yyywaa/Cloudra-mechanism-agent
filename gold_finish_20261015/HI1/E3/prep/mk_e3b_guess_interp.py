#!/usr/bin/env python3
"""E3b TS-guess frame builder: interpolate the hemiaminal minimum (job 1028 frame)
towards the converged P endpoint (job 1061) and emit frames along C2-N4.

Usage:
  mk_e3b_guess_interp.py REACTANT.xyz PRODUCT.xyz OUTDIR [LABEL]

Checks enforced (abort if any fails):
  * both files: 41 atoms, identical element sequence (same E3 working order)
  * every emitted frame: minsep >= 0.90 A
Reported per frame (never invented): lambda, R(C2-N4), R(C2-O25), R(N4-H26),
R(O25-H26), R(H26...C2), minsep, and monotonicity of R(C2-N4) along the table.
The frames are CONSTRUCTED GUESSES, not saddles and not converged geometries.
"""
import sys, math

def rd_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    at = [[x.split()[0]] + [float(v) for v in x.split()[1:4]] for x in L[2:2+n]]
    return at, n

def d(A, i, j):
    return math.dist(A[i-1][1:], A[j-1][1:])

def minsep(A):
    n = len(A)
    return min((math.dist(A[i][1:], A[j][1:]), i+1, j+1) for i in range(n) for j in range(i+1, n))

def interp(R, P, lam):
    return [[R[i][0]] + [R[i][k] + lam*(P[i][k]-R[i][k]) for k in (1,2,3)] for i in range(len(R))]

def main():
    rp, pp, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else 'e3b'
    R, nR = rd_xyz(rp); P, nP = rd_xyz(pp)
    if nR != nP or nR != 41:
        raise SystemExit('ATOM COUNT mismatch (%d vs %d) -> refuse' % (nR, nP))
    if [a[0] for a in R] != [a[0] for a in P]:
        raise SystemExit('ELEMENT ORDER mismatch -> refuse (working order must match)')
    print('both endpoints: 41 atoms, identical element order: True')
    print('reactant  R(C2-N4)=%.4f R(C2-O25)=%.4f R(N4-H26)=%.4f R(O25-H26)=%.4f' % (d(R,2,4), d(R,2,25), d(R,4,26), d(R,25,26)))
    print('product   R(C2-N4)=%.4f R(C2-O25)=%.4f R(N4-H26)=%.4f R(O25-H26)=%.4f' % (d(P,2,4), d(P,2,25), d(P,4,26), d(P,25,26)))
    rows = []
    import os
    os.makedirs(outdir, exist_ok=True)
    for k in range(1, 10):
        lam = k/10.0
        A = interp(R, P, lam)
        ms, mi, mj = minsep(A)
        if ms < 0.9:
            print('lam=%.1f REJECTED minsep %.4f (%d-%d)' % (lam, ms, mi, mj))
            continue
        rows.append((lam, d(A,2,4), d(A,2,25), d(A,4,26), d(A,25,26), d(A,26,2), ms, mi, mj, A))
    print('\n lam   R(C2-N4) R(C2-O25) R(N4-H26) R(O25-H26) R(H26..C2) minsep  pair')
    prev = None; mono = True
    for lam, r24, r225, r426, r2526, r26c2, ms, mi, mj, A in rows:
        print('%4.1f  %8.4f %9.4f %9.4f %10.4f %10.4f %7.4f  %d-%d' % (lam, r24, r225, r426, r2526, r26c2, ms, mi, mj))
        if prev is not None and r24 < prev - 1e-9:
            mono = False
        prev = r24
    print('\nR(C2-N4) monotone increasing along frames: %s' % mono)
    rec = [r for r in rows if 2.15 <= r[1] <= 2.45 and r[3] < 1.35 and r[2] < 1.32]
    if rec:
        lam = rec[0][0]
        print('recommended frame: lam=%.1f (R(C2-N4)=%.4f, R(N4-H26)=%.4f, R(C2-O25)=%.4f)' % (lam, rec[0][1], rec[0][3], rec[0][2]))
    else:
        lam = None
        print('no frame satisfied the recommendation window; inspect the table above')
    for lam2, r24, r225, r426, r2526, r26c2, ms, mi, mj, A in rows:
        name = '%s/%s_lam%02d_c2n4_%.2f.xyz' % (outdir, label, round(lam2*10), r24)
        with open(name, 'w') as f:
            f.write('%d\n%s interpolation lam=%.2f R(C2-N4)=%.4f (constructed guess, not a saddle)\n' % (len(A), label, lam2, r24))
            for a in A:
                f.write('%s %.8f %.8f %.8f\n' % (a[0], a[1], a[2], a[3]))
    print('frames written to %s' % outdir)

if __name__ == '__main__':
    main()
