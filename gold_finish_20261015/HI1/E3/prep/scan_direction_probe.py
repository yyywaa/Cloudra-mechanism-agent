import numpy as np, re
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
N=41
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[]
        while k<len(L) and len(co)<N:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit(): co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==N: blocks.append((i+1,np.array(co)))
        i=k
    else: i+=1
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
opt=[i+1 for i,ln in enumerate(L) if "Optimization completed" in ln]
d=lambda X,a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
pts=[]
for oc in opt:
    b=[x for x in blocks if x[0]<oc][-1]
    e=[(l,en) for l,en in scf if l<oc][-1]
    pts.append(dict(oc=oc,hdr=b[0],r24=d(b[1],2,4),rp=d(b[1],25,26),E=e[1],Eln=e[0]))
print("converged points: %d" % len(pts))
print("scan# | meas R(2,4) | meas R(25,26) | E (L) | OPT L")
for n,p in enumerate(pts,1):
    print("  %2d  |  %8.4f   |   %8.4f    | %.9f (L%d) | L%d" % (n,p["r24"],p["rp"],p["E"],p["Eln"],p["oc"]))
print()
cols={}
for n,p in enumerate(pts,1):
    key=round(p["rp"],2); cols.setdefault(key,[]).append((n,p["r24"]))
print("per-column measured R(2,4) sequences (grouped by rounded R(25,26)):")
for key in sorted(cols):
    seq=cols[key]
    print("  column R(25,26)=%.2f : " % key + " -> ".join("#%d %.4f" % (n,r) for n,r in seq))
print()
for key in sorted(cols):
    seq=cols[key]
    if len(seq)>=2:
        dirs=[(b[1]-a[1]) for a,b in zip(seq[:-1],seq[1:])]
        inc=all(x>0.05 for x in dirs); dec=all(x<-0.05 for x in dirs)
        print("  column %.2f direction within column: %s" % (key, "increasing" if inc else ("decreasing" if dec else "mixed/flat %s" % [round(x,3) for x in dirs])))
# in-progress point
laststep=[(i+1,L[i].strip()) for i in range(len(L)) if "on scan point" in L[i] and "Step number" in L[i]][-1]
h,X=blocks[-1]
print()
print("in-progress: last step L%d = %s" % laststep)
print("             last block L%d meas (R(2,4)=%.4f, R(25,26)=%.4f)" % (h,d(X,2,4),d(X,25,26)))
# earliest block of the in-progress scan point
m=re.search(r"scan point\s+(\d+) out of", laststep[1]); curpt=int(m.group(1))
marks=[i+1 for i,ln in enumerate(L) if "Step number" in ln and re.search(r"scan point\s+%d out of"%curpt, ln)]
first=[b for b in blocks if b[0]<marks[0]][-1]
print("             first block of scan point %d: L%d meas (R(2,4)=%.4f, R(25,26)=%.4f)" % (curpt, first[0], d(first[1],2,4), d(first[1],25,26)))
# verdict
curkey=round(pts[-1]["rp"],2)
new_first=(d(first[1],2,4), d(first[1],25,26))
print()
if abs(new_first[1]-curkey)<0.02:
    # same column as the last converged point => within-column advance
    last=pts[-1]
    seq=cols[curkey]
    dirn="decreasing" if new_first[0]<last["r24"] else "increasing"
    print("VERDICT: WITHIN-COLUMN ADVANCE (serpentine continues) -- scan point %d stays in column R(25,26)=%.2f and moves R(2,4) %.4f -> %.4f (%s); same direction as the column's converged sequence (%s)." % (curpt,curkey,last["r24"],new_first[0],dirn, " -> ".join("%.4f"%x for _,x in seq)))
else:
    cands=[(k,v) for k,v in cols.items() if k!=curkey and len(v)>=2]
    if cands:
        k_prev, prev = max(cands, key=lambda kv: len(kv[1]))
        lastrow=prev[-1][1]; firstrow=prev[0][1]
        step=abs(prev[-1][1]-prev[-2][1])
        pdir="increasing" if lastrow>firstrow else "decreasing"
        if abs(new_first[0]-(lastrow-step))<0.05:
            print("VERDICT: SERPENTINE (column change) -- column %.2f ran %s %.4f -> %.4f (step %.3f); the new column %.2f starts at R(2,4)=%.4f = last - step." % (k_prev,pdir,firstrow,lastrow,step,round(new_first[1],2),new_first[0]))
        elif abs(new_first[0]-firstrow)<0.05:
            print("VERDICT: ROW-MAJOR FORWARD -- new column resets R(2,4) to its start value %.4f." % firstrow)
        else:
            print("VERDICT: undetermined -- new column starts at R(2,4)=%.4f, neither last-step (%.4f) nor start (%.4f); report as artefact-class event, do not kill." % (new_first[0],lastrow-step,firstrow))
    else:
        print("VERDICT: undetermined -- need one finished column with >=2 converged points.")
