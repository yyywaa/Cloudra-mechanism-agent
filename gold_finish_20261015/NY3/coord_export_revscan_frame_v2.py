#!/usr/bin/env python3
"""Export a converged constrained-scan point of the NY3 E1 reverse relaxed scan (job 1023)
as a TS-guess frame in BOTH atom orders. v2: the constraint value in the comment is
DERIVED from the exported geometry (d(j4,j5)), never hardcoded.

Geometry: the log's own 'Input orientation' block of that point (input atom order).
  job-1023 (.gjf) order : 1 Na | 2 C(Me) | 3 O(OMe) | 4 C4 | 5 O(hydroxyl, H11) |
                          6 O(carbonyl) | 7,8,9 H(Me) | 10 H(on C4) | 11 H(on O5)
  reactant/working order: 1 Na | 2 O1 | 3 H6 | 4 C2(Me) | 5 O3(OMe) | 6 C4 | 7 O5 |
                          8,9,10 H(Me) | 11 H(formyl)
  mapping J: r_k = j[J[k-1]]  (== atom_map [1,4,5,6,2,7,8,9,10,11,3])
"""
import math, re, sys

J = [1, 5, 11, 2, 3, 4, 6, 7, 8, 9, 10]
SYM = {1: 'H', 6: 'C', 8: 'O', 11: 'Na'}

log, pt, base = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = open(log, errors='replace').read().split('\n')
atomre = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
blocks = []
for i, l in enumerate(lines):
    if 'Input orientation:' in l:
        j = i + 1
        while j < len(lines) and not atomre.match(lines[j]) and j - i <= 12:
            j += 1
        at = []
        while j < len(lines) and atomre.match(lines[j]):
            m = atomre.match(lines[j])
            at.append((int(m.group(2)), float(m.group(4)), float(m.group(5)), float(m.group(6))))
            j += 1
        if len(at) == 11:
            blocks.append((i + 1, at))
done = [i + 1 for i, l in enumerate(lines) if l.strip().startswith('Optimization completed.')]
end = done[pt - 1]
blk = [x for x in blocks if x[0] < end][-1]
at_j = blk[1]
scf = [(i + 1, float(m.group(1))) for i, l in enumerate(lines)
       for m in [re.search(r'SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)', l)] if m]
el, ev = [x for x in scf if x[0] < end][-1]

def d(i, j):
    return math.dist(at_j[i-1][1:4], at_j[j-1][1:4])

cv = d(4, 5)
cm = 'NY3 E1 job1023 scan point p%d (constraint R(4,5)=%.4f A, derived from this geometry) converged frame; Input orientation block @L%d, point ends @L%d, E=%.9f (L%d)'
def w(path, order):
    with open(path, 'w') as f:
        f.write('11\n%s\n' % (cm % (pt, cv, blk[0], end, ev, el)))
        for k in order:
            a = at_j[k - 1]
            f.write('%-2s %14.8f %14.8f %14.8f\n' % (SYM[a[0]], a[1], a[2], a[3]))

w(base + '_reactantorder.xyz', J)
w(base + '_productorder.xyz', list(range(1, 12)))
A = [at_j[k-1] for k in J]
print('point %d: constraint R(4,5)=%.4f A (derived); block @L%d; ends @L%d; E=%.9f @L%d' % (pt, cv, blk[0], end, ev, el))
print('elements reactant=%s product=%s' % ([SYM[a[0]] for a in A], [SYM[a[0]] for a in at_j]))
print('cross-check d(O1-C4): %.6f / %.6f ; Na-O1: %.6f / %.6f'
      % (math.dist(A[1][1:4], A[5][1:4]), math.dist(at_j[4][1:4], at_j[3][1:4]),
         math.dist(A[0][1:4], A[1][1:4]), math.dist(at_j[0][1:4], at_j[4][1:4])))
