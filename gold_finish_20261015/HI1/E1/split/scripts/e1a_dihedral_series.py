
import sys, math, re
import numpy as np
log=sys.argv[1]
L=open(log,errors='replace').read().splitlines()
def sym(z): return {1:'H',6:'C',7:'N',8:'O'}[z]
blocks=[]; i=0
while i<len(L):
    if ('Input orientation:' in L[i]) or ('Standard orientation:' in L[i]):
        j=i+1; d=0
        while j<len(L) and d<2:
            if L[j].strip().startswith('---'): d+=1
            j+=1
        at=[]
        while j<len(L):
            t=L[j].split()
            if len(t)==6 and t[0].isdigit() and t[1].isdigit():
                at.append((sym(int(t[1])),float(t[3]),float(t[4]),float(t[5]))); j+=1
            else: break
        if at: blocks.append((i+1, 'I' if 'Input orientation:' in L[i] else 'S', at))
        i=j; continue
    i+=1
def dih(A,a,b,c,d):
    p=[np.array(A[i-1][1:]) for i in (a,b,c,d)]
    b0=p[0]-p[1]; b1=p[2]-p[1]; b2=p[3]-p[2]
    b1n=b1/np.linalg.norm(b1)
    v=b0-np.dot(b0,b1n)*b1n; w=b2-np.dot(b2,b1n)*b1n
    return math.degrees(math.atan2(np.dot(np.cross(b1n,v),w), np.dot(v,w)))
conv=[idx for idx,line in enumerate(L,1) if 'Optimization completed' in line]
print('converged points:', len(conv))
for n,cl in enumerate(conv,1):
    cand=[b for b in blocks if b[0] < cl]
    ln,kind,A = cand[-1]
    print('pt%2d convL %6d  last block L%6d(%s): dih(3,2,18,14)=%+8.2f  R(2,18)=%.4f  R(3,27)=%.4f' % (n, cl, ln, kind, dih(A,3,2,18,14), math.dist(A[1][1:],A[17][1:]), math.dist(A[2][1:],A[26][1:])))
