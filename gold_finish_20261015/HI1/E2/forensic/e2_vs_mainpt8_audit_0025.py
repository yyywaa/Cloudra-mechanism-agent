import math, numpy as np
def frames(path):
    L=open(path).read().splitlines()
    conv=[i+1 for i,l in enumerate(L) if 'Optimization completed' in l]
    blocks=[]
    for i,l in enumerate(L):
        if 'Standard orientation' in l:
            at=[];j=i+5
            while j<len(L) and not L[j].strip().startswith('-----'):
                p=L[j].split()
                if len(p)==6: at.append((int(p[0]),int(p[1]),float(p[3]),float(p[4]),float(p[5])))
                j+=1
            blocks.append((i+1,at))
    scf=[(i+1,float(l.split('=')[1].split()[0])) for i,l in enumerate(L) if 'SCF Done' in l]
    out=[]
    for c in conv:
        g=[b for b in blocks if b[0]<c][-1]; s=[x for x in scf if x[0]<c][-1]
        assert len(g[1])==41 and g[1][0][0]==1
        out.append((c,g,s))
    return L,out
b='HI1/E2/scan_1d/build/'
Lm,fm=frames(b+'E2_1D_scan.log'); Lc,fc=frames(b+'E2_1D_scan_cont1.log')
print('main frames',len(fm),'cont1 frames',len(fc))
ref=fm[-1]
print('main pt8: conv L%d hdr L%d SCF L%d E=%.9f'%(ref[0],ref[1][0],ref[2][0],ref[2][1]))
def kab(X,Y,mask):
    idx=[x[0] for x in X if mask(x)]
    P=np.array([[x[2],x[3],x[4]] for x in X if mask(x)]); Q=np.array([[y[2],y[3],y[4]] for y in Y if mask(y)])
    Pc=P-P.mean(0); Qc=Q-Q.mean(0)
    U,S,Vt=np.linalg.svd(Pc.T@Qc); d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,d])@U.T
    dn=np.linalg.norm((R@Pc.T).T-Qc,axis=1)
    return math.sqrt(float((dn**2).sum())/len(P)), float(dn.max()), idx[int(dn.argmax())], float(np.linalg.det(R))
for k,(c,g,s) in enumerate(fc,1):
    D={x[0]:x for x in g[1]}; Dm={x[0]:x for x in ref[1][1]}
    print('cont1 pt%d vs main pt8: heavy20 rms/max/worst = %.4f / %.4f / %d det=%+.6f | all41 %.4f / %.4f / %d | R(1,29)=%.4f' % (
        k, *kab(ref[1][1], g[1], lambda x: x[1]!=1)[:3], kab(ref[1][1], g[1], lambda x: x[1]!=1)[3],
        *kab(ref[1][1], g[1], lambda x: True)[:3], math.dist(D[1][2:],D[29][2:])))
P0=np.array([[x[2],x[3],x[4]] for x in ref[1][1] if x[1]!=1])
rot=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]]); tt=np.array([1.,2.,-1.])
def kn(P,Q):
    Pc=P-P.mean(0);Qc=Q-Q.mean(0)
    U,S,Vt=np.linalg.svd(Pc.T@Qc); d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,d])@U.T
    dn=np.linalg.norm((R@Pc.T).T-Qc,axis=1); return math.sqrt(float((dn**2).sum())/len(P))
print('SELF r+t=%.3e mirror=%.4f copy=%.3e'%(kn(P0,(rot@P0.T).T+tt),kn(P0,P0*np.array([-1.,1.,1.])),kn(P0,P0)))
