
import math
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.gjf"
L=open(p).read().splitlines()
print("lines", len(L))
# geometry: after charge line
i=[k for k,l in enumerate(L) if l.strip()=="0 1"][0]
atoms=[]; k=i+1
while k<len(L) and len(L[k].split())==4:
    e,x,y,z=L[k].split(); atoms.append((e,float(x),float(y),float(z))); k+=1
print("natoms", len(atoms), "elements", "".join(a[0] for a in atoms))
def d(a,b): return math.dist(atoms[a-1][1:], atoms[b-1][1:])
print("R(1,29)=%.4f R(28,24)=%.4f R(11,24)=%.4f" % (d(1,29), d(28,24), d(11,24)))
seed="/home/ly/Cloudra-mechanism-agent/ts/ts_0009/build/input_0004/reactant/seed.xyz"
S=[l.split() for l in open(seed).read().splitlines()[2:] if len(l.split())==4]
print("seed natoms", len(S), "order_eq", [s[0] for s in S]==[a[0] for a in atoms])
mx=max(math.dist([float(c) for c in S[i][1:]], atoms[i][1:]) for i in range(len(S)))
print("max|d| vs seed (not expected 0; cont1 starts from pt8) =", round(mx,4))
