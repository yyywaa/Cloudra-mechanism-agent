import math
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0005/reactant_opt/reactant_opt.log"
L=open(LOG).read().splitlines()
print("lines",len(L))
for i,l in enumerate(L):
    if "Stationary point found" in l or "Normal termination" in l or "Error termination" in l:
        print(i+1, l.strip()[:90])
cs=[i for i,l in enumerate(L) if "Converged?" in l]
if cs:
    i=cs[-1]
    print("--- last conv table at",i+1)
    for l in L[i:i+6]: print("   ",l.strip()[:80])
es=[(i+1,l.split("=")[1].split("A.U.")[0].strip()) for i,l in enumerate(L) if "SCF Done:" in l]
print("nSCF",len(es),"first",es[0],"last",es[-1])
EL={8:'O',1:'H',6:'C',7:'N'}
def block(i):
    co=[];k=i+5
    while not L[k].strip().startswith("-----"):
        f=L[k].split()
        if len(f)>=6: co.append((int(f[0]),int(f[1]),float(f[3]),float(f[4]),float(f[5])))
        k+=1
    return co
idxs=[i for i,l in enumerate(L) if "Standard orientation:" in l or "Input orientation:" in l]
fr=[(i+1,block(i)) for i in idxs if len(block(i))==19]
print("frames",len(fr))
for tag,(ln,co) in (("start",fr[0]),("end",fr[-1])):
    d=lambda i,j: math.dist(co[i-1][2:],co[j-1][2:])
    print(f"{tag} L{ln}: O1H2={d(1,2):.4f} H2O9={d(2,9):.4f} O1H4={d(1,4):.4f} H4N8={d(4,8):.4f} O1O9={d(1,9):.4f} O9H16={d(9,16):.4f}")
