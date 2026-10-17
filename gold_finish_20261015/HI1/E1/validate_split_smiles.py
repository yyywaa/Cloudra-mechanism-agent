from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors
base='[CH3:1][C:2]([CH2:3]([H:22]))([O:4]([H:21]))[N:20]1[CH2:19][CH2:18][CH2:17][C%sH:16]1[C:14](=[O:13])[OH:15].[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1'
g=Chem.RWMol(Chem.MolFromXYZFile('gold_finish_20261015/HI1/E1/split/INT1_27_start.xyz'))
rdDetermineBonds.DetermineBonds(g,charge=0); g=g.GetMol()
for tag in ('@','@@'):
    s=base%tag
    m=Chem.MolFromSmiles(s)
    if m is None: print(tag,'parse fail'); continue
    Chem.AssignCIPLabels(m)
    cip=[(a.GetAtomMapNum(),a.GetPropsAsDict().get('_CIPCode')) for a in m.GetAtoms() if a.HasProp('_CIPCode')]
    q2=Chem.RemoveHs(m)
    main=[f for f in Chem.GetMolFrags(q2, asMols=True, sanitizeFrags=True) if any(a.GetAtomMapNum()==20 for a in f.GetAtoms())][0]
    mt=g.GetSubstructMatch(main, useChirality=True)
    print(tag,'CIP',cip,' chiral-match-INT1_27:',bool(mt),' natoms(smiles):',m.GetNumAtoms(),' formula',rdMolDescriptors.CalcMolFormula(m))