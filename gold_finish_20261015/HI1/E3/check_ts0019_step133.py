import numpy as np, itertools
log="/home/ly/Cloudra-mechanism-agent/ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log"
L=open(log,errors='ignore').read().splitlines()
idx=[i for i,l in enumerate(L) if 'Standard orientation' in l or 'Input orientation' in l]
start=idx[-1]
dash=[i for i in range(start,start+20) if L[i].strip().startswith('---')]
hdr=dash[1]
els=[];X=[]
k=hdr+1
while len(X)<41 and k<len(L):
    p=L[k].split()
    if len(p)==6:
        els.append(p[1]); X.append([float(p[3]),float(p[4]),float(p[5])])
    k+=1
print("block header line",start+1,"data",hdr+1,"->",hdr+len(X),"count",len(X))
X=np.array(X)
R=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
for a,b in [(2,4),(2,25),(4,26),(26,25),(10,27),(9,10),(9,11),(2,26)]:
    print("  R(%2d-%2d)=%.4f"%(a,b,R(a,b)))
cov={'1':0.31,'6':0.76,'7':0.71,'8':0.66}
pr=sorted((R(a,b),a,b,R(a,b)<1.25*(cov[els[a-1]]+cov[els[b-1]])) for a,b in itertools.combinations(range(1,42),2))
print("global sep min %.4f %d-%d bonded=%s"%(pr[0][0],pr[0][1],pr[0][2],pr[0][3]))
nb=[x for x in pr if not x[3]][:3]
print("tightest nonbonded:",[(round(d,4),a,b) for d,a,b,_ in nb])
E=-939.319785350; Ep=-939.319540184; Eh=-939.312626605
print("dE vs P = %.6f Ha = %.4f kcal"%(E-Ep,(E-Ep)*627.5095))
print("dE vs 1028 = %.6f Ha = %.4f kcal"%(E-Eh,(E-Eh)*627.5095))
