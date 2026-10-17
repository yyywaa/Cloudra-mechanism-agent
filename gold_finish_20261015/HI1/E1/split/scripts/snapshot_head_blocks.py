
import sys, math
def blocks(p):
    L=open(p,errors='replace').read().splitlines(); out=[]; i=0
    while i < len(L):
        if ('Standard orientation:' in L[i]) or ('Input orientation:' in L[i]):
            j=i+1; d=0
            while j<len(L) and d<2:
                if L[j].strip().startswith('---'): d+=1
                j+=1
            at=[]
            while j<len(L):
                t=L[j].split()
                if len(t)==6 and t[0].isdigit() and t[1].isdigit():
                    at.append((int(t[1]),float(t[3]),float(t[4]),float(t[5]))); j+=1
                else: break
            if at: out.append((i+1,j,at))
            i=j; continue
        i+=1
    return out
p=sys.argv[1]
bs=blocks(p)
def d(a,b,A): return math.dist(A[a-1][1:],A[b-1][1:])
for k,(s,e,at) in enumerate(bs[:4],1):
    print('block %d lines %d-%d natoms %d : R(2,18)=%.4f R(2,3)=%.4f R(18,27)=%.4f minsep=%.4f' % (k,s,e,len(at),d(2,18,at),d(2,3,at),d(18,27,at),min((math.dist(at[a-1][1:],at[b-1][1:]) for a in range(1,len(at)+1) for b in range(a+1,len(at)+1)))))
