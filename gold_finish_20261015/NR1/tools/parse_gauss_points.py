#!/usr/bin/env python3
"""Point-wise parse of a Gaussian relaxed scan log.
A scan point ends at each 'Optimization completed.' line: its energy is the last
'SCF Done' before that line, its geometry the last orientation block before it.
Usage: parse_gauss_points.py <log> [--all]"""
import sys, math, re

def load(path):
    return open(path, errors='ignore').read().split('\n')

def orientations(L):
    res = []
    i = 0
    while i < len(L):
        if 'orientation:' in L[i]:
            j = i + 5; el = []; co = []
            while j < len(L) and '-----' not in L[j]:
                p = L[j].split()
                if len(p) >= 6:
                    try:
                        el.append(int(p[1])); co.append((float(p[3]), float(p[4]), float(p[5])))
                    except ValueError:
                        pass
                j += 1
            res.append((i + 1, el, co)); i = j
        else:
            i += 1
    return res

def d(a, b): return math.dist(a, b)

path = sys.argv[1]; L = load(path)
sopt = [(n + 1, l) for n, l in enumerate(L) if 'Optimization completed' in l]
sscf = [(n + 1, float(re.search(r'=\s+(-?\d+\.\d+)', l).group(1))) for n, l in enumerate(L)
        if re.match(r'\s*SCF Done:', l)]
ori = orientations(L)
print('file:', path)
print('n_lines=%d  n_SCF=%d  n_opt_completed=%d  n_orientation=%d' % (len(L), len(sscf), len(sopt), len(ori)))
print('opt_completed lines:', [n for n, _ in sopt])
print('orientation lines:', [n for n, _, _ in ori])
cur = 0
prev = None
for k, (nopt, _) in enumerate(sopt):
    e = [ev for ln, ev in sscf if ln < nopt]
    g = [o for o in ori if o[0] < nopt]
    if not e or not g:
        print('pt%02d (no energy/geom before line %d)' % (k + 1, nopt)); continue
    ev = e[-1]; ln, el, co = g[-1]
    de = '' if prev is None else ' dE_from_prev=%+7.2f kcal' % ((ev - prev) * 627.509474)
    line = 'pt%02d E=%.9f (SCF line %d, geom line %d, opt line %d)' % (k + 1, ev, [ln2 for ln2, ev2 in sscf if ev2 == ev and ln2 < nopt][-1], ln, nopt)
    if len(co) >= 8:
        line += ' d(O1-H4)=%.4f d(H4-O8)=%.4f d(O1-O8)=%.4f d(C6-O8)=%.4f' % (d(co[0], co[3]), d(co[3], co[7]), d(co[0], co[7]), d(co[5], co[7]))
    print(line + de)
    prev = ev
