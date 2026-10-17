import math, sys
Z={1:"H",6:"C",8:"O",11:"Na"}
def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0].split()[0]); out=[]
    for ln in L[2:2+n]:
        f=ln.split(); out.append((f[0], float(f[1]), float(f[2]), float(f[3])))
    return out
def read_gjf(p):
    out=[]
    for ln in open(p).read().splitlines():
        f=ln.split()
        if len(f)==4 and f[0] in ("Na","C","O","H"): out.append((f[0], float(f[1]), float(f[2]), float(f[3])))
    return out
def orient_blocks(path):
    L=open(path).read().splitlines(); out=[]; i=0
    while i<len(L):
        s=L[i].strip()
        if s.startswith("Standard orientation:") or s.startswith("Input orientation:"):
            kind="std" if s.startswith("Standard") else "inp"; k=i+5; at=[]
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
logp, gjfp, d230p, rcp = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
o=orient_blocks(logp); inps=[x for x in o if x[0]=="inp"]
gjf=read_gjf(gjfp); first=inps[0][2]; last=inps[-1][2]
print("n inp blocks=%d ; first at L%d ; last at L%d"%(len(inps),inps[0][1],inps[-1][1]))
print("gjf order    :", ",".join(a[0] for a in gjf))
print("1st INP order:", ",".join(a[0] for a in first))
dmax=max(math.dist(gjf[i][1:], first[i][1:]) for i in range(len(gjf)))
print("INDEX-SAFETY: max |first INPUT orientation - gjf input coordinate| = %.6f A over %d atoms"%(dmax,len(gjf)))
a=read_xyz(d230p); b=read_gjf(gjfp)
print("d230 order   :", ",".join(x[0] for x in a))
c=read_gjf(sys.argv[5])
print("decl0005 gjf :", ",".join(x[0] for x in c))
print("BIND CHECK: max |decl0005 gjf coords - d230 xyz| = %.6f A"%(max(math.dist(c[i][1:], a[i][1:]) for i in range(11))))
rc=read_xyz(rcp)
print("%-28s %-10s %-10s %-8s" % ("quantity","RC ref","job1018 last","delta"))
def row(name,f): print("%-28s %-10.3f %-10.3f %-8.3f"%(name,f(rc),f(last),f(last)-f(rc)))
row("d(O1..C4)  [0-1..5]", lambda x: dist(x,1,5))
row("Na-O1      [0-1]", lambda x: dist(x,0,1))
row("O1-H6      [1-2]", lambda x: dist(x,1,2))
row("C4-O5      [5-6]", lambda x: dist(x,5,6))
row("C4-O3      [4-5]", lambda x: dist(x,4,5))
row("D_Me(8,4,5,6) [7,3,4,5]", lambda x: dih(x,7,3,4,5))
row("D_OH(1,2,3,11) [0,1,2,10]", lambda x: dih(x,0,1,2,10))
row("aNa-O1-H6  [0,1,2]", lambda x: ang(x,0,1,2))
row("BD O1C4O5  [1,5,6]", lambda x: ang(x,1,5,6))
print("H6 nearest heavy atom in last frame: ", min(((dist(last,2,j), j) for j in (0,3,4,5,6)), key=lambda t:t[0]))
print("XYZ_BEGIN")
print(len(last))
print("job1018 last frame (Input orientation L%d, input order Na,O,H,C,O,C,O,H,H,H,H) - failed ts_opt frame, NOT an optimised structure"%inps[-1][1])
for x in last: print("%-2s %14.8f %14.8f %14.8f"%(x[0],x[1],x[2],x[3]))
print("XYZ_END")