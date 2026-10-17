import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])

def block_at(path, start_line):
    lines = open(path,'rb').read().decode('utf-8','replace').splitlines()
    k = start_line-1+5; atoms=[]
    while k < len(lines):
        if lines[k].strip().startswith('-----'): break
        p = lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms

def key(atoms):
    m = Chem.RWMol()
    for z,_,_,_ in atoms:
        m.AddAtom(Chem.Atom(int(z)))
    conf = Chem.Conformer(len(atoms))
    for i,(z,x,y,zz) in enumerate(atoms):
        conf.SetAtomPosition(i, (x,y,zz))
    mol = m.GetMol(); mol.AddConformer(conf)
    rdDetermineBonds.DetermineBonds(mol, charge=0)
    Chem.SanitizeMol(mol)
    return inchi.MolToInchiKey(mol), inchi.MolToInchi(mol)

a73 = block_at('gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log', 51477)
ap  = block_at('gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log', 68977)
for nm, a in (('1073 final', a73), ('P final', ap)):
    k, i = key(a)
    print(nm, 'InChIKey =', k)
    print('   InChI =', i)
