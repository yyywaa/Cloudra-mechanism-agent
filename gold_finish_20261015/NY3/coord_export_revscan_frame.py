#!/usr/bin/env python3
"""Export the converged constrained-scan point p5 (2.0271 A) of the NY3 E1 reverse
relaxed scan (job 1023) as a TS-guess frame, in BOTH atom orders.

Geometry is taken from the log's OWN 'Input orientation' block for that point
(input atom order; never the Standard orientation by declared index).
  job-1023 (.gjf) order : 1 Na | 2 C(Me) | 3 O(OMe) | 4 C4 | 5 O(hydroxyl, H11) |
                          6 O(carbonyl) | 7,8,9 H(Me) | 10 H(on C4) | 11 H(on O5)
  reactant/working order: 1 Na | 2 O1 | 3 H6 | 4 C2(Me) | 5 O3(OMe) | 6 C4 | 7 O5 |
                          8,9,10 H(Me) | 11 H(formyl)
  mapping J: r_k = j[J[k-1]]  (== atom_map [1,4,5,6,2,7,8,9,10,11,3])
"""
import re, sys

J = [1, 5, 11, 2, 3, 4, 6, 7, 8, 9, 10]
SYM = {1: 'H', 6: 'C', 8: 'O', 11: 'Na'}
PT = int(sys.argv[2]) if len(sys.argv) > 2 else 5

lines = open(sys.argv[1], errors='replace').read().split('\n')
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
end = done[PT - 1]
b = [x for x in blocks if x[0] < end][-1]
at_j = b[1]
scf = [(i + 1, float(m.group(1))) for i, l in enumerate(lines)
       for m in [re.search(r'SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)', l)] if m]
el, ev = [x for x in scf if x[0] < end][-1]   # el = line, ev = energy

def w(path, order, comment):
    with open(path, 'w') as f:
        f.write('11\n%s\n' % comment)
        for k in order:
            a = at_j[k - 1]
            f.write('%-2s %14.8f %14.8f %14.8f\n' % (SYM[a[0]], a[1], a[2], a[3]))

base = sys.argv[3]
r_ord = J
p_ord = list(range(1, 12))
w(base + '_reactantorder.xyz', r_ord, 'NY3 E1 job1023 scan point p%d (R(4,5)=2.0271 A) converged frame, reactant/working order; log line %d, E=%.9f (L%d)' % (PT, b[0], ev, el))
w(base + '_productorder.xyz', p_ord, 'NY3 E1 job1023 scan point p%d (R(4,5)=2.0271 A) converged frame, job .gjf (product) order; log line %d, E=%.9f (L%d)' % (PT, b[0], ev, el))

def d(A, i, j):
    return sum((A[i-1][t]-A[j-1][t])**2 for t in (1, 2, 3)) ** 0.5
A = [at_j[k-1] for k in J]
print('source Input orientation block starts at L%d ; point %d ends at L%d ; E=%.9f (L%d)' % (b[0], PT, end, ev, el))
print('reactant-order elements: %s' % [SYM[a[0]] for a in A])
print('product-order  elements: %s' % [SYM[a[0]] for a in at_j])
print('cross-check d(O1-C4): reactant-order %.6f | product-order %.6f' % (d(A, 2, 6), d(at_j, 4, 5)))
print('cross-check Na-O1:    reactant-order %.6f | product-order %.6f' % (d(A, 1, 2), d(at_j, 1, 5)))
mx = 0.0
for k in range(11):
    mx = max(mx, sum((A[k][t]-at_j[J[k]-1][t])**2 for t in (1, 2, 3)) ** 0.5)
print('max per-atom deviation between the two exported orders after mapping: %.2e A' % mx)
