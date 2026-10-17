#!/usr/bin/env python3
"""HI1 package (coordinator as_84bdf87a0f94416c) independent geometry-identity checker.
Usage: python3 hi1_cip_tools.py <file.xyz|file.log> [more files...]
For a Gaussian .log it extracts the LAST "Standard orientation" block (the optimized geometry).
It perceives bonds with RDKit DetermineBonds(charge=0), assigns stereo from 3D and prints
1-based indices, elements, CIP codes and neighbours of every stereocentre.
Also prints max |d| vs any .xyz given with --cmp."""
import sys, numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds

ELEM = {1:'H',6:'C',7:'N',8:'O'}

def read_xyz(p):
    lines = open(p).read().splitlines()
    n = int(lines[0].split()[0]); syms=[]; xyz=[]
    for l in lines[2:2+n]:
        t=l.split(); syms.append(t[0]); xyz.append([float(t[1]),float(t[2]),float(t[3])])
    return syms, np.array(xyz)

def read_gjf(p):
    lines = open(p).read().splitlines()
    start = None
    for i,l in enumerate(lines):
        t = l.split()
        if len(t)==2 and all(x.lstrip('-').isdigit() for x in t) and i>3:
            start = i+1; break
    if start is None: raise SystemExit('no charge/mult line in '+p)
    syms=[]; xyz=[]
    for l in lines[start:]:
        t=l.split()
        if len(t)<4: break
        syms.append(t[0]); xyz.append([float(t[1]),float(t[2]),float(t[3])])
    return syms, np.array(xyz)

def last_std_orientation(logp):
    lines = open(logp, errors='ignore').read().splitlines()
    idx = [i for i,l in enumerate(lines) if 'Standard orientation' in l]
    if not idx: raise SystemExit('no Standard orientation in '+logp)
    i = idx[-1]; syms=[]; xyz=[]; j=i+5
    while j < len(lines):
        t = lines[j].split()
        if len(t)>=6 and t[0].isdigit():
            syms.append(ELEM.get(int(t[1]),'X')); xyz.append([float(t[3]),float(t[4]),float(t[5])])
        elif '-----' in lines[j] and syms:
            break
        j += 1
    return syms, np.array(xyz)

def build(syms, xyz):
    rw = Chem.RWMol()
    for s in syms: rw.AddAtom(Chem.Atom(s))
    m = rw.GetMol()
    conf = Chem.Conformer(len(syms))
    for i,(x,y,z) in enumerate(xyz):
        conf.SetAtomPosition(i, Chem.rdGeometry.Point3D(float(x),float(y),float(z)))
    m.AddConformer(conf, assignId=True)
    rdDetermineBonds.DetermineBonds(m, charge=0)
    Chem.AssignStereochemistryFrom3D(m)
    Chem.AssignCIPLabels(m)
    return m

def report(tag, syms, xyz):
    m = build(syms, xyz)
    frags = Chem.GetMolFrags(m)
    cents = []
    for a in m.GetAtoms():
        if a.HasProp('_CIPCode'):
            nb = ','.join('%d%s' % (n.GetIdx()+1, n.GetSymbol()) for n in a.GetNeighbors())
            cents.append('%d%s=%s(nb %s)' % (a.GetIdx()+1, a.GetSymbol(), a.GetProp('_CIPCode'), nb))
    print('%-46s natoms=%d frags=%d CIP[%s]' % (tag, len(syms), len(frags), '; '.join(cents) if cents else 'none'))
    return m

if __name__ == '__main__':
    args = [a for a in sys.argv[1:]]
    geom = {}
    for a in args:
        if a.endswith('--cmp'): continue
        if a.endswith('.log'): syms, xyz = last_std_orientation(a)
        elif a.endswith('.gjf') or a.endswith('.com'): syms, xyz = read_gjf(a)
        else: syms, xyz = read_xyz(a)
        geom[a] = (syms, xyz)
        report(a.split('/')[-1], syms, xyz)
    names = list(geom)
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            s1,x1 = geom[names[i]]; s2,x2 = geom[names[j]]
            if s1 == s2 and x1.shape == x2.shape:
                d = np.abs(x1-x2).max()
                print('  maxdev %-40s vs %-40s = %.4f A' % (names[i].split('/')[-1], names[j].split('/')[-1], d))
