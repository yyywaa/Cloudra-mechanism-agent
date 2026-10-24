import math
LOG="/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HL1/HL1_E1/irc_endpoints/rev_outer/rev_outer_opt_fix1.log"
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
fr=[(i+1,block(i)) for i in idxs if len(block(i))==19]
print("frames",len(fr),"last line",fr[-1][0])
for tag,(ln,co) in (("first",fr[0]),("last",fr[-1])):
    d=lambda i,j: math.dist(co[i-1][2:],co[j-1][2:])
    print(f"{tag} L{ln}: O1H2={d(1,2):.4f} H2O9={d(2,9):.4f} O1H4={d(1,4):.4f} H4N8={d(4,8):.4f} O9H16={d(9,16):.4f} O1O9={d(1,9):.4f}")
es=[(i+1,l.split("=")[1].split("A.U.")[0].strip()) for i,l in enumerate(L) if "SCF Done:" in l]
print("nSCF",len(es),"first",es[0],"last",es[-1])
print("--- tail lines")
for l in L[-8:]: print(l[:150])
