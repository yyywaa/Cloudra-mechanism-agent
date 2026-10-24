#!/usr/bin/env python3
"""Verify the generated (r2,c4) Gaussian input against the target xyz.

Checks: atom count/element order, max |delta| between .gjf coordinates and the
target xyz, the six monitored distances, frozen-coordinate block placement,
and the minimum non-bonded contact among heavy/light atom pairs (>= 1.20 A gate).

usage: python verify_r2c4_input.py <in.gjf> <target.xyz>
"""
import sys, math

def read_xyz(path):
    L = open(path).read().splitlines()
    n = int(L[0].split()[0])
    return [(f.split()[0], float(f.split()[1]), float(f.split()[2]), float(f.split()[3]))
            for f in L[2:2+n]]

def read_gjf(path):
    L = open(path).read().splitlines()
    i = 0
    while L[i].strip() and not L[i].startswith('#'):
        i += 1
    while L[i].startswith('#'):
        i += 1
    while not L[i].strip():
        i += 1
    while L[i].strip():
        i += 1
    while not L[i].strip():
        i += 1
    i += 1  # charge/mult
    at = []
    while L[i].strip():
        f = L[i].split()
        at.append((f[0], float(f[1]), float(f[2]), float(f[3])))
        i += 1
    tail = L[i:]
    return at, tail

def d(at, i, j):
    a, b = at[i-1], at[j-1]
    return math.sqrt((a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2)

def main():
    gjf, tgt = sys.argv[1], sys.argv[2]
    g, tail = read_gjf(gjf)
    t = read_xyz(tgt)
    print('gjf atoms', len(g), '| target atoms', len(t))
    print('element order identical:', [a[0] for a in g] == [a[0] for a in t])
    mx = 0.0
    for a, b in zip(g, t):
        mx = max(mx, max(abs(a[k]-b[k]) for k in (1,2,3)))
    print('max |delta(gjf - target)| = %.6f A' % mx)
    for lab, i, j in [('R(2,4)',2,4), ('R(25,26)',25,26), ('R(10,27)',10,27),
                      ('R(2,25)',2,25), ('R(2,26)',2,26), ('R(4,26)',4,26)]:
        print('%-10s %.4f' % (lab, d(g,i,j)))
    print('tail lines:', repr(tail))
    # non-bonded scan: report all pairs closer than 1.20 A excluding 1-2 and 1-3
    heavy = list(range(1, len(g)+1))
    close = []
    for i in range(1, len(g)+1):
        for j in range(i+1, len(g)+1):
            dd = d(g, i, j)
            if dd < 1.20:
                close.append((i, j, g[i-1][0]+g[j-1][0], dd))
    close.sort(key=lambda x: x[3])
    print('pairs < 1.20 A (may be 1-2 or 1-3; inspect manually):')
    for i, j, el, dd in close[:12]:
        print('   %2d-%2d %s %.4f' % (i, j, el, dd))
    h26 = sorted(((d(g,i,26), i, g[i-1][0]) for i in range(1, len(g)+1) if i != 26))[:4]
    print('nearest atoms to H26:', [('%.4f' % dd, i, e) for dd, i, e in h26])

main()
