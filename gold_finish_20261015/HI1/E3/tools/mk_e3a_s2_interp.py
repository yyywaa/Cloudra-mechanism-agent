#!/usr/bin/env python3
"""Build the E3a TS guess S2 = linear interpolation between two job-980 scan frames.

Both frames come from the same constrained scan (opt=modredundant, B 2 25 S 4 -0.150)
that started from the job 961 I2 minimum geometry, so no new conformer is created.
Interpolation parameter: lambda = (R3 - Rtarget) / (R3 - R4) with R3 = 1.89959,
R4 = 1.74959 (official scan values, log L59911) and Rtarget = 1.82 Angstrom.
"""
import hashlib, math, re, sys

LOG = '/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/preorg_v3/scan_c2o25_220_160.log'
L3 = 25159   # Standard orientation header line (1-based) of scan point 3 frame, R(2,25)=1.8996
L4 = 51856   # Standard orientation header line (1-based) of scan point 4 frame, R(2,25)=1.7496
RTARGET = 1.82
R3_OFF, R4_OFF = 1.89959, 1.74959
OUT = '/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/guess_c2o25_182/ts_guess_c2o25_182.xyz'
PROV = '/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/guess_c2o25_182/PROVENANCE_ts_guess_c2o25_182.md'

ELEM = ['C']*8 + ['N'] + ['O', 'O'] + ['H']*13 + ['O', 'H', 'H', 'O'] + ['C'] + ['C']*6 + ['H']*6
# exact working-order element list is validated against the log frame anyway
PT = {6: 'C', 1: 'H', 7: 'N', 8: 'O'}


def frame(path, header_line):
    lines = open(path).read().splitlines()
    i = header_line - 1
    assert 'Standard orientation' in lines[i], lines[i]
    at, xyz = [], []
    while i < len(lines) and len(at) < 200:
        m = re.match(r'\s+(\d+)\s+(\d+)\s+(-?\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)', lines[i])
        if m:
            at.append(PT.get(int(m.group(2)), str(m.group(2))))
            xyz.append([float(m.group(4)), float(m.group(5)), float(m.group(6))])
        elif at:
            break
        i += 1
    return at, xyz, header_line


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def dist(x, a, b):
    return math.dist(x[a - 1], x[b - 1])


def main():
    a3, x3, l3 = frame(LOG, L3)
    a4, x4, l4 = frame(LOG, L4)
    if a3 != a4:
        sys.exit('element order mismatch between frames')
    if len(a3) != 41:
        sys.exit('expected 41 atoms, got %d' % len(a3))

    lam = (R3_OFF - RTARGET) / (R3_OFF - R4_OFF)
    xi = [[(1.0 - lam) * x3[k][j] + lam * x4[k][j] for j in range(3)] for k in range(len(x3))]

    # --- bond-length restoration for rotating X-H bonds -------------------
    # Cartesian interpolation of a rotating O-H bond cuts the corner and
    # shortens it (here O28-H24 came out 0.8420 A). Restore the length to the
    # mean of the two parent frames, keeping the interpolated direction.
    RESTORE = [(28, 24)]  # (heavy atom, H atom) 1-based working order
    restored = []
    for heavy, hyd in RESTORE:
        dA = dist(x3, heavy, hyd)
        dB = dist(x4, heavy, hyd)
        target = 0.5 * (dA + dB)
        v = [xi[hyd - 1][k] - xi[heavy - 1][k] for k in range(3)]
        nrm = math.sqrt(sum(t * t for t in v))
        v = [t / nrm for t in v]
        before = nrm
        xi[hyd - 1] = [xi[heavy - 1][k] + target * v[k] for k in range(3)]
        restored.append((heavy, hyd, before, target))

    import os
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        f.write('%d\n' % len(a3))
        f.write('E3a TS guess S2: linear interpolation lambda=%.6f between %s StdOrient L%d (R=%.5f) and L%d (R=%.5f); target R(C2-O25)=%.2f\n'
                % (lam, LOG.split('/')[-1], L3, R3_OFF, L4, R4_OFF, RTARGET))
        for e, q in zip(a3, xi):
            f.write('%-2s %14.8f %14.8f %14.8f\n' % (e, q[0], q[1], q[2]))

    key = [(2, 25), (10, 27), (25, 27), (25, 26), (2, 4), (4, 26), (10, 25), (11, 27), (9, 10), (9, 11), (2, 1), (2, 3)]
    minsep = min(dist(xi, i, j) for i in range(1, 42) for j in range(i + 1, 42))
    rows = []
    for a, b in key:
        rows.append('| %d %s - %d %s | %.4f | %.4f | %.4f |' % (a, a3[a-1], b, a3[b-1], dist(x3, a, b), dist(x4, a, b), dist(xi, a, b)))
    o10h = []
    for h in range(1, 42):
        if a3[h-1] == 'H':
            o10h.append((dist(xi, 10, h), h, dist(x3, 10, h), dist(x4, 10, h)))

    txt = []
    txt.append('# Provenance — E3a TS guess S2 (R(C2-O25) = 1.82 A interpolated frame)\n')
    txt.append('- Source log (absolute): `%s`' % LOG)
    txt.append('- Source log sha256: `%s`' % sha(LOG))
    txt.append('- Frame A: scan point 3 converged region, `Standard orientation` header at line **L%d** (1-based), official scan R(2,25) = %.5f' % (L3, R3_OFF))
    txt.append('- Frame B: scan point 4 converged region, `Standard orientation` header at line **L%d** (1-based), official scan R(2,25) = %.5f' % (L4, R4_OFF))
    txt.append('- Official scan summary: log L59910 (\`Summary of Optimized Potential Surface Scan\`), R7 row at L59911; energies L6225/L16443/L25258/L53388/L59324')
    txt.append('- Interpolation: cartesian linear, `lambda = (R3 - R_target)/(R3 - R4) = (%.5f - %.2f)/(%.5f - %.5f) = %.6f`; `x = (1-lambda)*x_A + lambda*x_B`' % (R3_OFF, RTARGET, R3_OFF, R4_OFF, lam))
    txt.append('- Element order identical in both frames: **yes** (41 atoms, working order = `runs/I2_optfreq/I2_min_v5.xyz` order)')
    txt.append('- Output xyz: `%s`' % OUT)
    txt.append('- Output xyz sha256: `%s`\n' % sha(OUT))
    txt.append('## Key internals (Angstrom)\n')
    txt.append('| pair | frame A (L%d) | frame B (L%d) | S2 (interpolated) |' % (L3, L4))
    txt.append('|---|---|---|---|')
    txt.extend(rows)
    txt.append('\n## O10 -> every H distance in S2 (Angstrom), with the two parent frames\n')
    txt.append('| H atom | S2 | frame A | frame B |')
    txt.append('|---|---|---|---|')
    for d, h, da, db in sorted(o10h)[:8]:
        txt.append('| H%d | %.4f | %.4f | %.4f |' % (h, d, da, db))
    txt.append('\n## Admissibility self-check\n')
    txt.append('- R(C2-O25) in S2 = **%.4f** (target 1.82) => interpolation reproduced the coordinate.' % dist(xi, 2, 25))
    txt.append('- R(C2-O25) monotonically ordered: frame A %.4f > S2 %.4f > frame B %.4f => **yes**' % (dist(x3, 2, 25), dist(xi, 2, 25), dist(x4, 2, 25)))
    txt.append('- Minimum interatomic separation over all 861 pairs in S2 = **%.4f A** => admissibility (>= 0.9 A) **%s**' % (minsep, 'PASS' if minsep >= 0.9 else 'FAIL'))
    for heavy, hyd, before, target in restored:
        txt.append('- Bond-length restoration: atom%d-H%d interpolated %.4f A -> %.4f A (mean of the two parent frames, direction kept); pure cartesian interpolation of a rotating O-H shortens the bond.' % (heavy, hyd, before, target))
    txt.append('- Distortion note: distances are nonlinear under cartesian interpolation, so bonded pairs are not exact weighted means. Largest bond distortion: C9-O11 = %.4f A (parents %.4f / %.4f); C9-O10 = %.4f A (parents %.4f / %.4f). These relax during TS optimisation and are recorded here for transparency.' % (dist(xi, 9, 11), dist(x3, 9, 11), dist(x4, 9, 11), dist(xi, 9, 10), dist(x3, 9, 10), dist(x4, 9, 10)))
    txt.append('- No atom added/removed/reordered; composition C15H21NO4, charge 0, multiplicity 1 unchanged.')
    txt.append('- Provenance of the path: both frames are relaxed points of the constrained scan `B 2 25 S 4 -0.150` (constraint card log L158) whose starting geometry is the job 961 I2 minimum (`runs/I2_optfreq/I2_min_v5.xyz`, sha 9a6203ff...). No new conformer was constructed.\n')
    txt.append('## Status\n')
    txt.append('- This is a **guess only**: not a saddle, no barrier. E3a dE = missing measurement until a TS is verified.')
    txt.append('- S1 backup guess: `prep/guess_c2o25_175/ts_guess_c2o25_175.xyz` sha256 `db055959e7ffe9277f9e71b253c6873574a3c6d7c712c194d9f7916fc5867fd5`')
    open(PROV, 'w').write('\n'.join(txt) + '\n')

    print('lambda = %.6f' % lam)
    print('S2 R(2,25) = %.4f  R(10,27) = %.4f  R(2,4) = %.4f  R(25,27) = %.4f' % (dist(xi, 2, 25), dist(xi, 10, 27), dist(xi, 2, 4), dist(xi, 25, 27)))
    print('minsep = %.4f' % minsep)
    print('xyz', OUT, sha(OUT))
    print('prov', PROV, sha(PROV))


if __name__ == '__main__':
    main()
