#!/usr/bin/env python3
"""Parse a Gaussian scan/opt log: per frame geometry distances + preceding SCF Done.
Usage: parse_gauss_frames.py <log> [--points]
Indices are 1-based; defaults to NR1 E1 system (1=water O, 4=transfer H, 6=C, 8=receiving O)."""
import sys, math, re

def parse(path):
    L = open(path, errors='ignore').read().split('\n')
    frames = []   # (energies before, element list, coords)
    cur_e = None
    i = 0
    last_e = None
    out = []
    while i < len(L):
        line = L[i]
        m = re.match(r'\s*SCF Done:\s+E\(\S+\)\s+=\s+(-?\d+\.\d+)', line)
        if m:
            last_e = float(m.group(1))
        if 'orientation:' in line:
            j = i + 5
            el, co = [], []
            while j < len(L) and '-----' not in L[j]:
                p = L[j].split()
                if len(p) >= 6:
                    try:
                        el.append(int(p[1])); co.append((float(p[3]), float(p[4]), float(p[5])))
                    except ValueError:
                        pass
                j += 1
            out.append((last_e, el, co, L[max(0,i-40):i+1]))
            i = j
        else:
            i += 1
    return out, L

def d(a, b):
    return math.dist(a, b)

if __name__ == '__main__':
    path = sys.argv[1]
    frames, L = parse(path)
    print('file:', path, 'n_frames:', len(frames), 'n_lines:', len(L))
    do_points = '--points' in sys.argv
    for k, (e, el, co, ctx) in enumerate(frames):
        if len(co) < 8:
            print('fr%03d  (incomplete frame, natoms=%d)' % (k, len(co)))
            continue
        # last "Optimization completed." line number before this frame
        lc = None
        for n in range(len(ctx)-1, -1, -1):
            if 'Optimization completed' in ctx[n] or 'Stationary point found' in ctx[n]:
                lc = 'yes'
                break
        if do_points and lc is None:
            continue
        print('fr%03d E=%-16s d(O1-H4)=%.4f d(H4-O8)=%.4f d(O1-O8)=%.4f d(C6-O8)=%.4f%s'
              % (k, ('%.9f' % e) if e else 'None', d(co[0], co[3]), d(co[3], co[7]), d(co[0], co[7]), d(co[5], co[7]),
                 '  <-- after Optimization completed' if lc else ''))
