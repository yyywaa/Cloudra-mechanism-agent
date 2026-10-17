import numpy as np
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log"
L=open(LOG).read().splitlines()
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[];el=[]
        while k<len(L) and len(co)<41:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1]));co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==41: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
li,X,el=blocks[-1]
print("last orientation block L%d atoms %d C%d H%d N%d O%d" % (li,len(el),el.count(6),el.count(1),el.count(7),el.count(8)))
d=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
for nm,(a,b) in [("C2-N4",(2,4)),("C2-O25",(2,25)),("N4-H26",(4,26)),("O25-H26",(25,26)),("O10-H27",(10,27)),("N4-H27",(4,27))]:
    print("  %-8s %7.4f" % (nm,d(a,b)))
Z={1:"H",6:"C",7:"N",8:"O"}
heavy=[k for k in range(1,42) if el[k-1]!=1]
for a in (26,27):
    s=sorted(((d(a,k),k) for k in heavy))[:2]
    print("  H%d nearest: %s%d %.4f (2nd %s%d %.4f)" % (a,Z[el[s[0][1]-1]],s[0][1],s[0][0],Z[el[s[1][1]-1]],s[1][1],s[1][0]))
