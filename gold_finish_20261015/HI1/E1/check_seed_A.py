import numpy as np
def load(p):
    S=[];X=[]
    for L in open(p).read().splitlines()[2:]:
        q=L.split()
        if len(q)==4: S.append(q[0]); X.append([float(v) for v in q[1:]])
    return S,np.array(X)
S,X=load('gold_finish_20261015/HI1/E1/split/E1a_seed_search/closest_attempt.xyz')
Sref,_=load('gold_finish_20261015/HI1/E1/split/E1A_TS_candidate_job1055.xyz')
print('atoms',len(X),'element order match',S==Sref)
D=np.linalg.norm(X[:,None,:]-X[None,:,:],axis=-1); np.fill_diagonal(D,9)
idx=np.dstack(np.unravel_index(np.argsort(D,axis=None)[:6],D.shape))[0]
seen=set(); top=[]
for a,b in idx:
    k=tuple(sorted((int(a),int(b))))
    if k in seen: continue
    seen.add(k); top.append((round(float(D[a,b]),4),int(a)+1,S[a],int(b)+1,S[b]))
    if len(top)==3: break
def d(a,b): return float(np.linalg.norm(X[a-1]-X[b-1]))
print('R(C2-N18)=%.4f R(N18-H27)=%.4f C2-O3=%.4f O3-H27=%.4f'%(d(2,18),d(18,27),d(2,3),d(3,27)))
print('top3',top)