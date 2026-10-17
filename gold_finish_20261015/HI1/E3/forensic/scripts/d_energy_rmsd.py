#!/usr/bin/env python3
"""Part D: exact energy differences and fragment-wise RMSD."""
import math, numpy as np, json
from rdkit import Chem, RDLogger
from rdkit.Chem import rdDetermineBonds
RDLogger.DisableLog("rdApp.*")
ROOT="/home/ly/Cloudra-mechanism-agent"
RUN=ROOT+"/ts/ts_0011"; JOB=RUN+"/jobs/declaration_0004"; E3=ROOT+"/gold_finish_20261015/HI1/E3"
N=41; H2K=627.5094740631; Z={1:"H",6:"C",7:"N",8:"O"}
def rd(p):
    with open(p,errors="replace") as f: return f.read().splitlines()
def xyz(p):
    L=rd(p); n=int(L[0].split()[0])
    return [(q.split()[0],*map(float,q.split()[1:4])) for q in L[2:2+n]]
def frame(path, which=-1):
    L=rd(path); idx=[i for i,s in enumerate(L,1) if s.strip().startswith(("Standard orientation:","Input orientation:"))]
    i=idx[which]; a=[]; k=i+3
    while len(a)<N:
        p=L[k-1].split()
        if len(p)==6 and p[0].isdigit(): a.append((Z[int(p[1])],float(p[3]),float(p[4]),float(p[5]))); k+=1
        else: k+=1
    return a, i
def kab(A,B,sel=None):
    if sel: A=[A[i] for i in sel]; B=[B[i] for i in sel]
    A=np.array([x[1:] for x in A]); B=np.array([x[1:] for x in B])
    Ac=A-A.mean(0); Bc=B-B.mean(0)
    U,S,Vt=np.linalg.svd(Ac.T@Bc); d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T
    return float(np.sqrt(((R@Ac.T).T-Bc)**2).sum(1).mean())
F={}
F["I2"]=xyz(E3+"/runs/I2_optfreq/I2_min_v5.xyz")
F["P"]=xyz(E3+"/prep/P_1061_optframe.xyz")
F["prod_opt"],l1=frame(JOB+"/product_opt/product_opt.log")
F["react_opt"],l2=frame(JOB+"/reactant_opt/reactant_opt.log")
F["ts"],l3=frame(JOB+"/ts_opt/refine.log")
print("frame lines: prod_opt hdr L%d ; react_opt hdr L%d ; ts hdr L%d"%(l1,l2,l3))
# fragment membership of the water (O25,H26,H27) vs rest
water=[24,25,26]
rest=[i for i in range(N) if i not in water]
for a,b in [("prod_opt","I2"),("react_opt","I2"),("prod_opt","P"),("ts","I2")]:
    print("RMSD(%s,%s): all=%.4f  heavy-part(38 atoms)=%.4f  water(25,26,27)=%.4f"%(a,b,
        kab(F[a],F[b]),kab(F[a],F[b],rest),kab(F[a],F[b],water)))
E={"I2":-939.320655479,"TS":-939.319094501,"P":-939.319540184,
   "prod_opt":-939.320655496,"react_opt":-939.320655386,"freq1029":-939.319094501,
   "irc_fwd1":-939.319097479,"irc_rev1":-939.319097211,"irc_init":-939.319094501,
   "prod_freq":-939.320655496,"react_freq":-939.320655386,"P_step2":-939.319540184}
print("\nreference I2 = %.9f Eh"%E["I2"])
for k in E:
    if k=="I2": continue
    print("  dE(%-10s - I2) = %+.9f Eh = %+7.2f kcal/mol"%(k,E[k]-E["I2"],(E[k]-E["I2"])*H2K))
print("  dE(TS - P)      = %+.9f Eh = %+7.2f kcal/mol"%((E["TS"]-E["P"]),(E["TS"]-E["P"])*H2K))
print("  dE(P - prod_opt)= %+.9f Eh = %+7.2f kcal/mol"%((E["P"]-E["prod_opt"]),(E["P"]-E["prod_opt"])*H2K))
