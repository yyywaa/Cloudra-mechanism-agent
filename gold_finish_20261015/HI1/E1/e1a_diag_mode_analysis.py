import numpy as np, re, sys
sys.path.insert(0,'gold_finish_20261015/HI1/E1')
from gauss_mode_check import parse
log='gold_finish_20261015/HI1/E1/split/E1A_TS_diag_freq.log'
xyz='gold_finish_20261015/HI1/E1/split/E1A_TS_candidate_job1055.xyz'
S=[];X=[]
for L in open(xyz).read().splitlines()[2:]:
    p=L.split()
    if len(p)==4: S.append(p[0]); X.append([float(v) for v in p[1:]])
X=np.array(X)
g,hdr,rows=parse(log)
mode=None
for grp in g:
    for mi,f in enumerate(grp['freq']):
        if f<-50: mode=(grp,mi,f)
grp,mi,f=mode
N=len(S); print('atoms',N,'groups',len(g),'modes',sum(len(x['freq']) for x in g),'imag_mode',f,'line',grp['line'])
m={'H':1.008,'C':12.011,'N':14.007,'O':15.999}
a={}; dvec={}
for at,v in grp['disp'].items():
    dvec[at]=np.array(v[3*mi:3*mi+3]); a[at]=dvec[at]/np.sqrt(m[S[at-1]])
tot=sum(np.linalg.norm(v) for v in dvec.values())
print('--- key atoms (working order 1-based)')
for at in (2,3,18,27):
    print('atom %d %s |d|=%.4f share=%.4f  cart_amp=%.4f A'%(at,S[at-1],np.linalg.norm(dvec[at]),np.linalg.norm(dvec[at])/tot,np.linalg.norm(a[at])))
def bond(ia,ib,label):
    u=(X[ib-1]-X[ia-1]); R=np.linalg.norm(u); u/=R
    dR=float((a[ib]-a[ia]).dot(u))
    print('  %s: R=%.4f A, mode d R = %+.4f A (per unit mode amplitude)'%(label,R,dR))
print('--- bond responses')
bond(3,27,'O3-H27'); bond(18,27,'N18-H27'); bond(2,18,'C2-N18'); bond(2,3,'C2-O3'); bond(2,4,'C2-C4')
print('--- heavy-atom share vs H share')
shareH=sum(np.linalg.norm(dvec[i]) for i in range(1,N+1) if S[i-1]=='H')/tot
shareHeavy=1-shareH
print('  Sigma|d| share: H = %.4f, heavy = %.4f'%(shareH,shareHeavy))
print('--- lowest real mode')
allf=[(x['freq'][i],x['line'],i) for x in g for i in range(len(x['freq']))]
reals=sorted([t for t in allf if t[0]>0])
print('  lowest real mode %.4f cm-1 at log line %d'%(reals[0][0],reals[0][1]))
print('  next three: ',[round(t[0],4) for t in reals[1:4]])