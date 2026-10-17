import numpy as np, sys
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
pt=int(sys.argv[1]) if len(sys.argv)>1 else 8
L=open(LOG).read().splitlines()
N=41
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[]
        while k<len(L) and len(co)<N:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit(): co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==N: blocks.append((i+1,np.array(co)))
        i=k
    else: i+=1
mark=[i+1 for i,ln in enumerate(L) if "Step number" in ln and ("on scan point %5d out of" % pt) in ln]
if not mark: mark=[i+1 for i,ln in enumerate(L) if "Step number" in ln and ("scan point %d out of" % pt) in ln]
d=lambda X,a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
print("scan point %d : %d step markers" % (pt,len(mark)))
for s,ml in enumerate(mark,1):
    cand=[b for b in blocks if b[0]<ml]
    if not cand: continue
    h,X=cand[-1]
    print("  step %2d  stepL%-6d hdrL%-6d R(2,4)=%7.4f R(25,26)=%7.4f R(4,26)=%7.4f R(2,25)=%7.4f R(2,26)=%7.4f" % (s,ml,h,d(X,2,4),d(X,25,26),d(X,4,26),d(X,2,25),d(X,2,26)))
