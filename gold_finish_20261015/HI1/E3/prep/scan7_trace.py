import numpy as np, re, sys
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
start=None
for i,l in enumerate(L):
    if "on scan point     7 out of" in l:
        start=i; break
print("first scan-point-7 step line L%d: %s" % (start+1, L[start].strip()))
d=lambda X,a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
i=start
out=[]
while i < len(L):
    if "Step number" in L[i] and "on scan point     7 out of" in L[i]:
        step=L[i].strip()
        # find next orientation block
        k=i+1
        while k < len(L) and "Input orientation:" not in L[k] and "Standard orientation:" not in L[k]:
            k+=1
        if k>=len(L): break
        j=k+1; co=[]
        while j<len(L) and len(co)<41:
            p=L[j].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                co.append([float(p[3]),float(p[4]),float(p[5])])
            j+=1
        if len(co)==41:
            X=np.array(co)
            out.append((i+1,k+1,d(X,2,4),d(X,25,26),d(X,4,26),d(X,10,27)))
    i+=1
for r in out:
    print("stepL%-6d hdrL%-6d R(2,4)=%7.4f R(25,26)=%7.4f R(4,26)=%7.4f R(10,27)=%7.4f" % r)
print("blocks:", len(out))
