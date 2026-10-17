#!/usr/bin/env python3
"""HI1_E1 / lane1 — read-only evidence extractor for a Gaussian 16 log of this batch.

Usage:
  python3 extract_endpoint_identity.py <log> [--pairs "a,b;c,d;..."] [--order canonical|job51]

Prints (raw line + line number):
  * every 'SCF Done' line (number + text), flagged last one
  * 'Optimization completed.' / 'Stationary point found.' / 'Normal termination' lines
  * 'imaginary frequencies' related lines
  * number of 'Frequencies --' groups (x3 = modes) and the 3 lowest + 3 highest frequencies with line numbers
  * the LAST geometry (Standard/Input orientation) analysed with RDKit: formula, fragments, CIP labels,
    and (if --pairs) the listed 1-based pair distances.
--order job51 converts the printed pair indices from 'canonical binding order' to the job_51 order used
  by the RC_optfreq / I1_optfreq logs (table from E1/TS_GUESS_PROVENANCE.md section 3).
"""
import sys, subprocess
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors
import numpy as np

CANON2J51 = {1:3,2:2,3:25,4:1,5:14,6:15,7:16,8:12,9:13,10:27,11:28,12:29,13:30,14:31,15:32,16:33,17:34,
             18:35,19:36,20:37,21:38,22:39,23:40,24:41,25:10,26:9,27:11,28:8,29:7,30:6,31:5,32:4,33:24,
             34:23,35:21,36:22,37:19,38:20,39:17,40:18,41:26}
SYM = {1:'H',6:'C',7:'N',8:'O'}

def main():
    log = sys.argv[1]
    pairs = None; order = 'canonical'
    if '--pairs' in sys.argv:
        pairs = [tuple(int(x) for x in p.split(',')) for p in sys.argv[sys.argv.index('--pairs')+1].split(';')]
    if '--order' in sys.argv:
        order = sys.argv[sys.argv.index('--order')+1]
    lines = open(log).read().split(chr(10))
    print('log =', subprocess.run(['sha256sum', log], capture_output=True, text=True).stdout.strip())
    scf = [(i+1, l) for i, l in enumerate(lines) if 'SCF Done' in l]
    for i, l in scf[-3:]:
        print('SCF  L%-7d %s' % (i, l.strip()))
    for pat in ['Optimization completed.', 'Stationary point found.', 'Normal termination', 'imaginary', 'Error termination', 'Convergence failure']:
        for i, l in enumerate(lines):
            if pat in l:
                print('%-24s L%-7d %s' % (pat, i+1, l.strip()))
    fg = [(i+1, l) for i, l in enumerate(lines) if 'Frequencies --' in l]
    print('Frequencies groups =', len(fg), ' -> modes =', 3*len(fg))
    if fg:
        print('lowest  L%-7d %s' % fg[0]); print('highest L%-7d %s' % fg[-1])
    orient = [i for i, l in enumerate(lines) if 'Standard orientation' in l] or [i for i, l in enumerate(lines) if 'Input orientation' in l]
    if not orient:
        print('no orientation block found'); return
    b = orient[-1]
    geom = []
    for l in lines[b+5:b+50]:
        p = l.split()
        if len(p) == 6 and p[0].isdigit():
            geom.append((SYM.get(int(p[1]), 'X'), float(p[3]), float(p[4]), float(p[5])))
        elif geom:
            break
    print('last geometry block at L%d, atoms=%d' % (b+1, len(geom)))
    p_ = '/tmp/lastgeom_%s.xyz' % log.split('/')[-1].replace('.log','')
    open(p_, 'w').write('%d\n%s\n' % (len(geom), log) + chr(10).join('%s %.6f %.6f %.6f' % g for g in geom))
    m = Chem.RWMol(Chem.MolFromXYZFile(p_))
    rdDetermineBonds.DetermineBonds(m, charge=0)
    m = m.GetMol(); Chem.AssignStereochemistryFrom3D(m); Chem.AssignCIPLabels(m)
    print('xyz dumped to', p_)
    print('formula', rdMolDescriptors.CalcMolFormula(m), 'frags', len(Chem.GetMolFrags(m)))
    print('frags:', [Chem.MolToSmiles(f) for f in Chem.GetMolFrags(m, asMols=True, sanitizeFrags=True)])
    print('CIP:', [(a.GetIdx()+1, a.GetSymbol(), a.GetPropsAsDict().get('_CIPCode')) for a in m.GetAtoms() if a.HasProp('_CIPCode')])
    if pairs:
        P = np.array([[g[1], g[2], g[3]] for g in geom])
        for a, b_ in pairs:
            ia, ib = (CANON2J51[a], CANON2J51[b_]) if order == 'job51' else (a, b_)
            print('  pair (%2d,%2d) [log-order %2d,%2d]  %.3f A' % (a, b_, ia, ib, float(np.linalg.norm(P[ia-1]-P[ib-1]))))

main()
