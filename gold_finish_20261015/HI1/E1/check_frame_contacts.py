#!/usr/bin/env python3
"""Generic contact report for a 27-atom candidate frame: element sequence check against the
reference (E1A_TS_candidate_job1055.xyz) and the tightest contacts. Element-based only."""
import sys, itertools, numpy as np
def rd(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0])
    els=[l.split()[0] for l in L[2:2+n]]
    X=np.array([[float(x) for x in l.split()[1:4]] for l in L[2:2+n]])
    return els,X
ref="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_TS_candidate_job1055.xyz"
eR,_=rd(ref)
e,X=rd(sys.argv[1])
print("file:",sys.argv[1],"natoms:",len(e),"element sequence == reference(27):", e==eR)
if e!=eR:
    print("  file  :", " ".join(e))
    print("  ref   :", " ".join(eR))
C2,O3,C3,H22,N18,H21=1,2,3,9,17,26
def d(i,j): return float(np.linalg.norm(X[i]-X[j]))
if e==eR:
    print("  R(C2-N18)=%.4f  R(N18-H21)=%.4f  R(C2-O3)=%.4f  R(O3-H21)=%.4f  R(C3-H22)=%.4f" % (d(C2,N18),d(N18,H21),d(C2,O3),d(O3,H21),d(C3,H22)))
pairs=sorted(((float(np.linalg.norm(X[i]-X[j])),i+1,j+1,e[i],e[j]) for i,j in itertools.combinations(range(len(e)),2)))
print("  tightest 5 contacts:")
for p in pairs[:5]:
    print("    %.4f A  atom %d(%s) - atom %d(%s)" % (p[0],p[1],p[3],p[2],p[4]))
