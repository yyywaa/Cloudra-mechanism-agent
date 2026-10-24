from rdkit import Chem
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
def canon(s, strip=False):
    m=Chem.MolFromSmiles(s)
    if m is None: return None
    if strip:
        for a in m.GetAtoms(): a.SetAtomMapNum(0)
    return Chem.MolToSmiles(m)
given_r = r'''[CH3:1]/[C:2]([CH2:3][C@H:6]([OH:5])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1)=[N+:20]1\[CH2:19][CH2:18][CH2:17][C@H:16]1[C:14](=[O:13])[O-:15].[OH2:4]'''
given_p = r'''[CH3:1][C@@:2]([OH:4])([CH2:3][C@H:6]([OH:5])[c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1)[N:20]1[CH2:19][CH2:18][CH2:17][C@H:16]1[C:14](=[O:13])[OH:15]'''
ref_r = r'''C/C(C[C@H](O)c1ccccc1)=[N+]1\CCC[C@H]1C(=O)[O-].O'''
ref_p = r'''C[C@@](O)(C[C@H](O)c1ccccc1)N1CCC[C@H]1C(=O)O'''
for nm,g,r in [('react',given_r,ref_r),('prod',given_p,ref_p)]:
    cg=canon(g,True); cr=canon(r)
    print(nm,'given:',cg)
    print(nm,'ref  :',cr)
    print(nm,'MATCH:',cg is not None and cg==cr)
