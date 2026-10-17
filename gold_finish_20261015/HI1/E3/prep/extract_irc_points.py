#!/usr/bin/env python3
"""Extract the IRC point geometries from a Gaussian irc log.

Each computed IRC point is preceded by a line "Point Number: N   Path Number: M" and
followed by an "Input orientation:" block (41 atoms for this system). Frames are written
as xyz files named irc_point_p<M>_<N>.xyz in OUTDIR, in input atom order.

Usage: extract_irc_points.py irc.log OUTDIR
"""
import sys, os, re

def main():
    log, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    L = open(log, errors='replace').read().splitlines()
    cur = None
    written = []
    for i, line in enumerate(L):
        m = re.match(r'\s*Point Number:\s*(\d+)\s+Path Number:\s*(\d+)', line)
        if m:
            cur = (int(m.group(2)), int(m.group(1)))
            continue
        if cur and line.strip().startswith('Input orientation:'):
            # header lines: ----, Center Atomic Atomic Coordinates, ----, then atoms
            j = i + 1
            atoms = []
            while j < len(L):
                p = L[j].split()
                if len(p) == 6 and p[0].isdigit() and p[1].isdigit():
                    atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
                elif atoms and (not p or L[j].strip().startswith('-----')):
                    break
                j += 1
            sym = {1: 'H', 6: 'C', 7: 'N', 8: 'O'}
            path, pt = cur
            fn = os.path.join(outdir, 'irc_point_p%d_%02d.xyz' % (path, pt))
            with open(fn, 'w') as f:
                f.write('%d\nIRC point path %d point %d\n' % (len(atoms), path, pt))
                for z, x, y, zz in atoms:
                    f.write('%s %.8f %.8f %.8f\n' % (sym.get(z, 'X'), x, y, zz))
            written.append((fn, len(atoms), path, pt))
            cur = None
    for fn, n, path, pt in written:
        print('%s  atoms=%d  path=%d point=%d' % (fn, n, path, pt))
    if not written:
        raise SystemExit('no IRC point frames found')

if __name__ == '__main__':
    main()
