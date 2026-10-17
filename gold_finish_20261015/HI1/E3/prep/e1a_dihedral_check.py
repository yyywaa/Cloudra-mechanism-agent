import numpy as np, re, math
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log"
L=open(LOG).read().splitlines()
N=27
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[];el=[]
        while k<len(L) and len(co)<N:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1]));co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==N: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
opt=[i+1 for i,ln in enumerate(L) if "Optimization completed." in ln]
Z={1:"H",6:"C",7:"N",8:"O"}
el=blocks[0][2]
print("orientation blocks:",len(blocks),"| converged points:",len(opt),"| atoms:",len(el),"C%d H%d N%d O%d"%(el.count(6),el.count(1),el.count(7),el.count(8)))
print("labels 2,3,14,18 ->",[Z[el[k-1]]+str(k) for k in (2,3,14,18)])
def dih(p0,p1,p2,p3):
    b0=p0-p1; b1=p2-p1; b2=p3-p2
    b1/=np.linalg.norm(b1)
    v=b0-np.dot(b0,b1)*b1; w=b2-np.dot(b2,b1)*b1
    x=np.dot(v,w); y=np.dot(np.cross(b1,v),w)
    return math.degrees(math.atan2(y,x))
pts=[]
for oc in opt:
    cand=[b for b in blocks if b[0]<oc]
    if not cand: continue
    b=cand[-1]
    pts.append((oc,b[0],dih(b[1][2],b[1][1],b[1][17],b[1][13])))
print()
print("O3-C2-N18-C14 dihedral (signed, degrees) at each converged point:")
for n,(oc,hdr,t) in enumerate(pts,1):
    print("  pt%-2d convL%-6d hdrL%-6d tau = %+8.3f  |tau| = %7.3f" % (n,oc,hdr,t,abs(t)))
if len(pts)>=2:
    a=pts[0][2]; b=pts[-1][2]
    d=((b-a+180.0)%360.0)-180.0
    print()
    print("first->last : tau %+8.3f -> %+8.3f ; signed change %+8.3f ; |tau| %7.3f -> %7.3f" % (a,b,d,abs(a),abs(b)))
    print("shortest angular difference |Delta tau| = %.3f deg" % abs(d))
print()
print("all converged points' SCF energies (for context):")
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
for n,(oc,hdr,t) in enumerate(pts,1):
    e=[(l,en) for l,en in scf if l<oc][-1]
    print("  pt%-2d E=%.9f (L%d)" % (n,e[1],e[0]))
