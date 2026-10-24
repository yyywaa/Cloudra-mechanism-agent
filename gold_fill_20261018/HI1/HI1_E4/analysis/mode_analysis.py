
import numpy as np, sys

def parse_freq_log(path):
    L=open(path).read().splitlines()
    idx=[i for i,l in enumerate(L) if 'Input orientation:' in l]
    i0=idx[-1]
    els=[];X=[]
    for l in L[i0+5:]:
        s=l.split()
        if len(s)==6 and s[0].isdigit():
            els.append(int(s[1])); X.append([float(x) for x in s[3:6]])
        elif len(els)>0 and not (len(s)==6 and s[0].isdigit()):
            break
    X=np.array(X)
    mi=[i for i,l in enumerate(L) if l.strip().startswith('Frequencies --')][0]
    vec=[]
    for l in L[mi+5:mi+5+len(els)]:
        s=l.split()
        vec.append([float(s[2]),float(s[3]),float(s[4])])
    return np.array(els),X,np.array(vec)

path=sys.argv[1]
els,X,U=parse_freq_log(path)
n=len(els)
D=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
def dr(a,b):
    u=X[b-1]-X[a-1]; u=u/np.linalg.norm(u)
    return float(np.dot(U[b-1]-U[a-1],u))
zn={1:'H',6:'C',7:'N',8:'O'}
print('natoms',n)
print('elements(1-based):',' '.join('%d:%s'%(i+1,zn[e]) for i,e in enumerate(els)))
print('TS distances: C2-O25 %.4f  C2-N4 %.4f  O28-H24 %.4f  O25-H24 %.4f  O25-H26 %.4f  O25-H27 %.4f  O10-H27 %.4f'%(D(2,25),D(2,4),D(28,24),D(25,24),D(25,26),D(25,27),D(10,27)))
pairs=[(2,25),(2,4),(28,24),(25,24)]
norm=U**2; tot=norm.sum()
heavy=[i+1 for i,e in enumerate(els) if e!=1]
at=norm.sum(axis=1)/tot
sh_pair=sum((norm[a-1].sum()+norm[b-1].sum()) for a,b in pairs)
print('sum of squared disp %.6f'%tot)
print('share declared reaction-center atoms %.4f'%(sh_pair/tot))
print('share all heavy atoms %.4f'%(sum(at[i-1] for i in heavy)))
order=np.argsort(at)[::-1][:8]
print('max single-atom share %.4f at atom %d (%s)'%(at[order[0]],order[0]+1,zn[els[order[0]]]))
for i in order:
    print('   atom %2d %s share %.4f vec %s'%(i+1,zn[els[i]],at[i],np.round(U[i],3)))
print('dR along mode (negative = shortening):')
for a,b in pairs:
    print('   (%d,%d) %+0.5f'%(a,b,dr(a,b)))
