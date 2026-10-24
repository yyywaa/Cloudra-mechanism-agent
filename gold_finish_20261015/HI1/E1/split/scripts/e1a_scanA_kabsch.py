import sys, math
import numpy as np

def read_xyz(p):
    L=open(p).read().splitlines()
    n=int(L[0].split()[0]); ats=[]
    for ln in L[2:2+n]:
        t=ln.split(); ats.append((t[0], np.array([float(t[1]),float(t[2]),float(t[3])])))
    return ats

def kabs(P,Q):
    pc=P.mean(0); qc=Q.mean(0)
    P0=P-pc; Q0=Q-qc
    Hm=P0.T@Q0
    U,S,Vt=np.linalg.svd(Hm)
    sign=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1.0,1.0,sign])@U.T
    fit=(R@P0.T).T+qc
    dev=np.linalg.norm(fit-Q,axis=1)
    return dict(det=float(np.linalg.det(R)), det_raw=float(sign),
                rms=float(math.sqrt((dev**2).mean())), mx=float(dev.max()),
                worst=int(dev.argmax())+1, dev=dev)

a=read_xyz(sys.argv[1]); b=read_xyz(sys.argv[2])
assert len(a)==len(b)
heavy=[i for i,(e,_) in enumerate(a) if e!='H']
allidx=list(range(len(a)))
print('natoms',len(a),'heavy',len(heavy),'H',len(a)-len(heavy))
def run(name, idx):
    P=np.array([a[i][1] for i in idx]); Q=np.array([b[i][1] for i in idx])
    r=kabs(P,Q)
    order=np.argsort(-r['dev'])
    print('[%s] n=%d det(R)=%+.6f rms=%.4f A max=%.4f A worst_working_atom=%d'%(
        name, len(idx), r['det'], r['rms'], r['mx'], idx[r['worst']-1]+1))
    print('   top5 per-atom displacement (working atom : A): '+', '.join('%d:%.4f'%(idx[o]+1, r['dev'][o]) for o in order[:5]))
    return r
rh=run('heavy-12', heavy)
ra=run('all-27', allidx)

P=np.array([a[i][1] for i in allidx]); Q=np.array([b[i][1] for i in allidx])
rnd=np.random.default_rng(20261018)
Mu=rnd.normal(size=(3,3)); Qo,_=np.linalg.qr(Mu)
if np.linalg.det(Qo)<0: Qo[:,0]*=-1
t=rnd.normal(size=3)*3.0
r1=kabs(P, (P@Qo.T)+t)
print('[self-check 1: known rotation+translation] rms=%.6f A max=%.6f A det(R)=%+.6f'%(r1['rms'],r1['mx'],r1['det']))
Qm=Q.copy(); Qm[:,0]*=-1.0
r2=kabs(P,(P.copy()*np.array([-1.0,1.0,1.0])))
print('[self-check 2: mirrored copy] rms=%.4f A max=%.4f A det_raw=%+.0f det(R_used)=%+.0f'%(r2['rms'],r2['mx'],r2['det_raw'],r2['det']))
r3=kabs(P,P.copy())
print('[self-check 3: identical copy] rms=%.8f A max=%.8f A det=%+.6f'%(r3['rms'],r3['mx'],r3['det']))
