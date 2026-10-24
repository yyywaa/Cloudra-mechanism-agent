import math
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0004/reactant_opt/reactant_opt.log"
L=open(LOG).read().splitlines()
EL={8:'O',1:'H',6:'C',7:'N'}
idxs=[i for i,l in enumerate(L) if "Standard orientation:" in l or "Input orientation:" in l]
def block(i):
    co=[];k=i+5
    while not L[k].strip().startswith("-----"):
        f=L[k].split()
        if len(f)>=6: co.append((int(f[0]),int(f[1]),float(f[3]),float(f[4]),float(f[5])))
        k+=1
    return co
frames=[]
for i in idxs:
    co=block(i)
    if len(co)==19: frames.append((i+1,co))
print("frames",len(frames),"first line",frames[0][0],"last line",frames[-1][0])
for tag,(ln,co) in (("first",frames[0]),("last",frames[-1])):
    d=lambda i,j: math.dist(co[i-1][2:],co[j-1][2:])
    print(f"{tag} L{ln} formula="+"".join(EL[c[1]] for c in co))
    print(f"   O1H2={d(1,2):.4f} H2O9={d(2,9):.4f} O1H4={d(1,4):.4f} H4N8={d(4,8):.4f} O1H3={d(1,3):.4f} H2N8={d(2,8):.4f} O9H16={d(9,16):.4f} O1O9={d(1,9):.4f}")
    nb=[]
    for c in co:
        if c[0]==4: continue
        dd=math.dist(co[3][2:],c[2:])
        if dd<2.7: nb.append((dd,c[0],EL[c[1]]))
    nb.sort(); print("   H4 neighbors<2.7:", "  ".join(f"{i}{e}:{v:.3f}" for v,i,e in nb))
    nb=[]
    for c in co:
        if c[0]==8: continue
        dd=math.dist(co[7][2:],c[2:])
        if dd<2.7: nb.append((dd,c[0],EL[c[1]]))
    nb.sort(); print("   N8 neighbors<2.7:", "  ".join(f"{i}{e}:{v:.3f}" for v,i,e in nb))
# energies
es=[(i+1,l.split("=")[1].split("A.U.")[0].strip()) for i,l in enumerate(L) if "SCF Done:" in l]
print("n SCF Done:",len(es)," first",es[0]," last",es[-1])
