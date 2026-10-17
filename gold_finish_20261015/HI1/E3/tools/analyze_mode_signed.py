import math, re, sys
p='/home/ly/Cloudra-mechanism-agent/ts/ts_0016/jobs/declaration_0007/frequency/frequency.log'
L=open(p,errors='replace').read().splitlines()
# geometry: last orientation block
idx=None
for i,l in enumerate(L):
    if 'Standard orientation:' in l or 'Input orientation:' in l: idx=i
at=[]; i=idx+5
while i<len(L):
    t=L[i].split()
    if len(t)!=6: break
    try:
        int(t[0]);int(t[1]);int(t[2]); at.append([int(t[1]),float(t[3]),float(t[4]),float(t[5])])
    except ValueError: break
    i+=1
# displacement block of mode 1: first 'Atom  AN' block after first Frequencies line
freqline=None
for i,l in enumerate(L):
    if 'Frequencies --' in l: freqline=i; break
start=None
for i in range(freqline, freqline+40):
    if 'Atom  AN' in L[i]: start=i; break
disp={}
for i in range(start+1, start+1+len(at)):
    t=L[i].split()
    if len(t)<5: break
    disp[int(t[0])]=[float(t[2]),float(t[3]),float(t[4])]
print('parsed geometry atoms %d, disp atoms %d'%(len(at),len(disp)))
def r(i,j): return [at[i-1][k]-at[j-1][k] for k in (1,2,3)]
def dist(i,j): return math.dist(at[i-1][1:],at[j-1][1:])
def dRdq(i,j):
    u=[disp[i][k]-disp[j][k] for k in range(3)]
    v=r(i,j); n=math.dist([0,0,0],v)
    return sum(u[k]*v[k] for k in range(3))/n
pairs=[(2,25),(25,27),(10,27),(11,27),(2,4),(4,26),(9,10),(9,11),(25,26)]
print('\npair   R(A)    dR/dq (unnormalised eigenvector units)')
for i,j in pairs:
    print('(%2d,%2d) %7.4f  %+0.5f'%(i,j,dist(i,j),dRdq(i,j)))
# methyl H indices: H atoms bonded to C3 (atom 3) and benzylic etc.
def bonded(i, elem=None):
    out=[]
    for j in range(1,len(at)+1):
        if j==i: continue
        if dist(i,j) < 1.75: out.append(j)
    return out
print('\nC3 (atom 3) neighbours:', bonded(3))
print('C2 (atom 2) neighbours:', bonded(2))
# H27 displacement direction vs O25->O10
u=disp[27]
print('\nH27 disp vector: %s |u|=%.3f'%( ['%+.3f'%x for x in u], math.dist([0,0,0],u)))
for name,(a,b) in {'O25->O10':(25,10),'O25->C2':(25,2),'O10->O25':(10,25)}.items():
    v=[at[b-1][k]-at[a-1][k] for k in (1,2,3)]; n=math.dist([0,0,0],v); v=[x/n for x in v]
    print('  projection of H27 disp on %s: %+0.3f'%(name, sum(u[k]*v[k] for k in range(3))))
print('\nlargest |d| atoms:')
for k,v in sorted(disp.items(), key=lambda kv:-math.dist([0,0,0],kv[1]))[:8]:
    print('  atom %2d  |d|=%.3f'%(k, math.dist([0,0,0],v)))
