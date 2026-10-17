import numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors
L=open('ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log').read().split(chr(10))
sym={1:'H',6:'C',7:'N',8:'O'}
bl=[k for k,l in enumerate(L) if 'Input orientation' in l]
b=bl[-1]; g=[]
for l in L[b+5:b+50]:
    p=l.split()
    if len(p)==6 and p[0].isdigit(): g.append((sym[int(p[1])],float(p[3]),float(p[4]),float(p[5])))
    elif g: break
print('last Input orientation block L%d'%(b+1))
P=np.array([[x[1],x[2],x[3]] for x in g])
for a,bb,lab in [(2,3,'C2-O4'),(4,10,'C3-H22'),(32,41,'N20-H21'),(2,4,'C2-C3'),(2,32,'C2..N20'),(3,41,'O4..H21'),(3,10,'O4..H22')]:
    print('  %-8s %2d-%-2d %.3f'%(lab,a,bb,float(np.linalg.norm(P[a-1]-P[bb-1]))))
open('/tmp/tsfin.xyz','w').write('%d'%len(g)+chr(10)+'ts_opt converged frame'+chr(10)+chr(10).join('%s %.6f %.6f %.6f'%x for x in g))
m=Chem.RWMol(Chem.MolFromXYZFile('/tmp/tsfin.xyz')); rdDetermineBonds.DetermineBonds(m,charge=0); m=m.GetMol()
Chem.AssignStereochemistryFrom3D(m); Chem.AssignCIPLabels(m)
print('formula',rdMolDescriptors.CalcMolFormula(m),'frags',len(Chem.GetMolFrags(m)))
print('frags:',[Chem.MolToSmiles(f) for f in Chem.GetMolFrags(m,asMols=True,sanitizeFrags=True)])
print('CIP:',[(a.GetIdx()+1,a.GetSymbol(),a.GetPropsAsDict().get('_CIPCode')) for a in m.GetAtoms() if a.HasProp('_CIPCode')])
E=-939.242869284
print('E - job907 = %.6f Eh = %.2f kcal/mol'%(E+939.308829219,(E+939.308829219)*627.509474))
print('E - job924 = %.2f kcal/mol'%((E+939.308218263)*627.509474))