import math, numpy as np
P='HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log'
L=open(P).read().splitlines()
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
fr=[]
for c in conv:
    g=[b for b in blocks if b[0]<c][-1]; s=[x for x in scf if x[0]<c][-1]
    assert len(g[1])==41 and g[1][0][0]==1
    fr.append((c,g,s))
print('lines',len(L),'conv',len(fr),'convlines',[f[0] for f in fr])
R1028=-939.312626605
for k,(c,g,s) in enumerate(fr,1):
    D={x[0]:x for x in g[1]}
    d=lambda i,j: math.dist(D[i][2:],D[j][2:])
    print('pt%d optL%d hdrL%d SCF L%d E=%.9f dE1028=%+.4f | R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f R(2,26)=%.4f' % (
        k,c,g[0],s[0],s[1],(s[1]-R1028)*627.509474, d(2,4),d(25,26),d(4,26),d(10,27),d(2,25),d(2,26)))
def kab(X,Y,mask):
    idx=[x[0] for x in X if mask(x)]
    A=np.array([[x[2],x[3],x[4]] for x in X if mask(x)]); B=np.array([[y[2],y[3],y[4]] for y in Y if mask(y)])
    Ac=A-A.mean(0); Bc=B-B.mean(0)
    U,S,Vt=np.linalg.svd(Ac.T@Bc); d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,d])@U.T
    dn=np.linalg.norm((R@Ac.T).T-Bc,axis=1)
    return math.sqrt(float((dn**2).sum())/len(A)), float(dn.max()), idx[int(dn.argmax())], float(np.linalg.det(R))
for k in range(len(fr)-2, len(fr)-1):
    if k+1 < len(fr):
        pass
for k in [len(fr)-3, len(fr)-2]:
    X=fr[k][1][1]; Y=fr[k+1][1][1]
    print('Kabsch #%d->#%d heavy20 %.4f / %.4f / %d det=%+.6f | all41 %.4f / %.4f / %d' % (k+1,k+2,*kab(X,Y,lambda x:x[1]!=1)[:3],kab(X,Y,lambda x:x[1]!=1)[3],*kab(X,Y,lambda x:True)[:3]))
A=np.array([[x[2],x[3],x[4]] for x in fr[-1][1][1] if x[1]!=1])
rot=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]]); tt=np.array([1.,2.,-1.])
def kn(A,B):
    Ac=A-A.mean(0);Bc=B-B.mean(0)
    U,S,Vt=np.linalg.svd(Ac.T@Bc); d=np.sign(np.linalg.det(Vt.T@U.T)); R=Vt.T@np.diag([1,1,d])@U.T
    dn=np.linalg.norm((R@Ac.T).T-Bc,axis=1); return math.sqrt(float((dn**2).sum())/len(A))
print('SELF r+t=%.3e mirror=%.4f copy=%.3e'%(kn(A,(rot@A.T).T+tt),kn(A,A*np.array([-1.,1.,1.])),kn(A,A)))
