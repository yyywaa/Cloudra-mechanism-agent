#!/usr/bin/env python3
"""Extract the (r2,c3)=pt14 final converged frame from job 1074's native log,
report key internal coordinates, and write an xyz for downstream seeded work.

Read-only w.r.t. the native log. Nothing is hand-written: coordinates are parsed
from Gaussian's 'Input orientation' table (input atom order).

usage: python extract_frame_r2c4.py <log> <table_header_lineno> <out.xyz>
"""
import sys, math

ELEM = {1:'H',6:'C',7:'N',8:'O'}

def read_table(path, header_lineno):
    lines = open(path, 'r', errors='replace').read().splitlines()
    i = header_lineno - 1
    assert 'Input orientation' in lines[i], lines[i]
    # skip 4 header lines then dashed separator, then atoms
    j = i + 1
    atoms = []
    while j < len(lines):
        f = lines[j].split()
        if len(f) == 6 and f[0].isdigit() and f[1].isdigit():
            atoms.append((int(f[1]), float(f[3]), float(f[4]), float(f[5])))
        elif atoms and lines[j].strip().startswith('-----'):
            break
        j += 1
    return atoms

def dist(a, b):
    return math.sqrt(sum((a[k]-b[k])**2 for k in (1,2,3)))

def main():
    log, hdr, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    at = read_table(log, hdr)
    print('n_atoms', len(at))
    print('elements', ''.join(ELEM.get(z, 'X') for z, *_ in at))
    def d(i, j):
        return dist(at[i-1], at[j-1])
    print('R(2,4)  %.4f' % d(2,4))
    print('R(25,26) %.4f' % d(25,26))
    print('R(10,27) %.4f' % d(10,27))
    print('R(2,25) %.4f' % d(2,25))
    print('R(2,26) %.4f' % d(2,26))
    print('R(4,26) %.4f' % d(4,26))
    with open(out, 'w') as fh:
        fh.write('%d\n' % len(at))
        fh.write('job1074 scan#14 (r2,c3)=pt14 final converged frame, parsed from Input orientation L%d\n' % hdr)
        for z, x, y, zz in at:
            fh.write('%-3s %14.8f %14.8f %14.8f\n' % (ELEM.get(z, 'X'), x, y, zz))
    print('wrote', out)

main()
