import numpy as np
p="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/path/input_0001/provided.xyz"
L=open(p).read().splitlines(); n=int(L[0].split()[0])
els=[];X=[]
for i in range(2,2+n):
    t=L[i].split(); els.append(t[0]); X.append([float(t[1]),float(t[2]),float(t[3])])
X=np.array(X); R=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
print("n",n,"elements",els[:5])
for a,b in [(2,4),(2,25),(4,26),(26,25),(10,27),(2,26)]:
    print("  R(%2d-%2d)=%.4f"%(a,b,R(a,b)))
