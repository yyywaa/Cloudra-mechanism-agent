#!/usr/bin/env python3
"""Build the (r2,c4) target frame from the pt14=(r2,c3) converged frame.

Only ONE atom moves: H26 (index 26, 1-based) is translated along the
O25 -> H26 direction so that R(25,26) becomes exactly 1.7193 A.
All other 40 atoms are copied unchanged.

Tool-gap note: internal_coordinates mode=transform rejects
{"type":"stretch","atoms":[25,26]} for this frame because O25-H26 = 1.4693 A
is not bond-perceived (it is a shared/mid-transfer proton), so the rigid
one-atom translation is done here and then re-verified with
internal_coordinates (analyze + watch_pairs) and by direct distance checks.

usage: python build_r2c4_target.py <seed.xyz> <out.xyz> <target_R25_26>
"""
import sys, math

def read_xyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0].split()[0])
    at = []
    for ln in lines[2:2+n]:
        f = ln.split()
        at.append([f[0], float(f[1]), float(f[2]), float(f[3])])
    assert len(at) == n, (len(at), n)
    return at

def d(at, i, j):
    a, b = at[i-1], at[j-1]
    return math.sqrt((a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2)

def main():
    seed, out, target = sys.argv[1], sys.argv[2], float(sys.argv[3])
    at = read_xyz(seed)
    print('atoms', len(at))
    print('BEFORE R(2,4)   %.4f' % d(at,2,4))
    print('BEFORE R(25,26) %.4f' % d(at,25,26))
    print('BEFORE R(10,27) %.4f' % d(at,10,27))
    o, h = at[24], at[25]           # O25 = index 25, H26 = index 26 (1-based)
    v = [h[k]-o[k] for k in (1,2,3)]
    n = math.sqrt(sum(x*x for x in v))
    u = [x/n for x in v]
    delta = target - n
    for k in (1,2,3):
        h[k] += u[k-1]*delta
    print('moved atom 26 (H) by %.6f A along O25->H26 unit vector' % delta)
    print('unit vector %12.8f %12.8f %12.8f' % tuple(u))
    print('AFTER  R(2,4)   %.4f' % d(at,2,4))
    print('AFTER  R(25,26) %.4f' % d(at,25,26))
    print('AFTER  R(10,27) %.4f' % d(at,10,27))
    print('AFTER  R(2,25)  %.4f' % d(at,2,25))
    print('AFTER  R(2,26)  %.4f' % d(at,2,26))
    print('AFTER  R(4,26)  %.4f' % d(at,4,26))
    # closest heavy atom to H26
    heavy = [(i+1, a[0], d(at, i+1, 26)) for i, a in enumerate(at) if a[0] != 'H']
    heavy.sort(key=lambda x: x[2])
    print('nearest heavy atoms to H26:', [(e, '%.4f' % dd) for _, e, dd in heavy[:3]])
    with open(out, 'w') as fh:
        fh.write('%d\n' % len(at))
        fh.write('job1074 scan#14 (r2,c3)=pt14 seed -> target (r2,c4): R(2,4)=1.6248 kept, R(25,26)=%.4f\n' % target)
        for e, x, y, z in at:
            fh.write('%-3s %14.8f %14.8f %14.8f\n' % (e, x, y, z))
    print('wrote', out)

main()
