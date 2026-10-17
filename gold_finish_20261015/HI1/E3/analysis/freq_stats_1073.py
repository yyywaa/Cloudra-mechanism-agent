
import re, numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi, rdMolDescriptors
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
RUNS="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs"
LOG=RUNS+"/build_seed_product_optfreq.log"; PLOG=RUNS+"/P_e3b/P_optfreq.log"
PT=Chem.GetPeriodicTable()
def L(p): return open(p).read().splitlines()
def frame(lines,h):
    d=[j for j in range(h,h+10) if lines[j].strip().startswith('-----')]
    a=[]; j=d[1]+1
    while not lines[j].strip().startswith('-----'):
        p=lines[j].split(); a.append((int(p[1]),float(p[3]),float(p[4]),float(p[5]))); j+=1
    return a,d[1]+1,j
def xyz(a,t):
    return "\n".join([str(len(a)),t]+["%-3s %14.8f %14.8f %14.8f"%(PT.GetElementSymbol(z),x,y,zz) for z,x,y,zz in a])+"\n"
def mol(a):
    m=Chem.MolFromXYZBlock(xyz(a,"f")); rdDetermineBonds.DetermineBonds(m,charge=0); return m
lg=L(LOG); hl=[i for i,l in enumerate(lg) if 'Standard orientation' in l]
af,ab_s,ab_e=frame(lg,hl[-1]); pl=L(PLOG); hp=[i for i,l in enumerate(pl) if 'Standard orientation' in l]
pf,pb_s,pb_e=frame(pl,hp[-1])
open("1073_freq_final_frame.xyz","w").write(xyz(af,"1073 freq final frame; build_seed_product_optfreq.log L%d-L%d, 41 atoms, 1073 log order"%(ab_s,ab_e)))
open("P_1061_last_frame.xyz","w").write(xyz(pf,"P job1061 last frame; P_optfreq.log L%d-L%d, 41 atoms, P/E3 log order"%(pb_s,pb_e)))
print("xyz written; atoms",len(af),len(pf))
print("1073 elem seq:", "".join(PT.GetElementSymbol(a[0]) for a in af))
print("P    elem seq:", "".join(PT.GetElementSymbol(a[0]) for a in pf))
mA=mol(af); mP=mol(pf)
# first freq group with reduced masses / frc consts
i0=[i for i,l in enumerate(lg) if 'Frequencies --' in l][0]
for k in range(i0,i0+3): print("L%d: %s"%(k+1,lg[k].rstrip()))
freqs=[]
for i,l in enumerate(lg):
    if 'Frequencies --' in l: freqs+=[float(x) for x in re.findall(r'-?\d+\.\d+',l.split('--',1)[1])]
srt=sorted(freqs)
print("lowest 8:",["%.4f"%x for x in srt[:8]])
print("highest 8:",["%.4f"%x for x in srt[-8:]])
# mapping 1073 -> P (heavy subgraph, choose min heavy Kabsch among matches)
A=np.array([[x,y,z] for _,x,y,z in af]); B=np.array([[x,y,z] for _,x,y,z in pf])
def heavy(m): return Chem.RemoveHs(m)
def kabsch(P,Q):
    Pc=P-P.mean(0); Qc=Q-Q.mean(0)
    H=Pc.T@Qc; U,S,Vt=np.linalg.svd(H); d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T
    Pr=(R@Pc.T).T
    dev=np.linalg.norm(Pr-Qc,axis=1)
    return float(np.sqrt((dev**2).mean())), float(dev.max()), dev
hA=heavy(mA); hP=heavy(mP)
HA=[a.GetIdx() for a in hA.GetAtoms()]; HP=[a.GetIdx() for a in hP.GetAtoms()]
matches=hA.GetSubstructMatches(hP,uniquify=False,maxMatches=5000)
print("heavy-graph matches 1073->P:",len(matches))
best=None
for mt in matches:  # mt[i] = idx in hP for query atom i of hA
    if sorted(mt)!=list(range(len(HP))): continue
    rms,mx,dev=kabsch(A[HA],B[[HP[k] for k in mt]])
    if best is None or rms<best[0]: best=(rms,mx,mt,HA,HP,dev)
rms,mx,mt,HA,HP,dev=best
print("best heavy Kabsch rms=%.4f max=%.4f"%(rms,mx))
# worst atom
wi=int(np.argmax(dev)); print("worst heavy pair: 1073 atom %d (%s) <-> P atom %d (%s) dev=%.4f"%(HA[wi]+1,PT.GetElementSymbol(af[HA[wi]][0]),HP[mt[wi]]+1,PT.GetElementSymbol(pf[HP[mt[wi]]][0]),dev[wi]))
# full mapping incl H: heavy map then nearest H assignment by graph
map_all={}
for qi,ti in zip(HA,mt): map_all[qi]=HP[ti]
# hydrogens: match by bonded heavy neighbor
unA=[a.GetIdx() for a in mA.GetAtoms() if a.GetAtomicNum()==1]; unP=[a.GetIdx() for a in mP.GetAtoms() if a.GetAtomicNum()==1]
for ha in unA:
    nb=[n.GetIdx() for n in mA.GetAtomWithIdx(ha).GetNeighbors()][0]
    cand=[x for x in unP if x not in map_all.values() and [n.GetIdx() for n in mP.GetAtomWithIdx(x).GetNeighbors()]==[map_all[nb]]]
    if len(cand)!=1:
        # nearest by distance to mapped heavy
        tgt=B[map_all[nb]]; cand=[min([x for x in unP if x not in map_all.values()], key=lambda x: np.linalg.norm(B[x]-tgt))]
    map_all[ha]=cand[0]
print("full mapping 41 pairs complete:",len(map_all)==41,sorted(map_all.values())==list(range(41)))
print("--- distances in 1073 order and mapped P-order partner ---")
inv={v:k for k,v in map_all.items()}
def dv(X,i,j): return float(np.linalg.norm(X[i]-X[j]))
for (i,j,lab) in [(2,4,'C2-N4?'),(2,25,'C2-O?'),(4,26,'?'),(25,26,'?')]:
    print("  1073 R(%d,%d)=%.4f"%(i,j,dv(A,i-1,j-1)))
# report the four key bond pattern from perceived graphs
print("1073 graph bonds touching C2 (atom2):",[(b.GetOtherAtomIdx(1),PT.GetElementSymbol(mA.GetAtomWithIdx(b.GetOtherAtomIdx(1)).GetAtomicNum())) for b in mA.GetAtomWithIdx(1).GetBonds()])
print("1073 N atom idx:",[a.GetIdx()+1 for a in mA.GetAtoms() if a.GetAtomicNum()==7], "its H:",[(n.GetIdx()+1) for a in mA.GetAtoms() if a.GetAtomicNum()==7 for n in a.GetNeighbors()])
print("1073 O atoms idx:",[a.GetIdx()+1 for a in mA.GetAtoms() if a.GetAtomicNum()==8])
# fragments
fr=Chem.GetMolFrags(mA,asMols=False)
print("frag atom sets (1073 order):",[[i+1 for i in f] for f in fr])
for f in fr:
    sub=A[list(f)]; others=[i for i in range(41) if i not in f]
    d=np.linalg.norm(sub[:,None,:]-A[others][None,:,:],axis=2)
    k=np.unravel_index(np.argmin(d),d.shape)
    print("   min dist from frag -> rest: %.4f between 1073 atom %d and %d"%(d.min(),list(f)[k[0]]+1,others[k[1]]+1))
print("InChIKey 1073:",inchi.InchiToInchiKey(inchi.MolToInchi(mA)))
print("InChIKey P   :",inchi.InchiToInchiKey(inchi.MolToInchi(mP)))
