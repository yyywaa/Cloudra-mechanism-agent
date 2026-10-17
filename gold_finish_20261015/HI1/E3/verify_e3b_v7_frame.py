import numpy as np, itertools, hashlib
base="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/prep/"
def load(p):
    L=open(base+p).read().splitlines()
    n=int(L[0].split()[0]); els=[]; X=[]
    for i in range(2,2+n):
        t=L[i].split(); els.append(t[0]); X.append([float(t[1]),float(t[2]),float(t[3])])
    return els, np.array(X)
e1,X1=load("hemiaminal_1028_lastframe.xyz")
e2,X2=load("e3b_guess_formal_v7/E3B_TS_GUESS_v7_c2n4_2.200.xyz")
print("atoms", len(e1), len(e2), "element order identical:", e1==e2)
R=lambda X,a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
print("--- v7 (atom indices 1-based per file order)")
for a,b in [(2,4),(2,25),(4,26),(26,25),(2,26),(10,27),(9,10),(9,11),(25,27),(24,28)]:
    print("  R(%2d-%2d) v7=%.4f  1028=%.4f"%(a,b,R(X2,a,b),R(X1,a,b)))
# minsep and tightest 3 nonbonded
cov={'H':0.31,'C':0.76,'N':0.71,'O':0.66}
pairs=[]
for a,b in itertools.combinations(range(1,len(e2)+1),2):
    d=R(X2,a,b); bonded = d < 1.25*(cov[e2[a-1]]+cov[e2[b-1]])
    pairs.append((d,a,b,bonded))
nb=[p for p in pairs if not p[3]]
nb.sort()
allp=sorted(pairs)
print("global minsep %.4f pair %d-%d bonded=%s"%(allp[0][0],allp[0][1],allp[0][2],allp[0][3]))
print("tightest nonbonded:", [(round(d,4),a,b) for d,a,b,_ in nb[:5]])
print("any nonbonded <1.20:", [ (a,b,round(d,3)) for d,a,b,_ in nb if d<1.20 ])
# bond length drift outside reaction centre
changed=[]
for d,a,b,_ in [p for p in pairs if p[3]]:
    d1=R(X1,a,b)
    if abs(d-d1)>0.01: changed.append((a,b,round(d1,4),round(d,4),round(abs(d-d1),4)))
print("bonded pairs with |dR|>0.01 vs 1028:", changed)
# H26 geometry
def ang(a,b,c):
    v1=X2[a-1]-X2[b-1]; v2=X2[c-1]-X2[b-1]
    return float(np.degrees(np.arccos(np.dot(v1,v2)/np.linalg.norm(v1)/np.linalg.norm(v2))))
print("angle C2-N4-H26 in v7 = %.2f deg"%ang(2,4,26))
nn=sorted(((R(X2,26,a),a,e2[a-1]) for a in range(1,len(e2)+1) if a!=26))[:3]
print("nearest to H26:", [(round(d,4),a,el) for d,a,el in nn])
