#!/usr/bin/env python3
"""Derive a reduced (truncated+cap) model geometry from an existing computed structure.

Provenance-preserving: coordinates are taken verbatim from an existing Gaussian
log / xyz (no hand-typed values); only the requested atoms are deleted and one
capping H is placed along a declared bond vector.

Usage:
  python3 mk_reduced_model.py --xyz IN.xyz --delete 24,28,... --cap 1,29,1.09 --out OUT.xyz
  python3 mk_reduced_model.py --log job.log --delete ... --cap ... --out ...
"""
import argparse, hashlib, math, re, sys
from collections import Counter

PT = {1: 'H', 2: 'He', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 15: 'P', 16: 'S', 17: 'Cl'}


def read_xyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0].split()[0])
    at, xyz = [], []
    for ln in lines[2:2 + n]:
        p = ln.split()
        at.append(p[0]); xyz.append([float(p[1]), float(p[2]), float(p[3])])
    return at, xyz


def read_log_last_frame(path):
    L = open(path).read().splitlines()
    idx = [i for i, l in enumerate(L) if 'Standard orientation' in l]
    if not idx:
        sys.exit('no Standard orientation in log')
    start = idx[-1]
    at, xyz, i = [], [], start
    while i < len(L) and len(at) < 400:
        m = re.match(r'\s+(\d+)\s+(\d+)\s+(-?\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)', L[i])
        if m:
            at.append(int(m.group(2))); xyz.append([float(m.group(4)), float(m.group(5)), float(m.group(6))])
        elif at:
            break
        i += 1
    return at, xyz, idx[-1] + 1


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--xyz'); g.add_argument('--log')
    ap.add_argument('--delete', required=True)
    ap.add_argument('--cap', default='')
    ap.add_argument('--out', required=True)
    ap.add_argument('--note', default='')
    a = ap.parse_args()

    if a.xyz:
        at, xyz = read_xyz(a.xyz); src = 'xyz ' + a.xyz
    else:
        z, xyz, ln = read_log_last_frame(a.log)
        at = [PT.get(v, str(v)) for v in z]; src = 'log %s Standard orientation line %d' % (a.log, ln)

    dele = sorted({int(x) for x in a.delete.split(',') if x.strip()})
    keep = [i for i in range(1, len(at) + 1) if i not in dele]
    newat = [at[i - 1] for i in keep]
    newxyz = [xyz[i - 1][:] for i in keep]

    capinfo = ''
    if a.cap:
        anc, dr, bl = [float(x) if '.' in x else int(x) for x in a.cap.split(',')]
        pa, pd = xyz[int(anc) - 1], xyz[int(dr) - 1]
        v = [pd[k] - pa[k] for k in range(3)]
        nrm = math.sqrt(sum(x * x for x in v)); v = [x / nrm for x in v]
        newat.append('H')
        newxyz.append([pa[k] + bl * v[k] for k in range(3)])
        capinfo = 'capped atom %d along %d->%d at %.3f A' % (int(anc), int(anc), int(dr), bl)

    with open(a.out, 'w') as f:
        f.write('%d\n' % len(newat))
        f.write('reduced from %s ; deleted %s ; %s ; %s\n' % (src, dele, capinfo, a.note))
        for e, p in zip(newat, newxyz):
            f.write('%-2s %14.8f %14.8f %14.8f\n' % (e, p[0], p[1], p[2]))

    c = Counter(newat)
    formula = ''.join('%s%d' % (k, c[k]) for k in ['C', 'H', 'N', 'O'] if c.get(k))
    print('in atoms %d -> out atoms %d' % (len(at), len(newat)))
    print('formula', formula)
    print('kept original indices', keep)
    print('out', a.out, 'sha256', sha(a.out))
    print('source', src, 'sha256', sha(a.xyz if a.xyz else a.log))


if __name__ == '__main__':
    main()
