import math, sys
Z={1:"H",6:"C",8:"O",11:"Na"}
def blocks(path):
    L=open(path).read().splitlines(); out=[]; i=0
    while i<len(L):
        s=L[i].strip()
        if s.startswith("Standard orientation:") or s.startswith("Input orientation:"):
            kind="std" if s.startswith("Standard") else "inp"
            k=i+5; at=[]
            while k<len(L) and not L[k].strip().startswith("-----"):
                f=L[k].split()
                if len(f)>=6: at.append((Z.get(int(f[1]),"X"), float(f[3]), float(f[4]), float(f[5])))
                k+=1
            out.append((kind,i+1,at)); i=k
        else: i+=1
    return out
def v(a,b): return (b[1]-a[1], b[2]-a[2], b[3]-a[3])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def nrm(a): return math.sqrt(dot(a,a))
def dist(a,i,j): return nrm(v(a[i],a[j]))
def ang(a,i,j,k):
    u=v(a[j],a[i]); w=v(a[j],a[k]); return math.degrees(math.acos(max(-1,min(1,dot(u,w)/(nrm(u)*nrm(w))))))
def dih(a,i,j,k,l):
    b1=v(a[i],a[j]); b2=v(a[j],a[k]); b3=v(a[k],a[l]); n1=cross(b1,b2); n2=cross(b2,b3); m=[x/nrm(b2) for x in cross(n1,b2)]
    return math.degrees(math.atan2(dot(m,n2), dot(n1,n2)))
def met(a):
    return "d(O1..C4)=%.3f Na-O1=%.3f D_Me=%.2f D_OH=%.2f aNaO1H6=%.2f BD=%.2f C4-O1=%.3f C4=O5=%.3f O3-C4=%.3f"%(dist(a,1,5),dist(a,0,1),dih(a,7,3,4,5),dih(a,0,1,2,10),ang(a,0,1,2),ang(a,1,5,6),dist(a,5,1),dist(a,5,6),dist(a,4,5))
p=sys.argv[1]
o=blocks(p)
inps=[x for x in o if x[0]=="inp"]; stds=[x for x in o if x[0]=="std"]
print("total inp blocks %d, std blocks %d"%(len(inps),len(stds)))
li=inps[-1]; ls=stds[-1]
print("last INPUT orientation at L%d: order %s"%(li[1], ",".join(a[0] for a in li[2])))
print("  INPUT : "+met(li[2]))
print("last STD orientation at L%d: order %s"%(ls[1], ",".join(a[0] for a in ls[2])))
print("  STD   : "+met(ls[2]))
print("XYZ_BEGIN")
print(len(li[2]))
print("job1018 last frame (Input orientation L%d, input order Na,O,H,C,O,C,O,H,H,H,H) - failure frame, NOT an optimised structure"%li[1])
for a in li[2]: print("%-2s %14.8f %14.8f %14.8f"%(a[0],a[1],a[2],a[3]))
print("XYZ_END")