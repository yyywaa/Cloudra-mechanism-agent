import math
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0004/irc/irc.log"
L=open(LOG).read().splitlines()
def frame(hdr_line):
    co=[]; k=hdr_line+4
    while not L[k].strip().startswith("-----"):
        f=L[k].split()
        if len(f)>=6: co.append((int(f[0]), int(f[1]), float(f[3]), float(f[4]), float(f[5])))
        k+=1
    return co
EL={8:'O',1:'H',6:'C',7:'N'}
for name,line in (("REV pt10",8672),("FWD pt10",4538)):
    co=frame(line)
    print("==",name,"line",line,"natoms",len(co),"formula","".join(EL[c[1]] for c in co))
    print("   N count:",sum(1 for c in co if c[1]==7), " O count:",sum(1 for c in co if c[1]==8))
    for center in (4,8,1,2,9):
        nb=[]
        for c in co:
            if c[0]==center: continue
            d=math.dist(co[center-1][2:], c[2:])
            if d<2.7: nb.append((d,c[0],EL[c[1]]))
        nb.sort()
        print(f"   atoms<2.7 of {center}{EL[co[center-1][1]]}: "+"  ".join(f"{i}{e}:{d:.3f}" for d,i,e in nb))
