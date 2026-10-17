
import math, json
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdCIPLabeler, rdMolDescriptors

SRC='/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/hemiaminal_1028_lastframe.xyz'
P_SMILES='CC(=O)C[C@H](O)c1ccccc1.O=C(O)[C@@H]1CCCN1'
L=open(SRC).read().splitlines(); n=int(L[0].split()[0])
at=[[L[2+i].split()[0]]+[float(x) for x in L[2+i].split()[1:4]] for i in range(n)]
sym=[a[0] for a in at]; X=[a[1:] for a in at]
r={'H':0.31,'C':0.76,'N':0.71,'O':0.66}
def bonds(X,sym):
    s=set()
    for i in range(len(X)):
        for j in range(i+1,len(X)):
            if math.dist(X[i],X[j]) < r[sym[i]]+r[sym[j]]+0.45: s.add((i,j))
    return s
B=bonds(X,sym)
nb={i:set() for i in range(n)}
for i,j in B: nb[i].add(j); nb[j].add(i)
# proline fragment = component of N4 (index 3) without passing through C2 (index 1)
start=3; block=1
seen={start}; stack=[start]
while stack:
    u=stack.pop()
    for v in nb[u]:
        if v==block or v in seen: continue
        seen.add(v); stack.append(v)
pro=sorted(seen); keep=[i for i in range(n) if i not in seen]
print('proline fragment atoms (1-based):', [i+1 for i in pro], 'n=',len(pro))
print('ketol fragment atoms (1-based):', [i+1 for i in keep], 'n=',len(keep))
C2=1; N4=3; O25=24; H26=25
# 1) separate fragments: translate proline along C2->N4 so that C2...N4 = 2.70 A
d0=math.dist(X[C2],X[N4]); u=[(X[N4][k]-X[C2][k])/d0 for k in range(3)]
target=2.70; shift=target-d0
for i in pro:
    for k in range(3): X[i][k]+=u[k]*shift
# 2) ketone C2=O25 at 1.22 A along the original C2->O25 direction
v=[X[O25][k]-X[C2][k] for k in range(3)]; nn=math.dist([0,0,0],v); v=[x/nn for x in v]
for k in range(3): X[O25][k]=X[C2][k]+1.22*v[k]
# 3) H26 -> N4: place at 1.02 A along N4 lone-pair direction (N4 bonded to C5,C8 after C2 removal)
def unitv(a,b):
    w=[X[b][k]-X[a][k] for k in range(3)]; m=math.dist([0,0,0],w); return [x/m for x in w]
sumv=[0.0,0.0,0.0]
for j in nb[N4]:
    if j==C2: continue
    w=unitv(N4,j)
    for k in range(3): sumv[k]+=w[k]
m=math.dist([0,0,0],sumv); lp=[-x/m for x in sumv]
for k in range(3): X[H26][k]=X[N4][k]+1.02*lp[k]
# checks
def d(i,j): return math.dist(X[i],X[j])
print('after build: C2-O25 %.4f  C2-N4 %.4f  N4-H26 %.4f  O25-H26 %.4f  O10-H27 %.4f  O25-H27 %.4f'%(d(C2,O25),d(C2,N4),d(N4,H26),d(O25,H26),d(9,26),d(O25,26)))
mn=min((math.dist(X[i],X[j]),i+1,j+1) for i in range(n) for j in range(i+1,n))
print('minsep %.4f (atoms %d-%d)'%mn)
heavy=[i for i in range(n) if sym[i]!='H']
inter=min((math.dist(X[i],X[j]),i+1,j+1) for i in pro for j in keep if sym[i]!='H' and sym[j]!='H')
print('min heavy inter-fragment contact %.4f A between atoms %d-%d (1-based working)'%inter)
B2=bonds(X,sym)
only=[(i+1,j+1) for (i,j) in sorted(B2-B)]
print('new bonds vs 1028 frame:', [(i,sym[i-1],j,sym[j-1]) for i,j in only])
gone=[(i+1,j+1) for (i,j) in sorted(B-B2)]
print('lost bonds vs 1028 frame:', [(i,sym[i-1],j,sym[j-1]) for i,j in gone])
# identity check via RDKit
xyz_block='%d\nP built from job 1028 frame (E3b product)\n'%n + '\n'.join('%s %.8f %.8f %.8f'%(sym[i],X[i][0],X[i][1],X[i][2]) for i in range(n)) + '\n'
OUT='/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/P_e3b_product_41_seed.xyz'
open(OUT,'w').write(xyz_block)
print('seed written', OUT)
mol=Chem.Mol(Chem.MolFromXYZFile('/tmp/p_built.xyz'))
rdDetermineBonds.DetermineBonds(mol, charge=0)
Chem.AssignStereochemistryFrom3D(mol)
noH=Chem.RemoveHs(mol); Chem.AssignStereochemistry(noH, cleanIt=True, force=True); rdCIPLabeler.AssignCIPLabels(noH)
smi=Chem.MolToSmiles(noH)
ref=Chem.MolFromSmiles(P_SMILES); Chem.AssignStereochemistry(ref, cleanIt=True, force=True); rdCIPLabeler.AssignCIPLabels(ref)
refs=Chem.MolToSmiles(ref)
print('built canonical isomeric:', smi)
print('declared P canonical    :', refs)
print('IDENTICAL (chirality):', smi==refs)
print('frags built', len(Chem.GetMolFrags(noH)), 'heavy', noH.GetNumAtoms(), 'formula', rdMolDescriptors.CalcMolFormula(noH), 'charge', Chem.GetFormalCharge(noH))
print('CIP built:', sorted((a.GetIdx(),a.GetProp('_CIPCode')) for a in noH.GetAtoms() if a.HasProp('_CIPCode')))
json.dump({'sym':sym,'X':X}, open('/tmp/p_built.json','w'))
