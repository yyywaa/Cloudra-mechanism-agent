#!/usr/bin/env python3
"""E3b TS-guess frame builder (v4 = approved v3 interpolation logic + formal-frame selection).

v3 logic (approved by the main coordinator): interpolate the heavy skeleton linearly between
the hemiaminal minimum (job 1028 frame) and the converged P endpoint (job 1061), and carry the
transferred proton H26 ON N4 (N4-H26 = 1.05 A) pointing away from the ketone carbon (direction
unit(N4 - C2)). The two rejected constructions are documented in the selection report.

v4 adds the selection rule requested by the coordinator:
  * report the full table for lambda = 0.50 ... 0.80
  * formal frame = the frame in lambda 0.55-0.65 whose R(C2-N4) lies inside 2.15-2.25 A,
    choosing the LARGEST minsep; ties break toward the LOWER R(C2-N4) (low end of the window,
    so a ts_opt is less likely to slide straight to the product side)
  * if nothing lies inside 2.15-2.25 A, fall back to the frame in 0.55-0.65 closest to 2.20 A
    and say so explicitly in the report
  * every emitted frame must satisfy minsep >= 0.90 A; both endpoints must be 41 atoms in the
    identical element sequence (E3 working order), otherwise the script refuses

Frames are CONSTRUCTED GUESSES: not saddles, not converged geometries, no energies implied.
Usage: mk_e3b_guess_interp_v4.py REACTANT.xyz PRODUCT.xyz OUTDIR LABEL
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
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for k in range(1, 100):
        lam = k/100.0
        A = put_proton_on_N(interp(R, P, lam))
        ms, mi, mj = minsep(A)
        rows.append(dict(lam=lam, r24=d(A,2,4), r225=d(A,2,25), r426=d(A,4,26),
                         r2526=d(A,25,26), r26c2=d(A,26,2), ms=ms, mi=mi, mj=mj, A=A))
    ok = [r for r in rows if r['ms'] >= 0.90]
    win = [r for r in ok if 0.55 <= r['lam'] <= 0.65]
    cand = [r for r in win if 2.15 <= r['r24'] <= 2.25]
    if cand:
        best = sorted(cand, key=lambda r: (-round(r['ms'], 6), r['r24']))[0]
        rule = 'in-window largest minsep, tie -> lower R(C2-N4)'
    elif win:
        best = sorted(win, key=lambda r: abs(r['r24'] - 2.20))[0]
        rule = 'FALLBACK: no frame inside 2.15-2.25 A; nearest to 2.20 A'
    else:
        raise SystemExit('no acceptable frame in lambda 0.55-0.65')
    rep = []
    rep.append('# E3b TS guess - selection report (%s)\n\n' % label)
    rep.append('Endpoints: reactant "%s" (job 1028 minimum frame); product "%s".\n\n' % (rp, pp))
    rep.append('Both endpoints are 41 atoms with an identical element sequence (E3 working order): checked by this script.\n')
    rep.append('\n## Interpolation logic (v3, approved)\n\n')
    rep.append('Heavy skeleton interpolated linearly; H26 (the proton that leaves O25) is carried on N4 at 1.05 A,\n')
    rep.append('direction unit(N4 - C2), i.e. pointing away from the ketone carbon.\n')
    rep.append('\n## Rejected constructions (measured, reproducible with the archived scripts)\n\n')
    rep.append('* v1 (plain all-atom Cartesian interpolation, script prep/mk_e3b_guess_interp.py): H26 is dragged\n')
    rep.append('  straight from O25 to N4 and that line passes the ketone carbon; minsep falls to\n')
    rep.append('  **0.3819-0.6654 A** for lambda 0.1-0.4 (pairs 25-26 and 2-26), violating the 0.90 A gate.\n')
    rep.append('* v2 (H26 on the N4->O25 chord at 1.05 A, script prep/mk_e3b_guess_interp_v2.py): at C2 the chord\n')
    rep.append('  passes about 1.05 A away (law of cosines, sides 2.25/1.31 with N4...O25 2.91), giving a spurious\n')
    rep.append('  H26...C2 contact of about **1.38 A**; rejected.\n')
    rep.append('* Those readings are recorded in gold_finish_20261015/HI1/E3/STATUS.md section P.18 and are reproducible\n')
    rep.append('  by rerunning the two scripts; their scratch frame directories were removed.\n')
    rep.append('\n## Table, lambda = 0.50 - 0.80\n\n')
    rep.append('| lambda | R(C2-N4) | R(C2-O25) | R(N4-H26) | R(O25-H26) | R(H26...C2) | minsep | pair | gate |\n')
    rep.append('|---|---|---|---|---|---|---|---|---|\n')
    for r in rows:
        if 0.50 <= r['lam'] <= 0.80:
            rep.append('| %.2f | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f | %d-%d | %s |\n' % (
                r['lam'], r['r24'], r['r225'], r['r426'], r['r2526'], r['r26c2'], r['ms'], r['mi'], r['mj'],
                'PASS' if r['ms'] >= 0.90 else 'FAIL'))
    rep.append('\nMonotonicity over all gate-passing frames: R(C2-N4) increasing = %s ; R(C2-O25) decreasing = %s.\n' % (
        all(ok[i+1]['r24'] > ok[i]['r24'] for i in range(len(ok)-1)),
        all(ok[i+1]['r225'] < ok[i]['r225'] for i in range(len(ok)-1))))
    rep.append('\n## Selected formal guess\n\n')
    rep.append('* lambda = %.2f (rule: %s)\n' % (best['lam'], rule))
    rep.append('* R(C2-N4) = %.4f A, R(C2-O25) = %.4f A, R(N4-H26) = %.4f A, R(O25-H26) = %.4f A\n' % (
        best['r24'], best['r225'], best['r426'], best['r2526']))
    rep.append('* R(H26...C2) = %.4f A, minsep = %.4f A (pair %d-%d)\n' % (best['r26c2'], best['ms'], best['mi'], best['mj']))
    rep.append('\n## Semantics and limits\n\n')
    rep.append('* This is a **late-corner guess with the proton already on N4**: not a saddle, not a converged geometry.\n')
    rep.append('* Frames with lambda < 0.5 are not physical (the proton would have to jump; O25-H26 goes from ~0.97 to ~3.8 A)\n')
    rep.append('  and are never reported as candidates.\n')
    rep.append('* No energy in this file may be used as a barrier: the E3b barrier stays null until a TS frequency with the\n')
    rep.append('  intended imaginary mode, two frequency-verified endpoints and connectivity are available.\n')
    A = best['A']
    xyz = '%s/E3B_TS_GUESS_lam%03d_c2n4_%.3f.xyz' % (outdir, round(best['lam']*100), best['r24'])
    with open(xyz, 'w') as f:
        f.write('%d\n%s E3b TS guess (constructed, lam=%.2f R(C2-N4)=%.4f, H26 on N4 1.05 A away from C2; NOT a saddle)\n' % (len(A), label, best['lam'], best['r24']))
        for a in A: f.write('%s %.8f %.8f %.8f\n' % (a[0], a[1], a[2], a[3]))
    rp_out = '%s/GUESS_SELECTION_%s.md' % (outdir, label)
    open(rp_out, 'w').writelines(rep)
    print(''.join(rep))
    print('WROTE %s' % xyz)
    print('WROTE %s' % rp_out)

if __name__ == '__main__':
    main()
