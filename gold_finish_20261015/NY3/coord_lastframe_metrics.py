import math, sys, os
Z={1:"H",6:"C",8:"O",11:"Na"}
def read_last_orient(p):
    L=open(p).read().splitlines()
    start=None
    for i,ln in enumerate(L):
        if ln.strip().startswith("Standard orientation:") or ln.strip().startswith("Input orientation:"):
            start=i
    if start is None: return None,None
    # block: start, ----, center, ----, header, atoms..., ----, then blank
    k=start+5
    at=[]
    while k<len(L) and not L[k].strip().startswith("-----"):
        f=L[k].split()
        if len(f)>=6: at.append((Z.get(int(f[1]),"X"), float(f[3]), float(f[4]), float(f[5])))
        k+=1
    return at,start+1
def v(a,b): return (b[1]-a[1], b[2]-a[2], b[3]-a[3])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a,a))
def dist(a,i,j): return norm(v(a[i],a[j]))
def angle(a,i,j,k):
    u=v(a[j],a[i]); w=v(a[j],a[k]); return math.degrees(math.acos(max(-1,min(1,dot(u,w)/(norm(u)*norm(w))))))
def dih(a,i,j,k,l):
    b1=v(a[i],a[j]); b2=v(a[j],a[k]); b3=v(a[k],a[l]); n1=cross(b1,b2); n2=cross(b2,b3); m=[x/norm(b2) for x in cross(n1,b2)]
    return math.degrees(math.atan2(dot(m,n2), dot(n1,n2)))
rc=read_last_orient("/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/E1/rc_dft_min_working_order.xyz") if False else None
import json
def metrics(a):
    return dict(d_O1C4=dist(a,1,5), Na_O1=dist(a,0,1), D_Me=dih(a,7,3,4,5), D_OH=dih(a,0,1,2,10), aNaO1H6=angle(a,0,1,2), BD=angle(a,1,5,6), C4O1=dist(a,5,1), C4O5=dist(a,5,6), O3C4=dist(a,4,5))
p=sys.argv[1]
at,ln=read_last_orient(p)
if at is None: print("no orientation block"); sys.exit()
print("last orientation block at L%d, %d atoms, order %s"%(ln,len(at),",".join(x[0] for x in at)))
m=metrics(at)
print("d(O1...C4)=%.3f  Na-O1=%.3f  D_Me=%.2f  D_OH=%.2f  aNaO1H6=%.2f  BD=%.2f  C4-O1=%.3f  C4=O5=%.3f  O3-C4=%.3f"%(
  m["d_O1C4"],m["Na_O1"],m["D_Me"],m["D_OH"],m["aNaO1H6"],m["BD"],m["C4O1"],m["C4O5"],m["O3C4"]))
print("RC ref: d 2.803  Na-O1 2.093  D_Me -60.35  D_OH -152.44  aNaO1H6 145.38  BD 96.06")