import numpy as np
path='gold_finish_20261015/HI1/E1/split/E1A_fallback_earlyattack_minsep090.xyz'
S=[];X=[]
for L in open(path).read().splitlines()[2:]:
    p=L.split()
    if len(p)==4: S.append(p[0]); X.append([float(v) for v in p[1:]])
X=np.array(X); print('atoms',len(X),{s:S.count(s) for s in set(S)})
D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1); np.fill_diagonal(D,9)
i,j=np.unravel_index(np.argmin(D),D.shape)
print('minsep %.4f at %d%s-%d%s'%(D[i,j],i+1,S[i],j+1,S[j]))
def d(a,b): return float(np.linalg.norm(X[a-1]-X[b-1]))
print('C2-N18 %.4f C2-O3 %.4f N18-H27 %.4f O3-H27 %.4f'%(d(2,18),d(2,3),d(18,27),d(3,27)))