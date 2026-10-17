
import sys, math, re
log = sys.argv[1]; RC = -593.934532807; K = 627.509474; R0 = 2.1920; STEP = -0.1000
L = open(log, errors='replace').read().splitlines()
RAD = {'H':0.31,'C':0.76,'N':0.71,'O':0.66}
def sym(z): return {1:'H',6:'C',7:'N',8:'O'}[z]
blocks=[]; i=0
while i < len(L):
    if ('Input orientation:' in L[i]) or ('Standard orientation:' in L[i]):
        j=i+1; d=0
        while j<len(L) and d<2:
            if L[j].strip().startswith('---'): d+=1
            j+=1
        at=[]
        while j<len(L):
            t=L[j].split()
            if len(t)==6 and t[0].isdigit() and t[1].isdigit():
                at.append((sym(int(t[1])), float(t[3]), float(t[4]), float(t[5]))); j+=1
            else: break
        if at: blocks.append((j, at))
        i=j; continue
    i+=1
pts=[]; scfE=None; scfL=None
for idx,line in enumerate(L,1):
    if 'SCF Done:' in line:
        m=re.search(r'E\(RB3LYP\)\s*=\s*(-?\d+\.\d+)', line)
        if m: scfE=float(m.group(1)); scfL=idx
    if 'Optimization completed' in line:
        pts.append((idx, scfE, scfL))
def d(a,b,A): return math.dist(A[a-1][1:], A[b-1][1:])
def classify(A):
    n=len(A); bonded=set()
    for a in range(1,n+1):
        for b in range(a+1,n+1):
            if d(a,b,A) < RAD[A[a-1][0]]+RAD[A[b-1][0]]+0.45: bonded.add((a,b))
    adj={k:set() for k in range(1,n+1)}
    for a,b in bonded: adj[a].add(b); adj[b].add(a)
    def order(a,b):
        if (min(a,b),max(a,b)) in bonded: return 1
        if adj[a] & adj[b]: return 2
        return 3
    return order
E1=None
print('%2s %6s %7s %16s %8s %8s %8s %9s %9s %8s %8s %8s %8s' % ('pt','convL','scfL','E(RB3LYP)','R2-18','target','diff','dE_RC27','dE_pt1','C2-O3','R18-27','R3-27','minsep'))
for n,(convL,E,scfL) in enumerate(pts,1):
    _,A=[b for b in blocks if b[0] < convL][-1]
    if n==1: E1=E
    tgt = R0 + STEP*(n-1)
    order=classify(A)
    pairs=sorted(((d(a,b,A),a,b,order(a,b)) for a in range(1,len(A)+1) for b in range(a+1,len(A)+1)))
    bmin=min(p for p in pairs if p[3]==1); omin=min(p for p in pairs if p[3]==2); nmin=min(p for p in pairs if p[3]==3)
    print('%2d %6d %7d %16.9f %8.4f %8.4f %+8.4f %9.2f %9.2f %8.4f %8.4f %8.4f %8.4f' % (n, convL, scfL, E, d(2,18,A), tgt, d(2,18,A)-tgt, (E-RC)*K, (E-E1)*K, d(2,3,A), d(18,27,A), d(3,27,A), pairs[0][0]))
    print('     contacts: bonded %.4f (%d-%d) | 1-3 %.4f (%d-%d) | nonbonded %.4f (%d-%d)' % (bmin[0],bmin[1],bmin[2], omin[0],omin[1],omin[2], nmin[0],nmin[1],nmin[2]))
Es=[p[1] for p in pts]
print('E series:', ', '.join('%.9f'%e for e in Es))
print('monotone increasing vs RC?', all(Es[i] > Es[i+1] for i in range(len(Es)-1)) if False else [((Es[i]-RC)*K < (Es[i+1]-RC)*K) for i in range(len(Es)-1)])
