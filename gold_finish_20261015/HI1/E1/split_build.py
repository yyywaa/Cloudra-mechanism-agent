import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors
import os
out='gold_finish_20261015/HI1/E1/split'
os.makedirs(out, exist_ok=True)
def readxyz(p):
    L=open(p).read().strip().split(chr(10))
    n=int(L[0]); return [l.split() for l in L[2:2+n]]
def writexyz(p, atoms, comment):
    open(p,'w').write('%d'%len(atoms)+chr(10)+comment+chr(10)+chr(10).join('%-3s %14.8f %14.8f %14.8f'%(a[0],float(a[1]),float(a[2]),float(a[3])) for a in atoms)+chr(10))
def check(p,label):
    m=Chem.RWMol(Chem.MolFromXYZFile(p)); rdDetermineBonds.DetermineBonds(m,charge=0); m=m.GetMol()
    print(label,'atoms',m.GetNumAtoms(),'formula',rdMolDescriptors.CalcMolFormula(m),'frags',len(Chem.GetMolFrags(m)))
    print('   frags:',[Chem.MolToSmiles(f) for f in Chem.GetMolFrags(m,asMols=True,sanitizeFrags=True)])
RC=readxyz('ts/ts_0008/jobs/declaration_0002/candidate_opt/optimized_seed.xyz')
print('reactant built atoms',len(RC))
benzo=set(range(11,25))  # 1-based 11..24 = benzaldehyde
rc27=[a for i,a in enumerate(RC,1) if i not in benzo]
bza =[a for i,a in enumerate(RC,1) if i in benzo]
writexyz(out+'/RC_27_start.xyz', rc27, 'E1a RC subsystem (proline+acetone, 27 atoms) = built reactant minus benzaldehyde atoms 11-24; source ts/ts_0008/jobs/declaration_0002/candidate_opt/optimized_seed.xyz')
writexyz(out+'/BZA_14_start.xyz', bza, 'E1 spectator benzaldehyde (14 atoms) extracted from built reactant atoms 11-24; source optimized_seed.xyz')
check(out+'/RC_27_start.xyz','RC_27')
check(out+'/BZA_14_start.xyz','BZA_14')
L=open('ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log').read().split(chr(10))
sym={1:'H',6:'C',7:'N',8:'O'}
bl=[k for k,l in enumerate(L) if 'Input orientation' in l]
b=bl[-1]; g=[]
for l in L[b+5:b+50]:
    p=l.split()
    if len(p)==6 and p[0].isdigit(): g.append([sym[int(p[1])],p[3],p[4],p[5]])
    elif g: break
print('ts_opt converged frame atoms',len(g))
int27=[a for i,a in enumerate(g,1) if i not in benzo]
writexyz(out+'/INT1_27_start.xyz', int27, 'E1b/E1a carbinolamine (zwitterionic adduct, 27 atoms) = ts_opt converged frame minus benzaldehyde atoms 11-24; source ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log Input orientation block L%d'%(b+1))
check(out+'/INT1_27_start.xyz','INT1_27')