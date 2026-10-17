#!/usr/bin/env python3
"""Lowest-real-mode reporter for a Gaussian frequency log.

Reports the first band of the analytic 'Frequencies --' table (the lowest real
mode), its line number, per-atom |d| leaders, and how much of the
mean-square displacement sits on declared bonds of interest.

Usage: python3 freq_lowmode_oh.py <freq.log> [--mode N]
"""
import hashlib, math, re, sys

PT = {1: 'H', 6: 'C', 7: 'N', 8: 'O'}


def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def parse_modes(path):
    lines = open(path).read().splitlines()
    freqs, disp, atoms, flines = [], [], None, []
    i = 0
    while i < len(lines):
        s = lines[i]
        if s.strip().startswith('Frequencies --'):
            vals = [float(x) for x in s.split('--', 1)[1].split()]
            freqs.extend(vals)
            flines.append(i + 1)
            # displacement block: skip until 'Atom  AN' header, then read rows
            j = i + 1
            hdr = None
            while j < len(lines) and 'Atom' not in lines[j]:
                j += 1
            if j < len(lines):
                hdr = lines[j]
                j += 1
                rows = []
                while j < len(lines):
                    parts = lines[j].split()
                    if len(parts) < 5 or not parts[0].isdigit():
                        break
                    rows.append(parts)
                    j += 1
                if atoms is None and rows:
                    atoms = [(int(r[0]), int(r[1])) for r in rows]
                disp.append(rows)
                i = j
                continue
        i += 1
    return freqs, disp, atoms, flines


def main():
    log = sys.argv[1]
    sel = None
    if '--mode' in sys.argv:
        sel = int(sys.argv[sys.argv.index('--mode') + 1])
    freqs, disp, atoms, flines = parse_modes(log)
    if not freqs:
        print('NO normal-mode block found')
        return
    imag = [n + 1 for n, v in enumerate(freqs) if v < 0]
    n = sel if sel is not None else 1
    if n < 1 or n > len(freqs):
        sys.exit('mode index out of range')
    v = freqs[n - 1]
    rows = disp[(n - 1) // 3]
    col = (n - 1) % 3
    vec = []
    for r in rows:
        k = 2 + 3 * col
        vec.append([float(r[k]), float(r[k + 1]), float(r[k + 2])])
    norms = [math.sqrt(sum(c * c for c in q)) for q in vec]
    tot = sum(q * q for q in norms)
    bonds = [(2, 25), (25, 26), (10, 27), (11, 27), (28, 24), (2, 4), (9, 10), (9, 11), (4, 26), (4, 2)]
    print('log: %s' % log)
    print('  sha256 %s' % sha256(log))
    print('  modes parsed = %d ; imaginary = %d %s' % (len(freqs), len(imag), imag[:6]))
    print('  lowest bands (cm^-1): ' + ', '.join('%d:%.4f' % (k + 1, f) for k, f in enumerate(freqs[:6])))
    print('  reported mode %d = %.4f cm^-1 ; Frequencies line L%d' % (n, v, flines[(n - 1) // 3]))
    top = sorted(((norms[a - 1], a) for a, _ in atoms), reverse=True)[:10]
    print('  largest per-atom |d|: ' + ', '.join('%d(%s)=%.3f' % (a, PT.get(dict(atoms)[a], '?'), d) for d, a in top))
    print('  projection shares of mean-square displacement:')
    for i, j in bonds:
        if i - 1 < len(vec) and j - 1 < len(vec):
            dv = [vec[i - 1][k] - vec[j - 1][k] for k in range(3)]
            s = sum(c * c for c in dv)
            print('    bond (%d,%d) %s-%s : |d_i - d_j|^2 = %.4f  (%.2f%%)' %
                  (i, j, PT.get(dict(atoms)[i], '?'), PT.get(dict(atoms)[j], '?'), s, 100.0 * s / tot if tot else 0.0))
    soft = v < 30.0
    print('  softness flag (lowest real mode < 30 cm^-1): %s' % ('YES - coordinates are soft' if soft else 'no'))


if __name__ == '__main__':
    main()
