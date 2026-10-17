import numpy as np, itertools
p="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192.gjf"
L=open(p).read().splitlines()
print("line4 route:", L[3])
# find geometry start: after blank line following route
i=[k for k,l in enumerate(L) if l.strip()==""][1]+1
# skip title/charge lines: title line, blank, charge
# locate first atom line (starts with element symbol)
start=None
for k in range(i, len(L)):
    t=L[k].split()
    if len(t)==4 and t[0] in ("C","N","O","H"):
        start=k; break
geo=[]; els=[]
for k in range(start, start+27):
    t=L[k].split(); els.append(t[0]); geo.append([float(t[1]),float(t[2]),float(t[3])])
X=np.array(geo)
print("atoms",len(X),"elements",els[:6],"...")
R=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
for a,b in [(2,18),(2,3),(18,27),(3,27),(2,4)]:
    print("  R(%2d-%2d)=%.4f"%(a,b,R(a,b)))
cov={'H':0.31,'C':0.76,'N':0.71,'O':0.66}
pr=[]
for a,b in itertools.combinations(range(1,28),2):
    d=R(a,b); pr.append((d,a,b,d<1.25*(cov[els[a-1]]+cov[els[b-1]])))
pr.sort()
print("minsep %.4f pair %d-%d bonded=%s"%(pr[0][0],pr[0][1],pr[0][2],pr[0][3]))
nb=[x for x in pr if not x[3]][:3]
print("tightest nonbonded:", [(round(d,4),a,b) for d,a,b,_ in nb])
