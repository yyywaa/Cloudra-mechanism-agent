#!/usr/bin/env python3
"""Parse Gaussian 16 logs (read-only): frames, SCF energies, freqs, terminations."""
import math, sys, hashlib, re

def elem(s):
    return ''.join(c for c in s if c.isalpha())

ZSYM = {1: 'H', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 15: 'P', 16: 'S', 17: 'Cl'}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def frames(path):
    out = []
    with open(path) as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        if 'Input orientation' in l:
            k = i + 5
            atoms = []
            while k < len(lines) and '-----' not in lines[k]:
                p = lines[k].split()
                if len(p) >= 6:
                    atoms.append((int(p[0]), ZSYM.get(int(p[1]), 'X'), float(p[3]), float(p[4]), float(p[5])))
                k += 1
            out.append({'line': i + 1, 'atoms': atoms})
    return out

def scf_lines(path):
    out = []
    with open(path) as f:
        for i, l in enumerate(f, 1):
            if 'SCF Done' in l:
                m = re.search(r'=\s*(-?\d+\.\d+)', l)
                if m:
                    out.append((i, float(m.group(1))))
    return out

def freq_info(path):
    vals = []
    lowf = []
    with open(path) as f:
        for i, l in enumerate(f, 1):
            if 'Frequencies --' in l:
                for v in re.findall(r'-?\d+\.\d+', l.split('--', 1)[1]):
                    vals.append((i, float(v)))
            if l.strip().startswith('Low frequencies'):
                lowf.append((i, l.strip()))
    neg = [(i, v) for i, v in vals if v < 0]
    return {'n_freq': len(vals), 'n_neg': len(neg), 'neg': neg,
            'min': (min(v for _, v in vals) if vals else None),
            'first_freq_line': (vals[0][0] if vals else None),
            'lowfreq': lowf[:2]}

def termination(path):
    out = []
    with open(path) as f:
        for i, l in enumerate(f, 1):
            if 'Normal termination' in l or 'Error termination' in l:
                out.append((i, l.strip()[:90]))
    return out

def optdone(path):
    out = []
    with open(path) as f:
        for i, l in enumerate(f, 1):
            if 'Stationary point found' in l or 'Optimization completed' in l:
                out.append((i, l.strip()[:80]))
    return out

def d(atoms, i, j):
    p = {a[0]: a for a in atoms}
    return math.dist(p[i][2:5], p[j][2:5])

if __name__ == '__main__':
    cmd = sys.argv[1]; path = sys.argv[2]
    if cmd == 'info':
        fr = frames(path)
        print('file', path)
        print('sha256', sha256(path))
        print('n_input_orientation_frames', len(fr), 'last_header_line', fr[-1]['line'] if fr else None,
              'natoms', len(fr[-1]['atoms']) if fr else 0)
        print('terminations', termination(path))
        print('opt_flags(opt chain)', optdone(path)[:6], '... total', len(optdone(path)))
        s = scf_lines(path)
        print('n_scf', len(s), 'last_scf', s[-1] if s else None)
        print('freq', freq_info(path))
    elif cmd == 'geom':
        fr = frames(path)
        at = fr[-1]['atoms']
        print('last frame line', fr[-1]['line'], 'natoms', len(at))
        for pr in sys.argv[3:]:
            i, j = [int(x) for x in pr.split('-')]
            print('d(%d,%d) = %.4f' % (i, j, d(at, i, j)))
    elif cmd == 'xyz':
        fr = frames(path)
        at = fr[-1]['atoms']
        out = sys.argv[3]
        with open(out, 'w') as f:
            f.write('%d\n' % len(at))
            f.write('%s frame line %d\n' % (path, fr[-1]['line']))
            for i, e, x, y, z in at:
                f.write('%-2s %14.8f %14.8f %14.8f\n' % (e, x, y, z))
        print('wrote', out)
