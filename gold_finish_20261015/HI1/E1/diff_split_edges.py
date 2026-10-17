from rdkit import Chem
RSMI='[CH3:1][C:2](=[O:4])[CH2:3]([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1.[O:13]=[C:14]([OH:15])[C@@H:16]1[CH2:17][CH2:18][CH2:19][N:20]1([H:21])'
CSMI='[CH3:1][C:2]([CH2:3]([H:22]))([O:4]([H:21]))[N:20]1[CH2:19][CH2:18][CH2:17][C@H:16]1[C:14](=[O:13])[OH:15].[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1'
PSMI='[CH3:1][C:2](=[CH2:3])[N:20]2[CH2:19][CH2:18][CH2:17][C@H:16]2[C:14](=[O:13])[OH:15].[O:4]([H:21])([H:22]).[O:5]=[CH:6][c:7]1[cH:8][cH:9][cH:10][cH:11][cH:12]1'
def parse(s):
    p=Chem.SmilesParserParams(); p.removeHs=False
    return Chem.MolFromSmiles(s,p)
def bonds(m):
    d={}
    for b in m.GetBonds():
        l1=b.GetBeginAtom().GetAtomMapNum(); l2=b.GetEndAtom().GetAtomMapNum()
        if l1==0 or l2==0: continue
        d[tuple(sorted((l1,l2)))]=int(b.GetBondTypeAsDouble())
    return d
for n,s in (('RC',RSMI),('CARB',CSMI),('I1',PSMI)):
    m=parse(s)
    print(n,'atoms(with explicit H)=',m.GetNumAtoms(),' labels:',sorted(a.GetAtomMapNum() for a in m.GetAtoms() if a.GetAtomMapNum()>0))
r,c,p=bonds(parse(RSMI)),bonds(parse(CSMI)),bonds(parse(PSMI))
def diff(a,b,na,nb):
    br=sorted(k for k in a if k not in b); fo=sorted(k for k in b if k not in a)
    oc=sorted((k,a[k],b[k]) for k in a if k in b and a[k]!=b[k])
    print(na,'->',nb,'| break:',br,'| form:',fo,'| order_change:',oc)
diff(r,c,'RC','CARB')
diff(c,p,'CARB','I1')