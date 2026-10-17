
import sys, math, re
L=open(sys.argv[1],errors='replace').read().splitlines()
pt=0; blocks=[]
i=0
while i < len(L):
    m=re.search(r'on scan point\s+(\d+) out of', L[i])
    if m: pt=int(m.group(1))
    if ('Input orientation:' in L[i]) or ('Standard orientation:' in L[i]):
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
        if at: blocks.append((pt,i+1,at))
        i=j; continue
    i+=1
def d(a,b,A): return math.dist(A[a-1][1:],A[b-1][1:])
seen=set()
for pt,s,at in blocks:
    key=(pt, round(d(2,18,at),4))
    print('scan point %d (log line %d): R(2,18)=%.4f R(2,3)=%.4f R(18,27)=%.4f R(3,27)=%.4f minsep=%.4f' % (pt, s, d(2,18,at), d(2,3,at), d(18,27,at), d(3,27,at), min((math.dist(at[a-1][1:],at[b-1][1:]) for a in range(1,len(at)+1) for b in range(a+1,len(at)+1)))))
