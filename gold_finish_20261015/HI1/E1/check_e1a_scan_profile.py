import numpy as np, itertools
log="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192.log"
L=open(log,errors='ignore').read().splitlines()
starts=[i for i,l in enumerate(L) if 'Standard orientation' in l]
Z={'6':0.76,'7':0.71,'8':0.66,'1':0.31}
cov=Z
frames=[]
for s in starts:
    dash=[i for i in range(s,s+20) if L[i].strip().startswith('---')]
    if len(dash)<2: continue
    hdr=dash[1]; els=[];X=[];k=hdr+1
    while len(X)<27 and k<len(L):
        p=L[k].split()
        if len(p)==6 and p[1] in cov:
            els.append(p[1]); X.append([float(p[3]),float(p[4]),float(p[5])])
        k+=1
    if len(X)==27: frames.append((s+1,els,np.array(X)))
print("orientation blocks with 27 atoms:",len(frames))
for idx,(ln,els,X) in enumerate(frames,1):
    R=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
    sep=min(((R(a,b),a,b,R(a,b)<1.25*(cov[els[a-1]]+cov[els[b-1]])) for a,b in itertools.combinations(range(1,28),2)))
    nb=[x for x in sorted((R(a,b),a,b) for a,b in itertools.combinations(range(1,28),2) if not R(a,b)<1.25*(cov[els[a-1]]+cov[els[b-1]]))][:1]
    print("frame %2d (L%d): R(2,18)=%.4f R(2,3)=%.4f R(3,27)=%.4f R(18,27)=%.4f globalmin=%.4f(%d-%d,bonded=%s) min_nonbond=%.4f(%d-%d)"%(
        idx,ln,R(2,18),R(2,3),R(3,27),R(18,27),sep[0],sep[1],sep[2],sep[3],nb[0][0],nb[0][1],nb[0][2]))
