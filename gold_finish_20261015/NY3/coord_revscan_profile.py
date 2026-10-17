#!/usr/bin/env python3
"""Index-safe profile + branch diagnostics for the NY3 E1 reverse relaxed scan (job 1023).

Geometry reads use the Gaussian log's own 'Input orientation' blocks (input atom order),
never the Standard orientation by declared index. Atom numbering = the job's .gjf order:
 1 Na | 2 C(Me) | 3 O(OMe) | 4 C4 | 5 O(=O1, bears H11) | 6 O(alkoxide) |
 7,8,9 H(Me) | 10 H(on C4) | 11 H(on O5)
"""
import re, sys

I1 = -467.004842486
RC = -466.986564979
K = 627.509474

def dist(A, i, j):
    a, b = A[i - 1], A[j - 1]
    return ((a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2) ** 0.5

def ang(A, i, j, k):
    import math
    def v(p, q):
        return [A[q-1][t]-A[p-1][t] for t in (1, 2, 3)]
    u, w = v(j, i), v(j, k)
    nu = sum(x*x for x in u) ** 0.5
    nw = sum(x*x for x in w) ** 0.5
    c = sum(u[t]*w[t] for t in range(3)) / (nu*nw)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

def dih(A, i, j, k, l):
    import math
    def v(p, q):
        return [A[q-1][t]-A[p-1][t] for t in (1, 2, 3)]
    def cross(a, b):
        return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    b1, b2, b3 = v(i, j), v(j, k), v(k, l)
    n1, n2 = cross(b1, b2), cross(b2, b3)
    m = cross(n1, [x / (sum(y*y for y in b2) ** 0.5) for x in b2])
    x = sum(n1[t]*n2[t] for t in range(3))
    y = sum(m[t]*n2[t] for t in range(3))
    return math.degrees(math.atan2(y, x))

def main(path):
    lines = open(path, errors='replace').read().split('\n')
    scf = [(i+1, float(m.group(1))) for i, l in enumerate(lines)
           for m in [re.search(r'SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)', l)] if m]
    done = [i+1 for i, l in enumerate(lines) if l.strip().startswith('Optimization completed.')]
    cons = [(i+1, float(m.group(1)), 'Scan' in l) for i, l in enumerate(lines)
            for m in [re.search(r'!\s+R9\s+R\(4,5\)\s+([\d.]+)', l)] if m]
    term = [(i+1, l.strip()) for i, l in enumerate(lines)
            if 'Normal termination of Gaussian 16' in l or 'Error termination' in l]
    atomre = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$')
    blocks = []
    for i, l in enumerate(lines):
        if 'Input orientation:' in l:
            j = i + 1
            while j < len(lines) and not atomre.match(lines[j]) and j - i <= 12:
                j += 1
            atoms = []
            while j < len(lines) and atomre.match(lines[j]):
                m = atomre.match(lines[j])
                atoms.append((int(m.group(2)), float(m.group(4)), float(m.group(5)), float(m.group(6))))
                j += 1
            if len(atoms) == 11:
                blocks.append((i+1, atoms))
    print('log=%s lines=%d  input-orientation blocks=%d' % (path, len(lines), len(blocks)))
    print('scan-constraint rows (line, value, init?): %s' % cons)
    print('Optimization completed lines: %s' % done)
    print('termination lines: %s' % term)
    hdr = ('pt  cons/R(4,5)  E/Ha            E_line  dE_I1  dE_RC  | d45    Na-O3  Na-O5  Na-O6  Na-C4'
           '  | C4-O3  C4-O6  C4-H10 O5-H11 | nearest-heavy-to-H11  D(H11-O5-C4-O6)  D(H7-C2-O3-C4)')
    print(hdr)
    for p, end in enumerate(done):
        e = [x for x in scf if x[0] < end]
        if not e:
            continue
        el, ev = e[-1]
        b = [x for x in blocks if x[0] < end]
        if not b:
            continue
        A = b[-1][1]
        # The '! R9 R(4,5) x.xxxx' row is printed AFTER that point's
        # 'Optimization completed.' line (Optimized Parameters table), so the value
        # belonging to this point is the FIRST non-init row with line > end.
        cand = [c[1] for c in cons if (not c[2]) and c[0] > end]
        cv = min(cand) if cand else None
        ncand = min([(dist(A, 11, x), x) for x in (3, 4, 6)])
        print('%2d  %9.4f  %14.9f  %6d  %+6.2f %+6.2f | %5.3f  %5.3f  %5.3f  %5.3f  %5.3f'
              ' | %5.3f  %5.3f  %5.3f  %5.3f | %6.3f (atom %d) %10.2f %10.2f'
              % (p+1, cv if cv else float('nan'), ev, el, (ev-I1)*K, (ev-RC)*K,
                 dist(A, 4, 5), dist(A, 1, 3), dist(A, 1, 5), dist(A, 1, 6), dist(A, 1, 4),
                 dist(A, 4, 3), dist(A, 4, 6), dist(A, 4, 10), dist(A, 5, 11),
                 ncand[0], ncand[1], dih(A, 11, 5, 4, 6), dih(A, 7, 2, 3, 4)))
    # Na coordination sphere of the last converged point (contacts < 2.75 A)
    if done:
        A = [x for x in blocks if x[0] < done[-1]][-1][1]
        contacts = sorted([(round(dist(A, 1, x), 3), x) for x in (3, 4, 5, 6) if dist(A, 1, x) < 2.75])
        print('last point Na contacts (<2.75 A): %s' % contacts)

if __name__ == '__main__':
    main(sys.argv[1])
