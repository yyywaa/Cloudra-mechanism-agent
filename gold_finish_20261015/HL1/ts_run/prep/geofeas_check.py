
import numpy as np
base="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run"
L=open(f"{base}/prep/RC_seedB.xyz").read().split("\n"); n=int(L[0])
X=np.array([[float(x) for x in l.split()[1:4]] for l in L[2:2+n]])
C4,N6,O7=X[6],X[7],X[8]
hg=0.988; d3=1.014; c3=np.cos(np.radians(105.6)); s3=np.sin(np.radians(105.6))
unit=lambda v: v/np.linalg.norm(v)
n_hat=unit(N6-O7)
tv=np.array([1.,0.,0.]) if abs(n_hat[0])<0.9 else np.array([0.,1.,0.])
e1=unit(np.cross(n_hat,tv)); e2=np.cross(n_hat,e1)
th=np.radians(np.arange(0,181,4.)); ph=np.radians(np.arange(0,360,6.))
TH,PH=np.meshgrid(th,ph,indexing='ij')
U=(np.cos(TH)[...,None]*n_hat+np.sin(TH)[...,None]*(np.cos(PH)[...,None]*e1+np.sin(PH)[...,None]*e2)).reshape(-1,3)
dOO=np.arange(2.30,3.31,0.10)
O1=(O7[None,None,:]+U[:,None,:]*dOO[None,:,None]).reshape(-1,3)
dO7=np.linalg.norm(O1-O7,axis=1); dN6=np.linalg.norm(O1-N6,axis=1); dC4=np.linalg.norm(O1-C4,axis=1)
R29=dOO[None,:].repeat(U.shape[0],0).reshape(-1)-hg
Ur=np.repeat(U,len(dOO),axis=0)
b1=-Ur; b2=n_hat[None,:]-b1*np.sum(b1*n_hat[None,:],axis=1)[:,None]; b2/=np.linalg.norm(b2,axis=1)[:,None]
ref=b2.copy()
P=O1+(d3*c3)*b1; N6P=N6[None,:]-P
vax=np.sum(N6P*b1,axis=1); rad=np.linalg.norm(N6P-vax[:,None]*b1,axis=1); rr=d3*s3
H3N6=np.sqrt(np.maximum(0.,rad-rr)**2+vax**2)
ok=(dO7>=2.30)&(dN6>=2.30)&(dC4>=3.00)
print("N configs:",int(ok.sum()))
bands=[(1.55,1.70),(1.60,1.70),(1.40,1.55),(1.30,1.40),(1.312,1.400)]
for lo,hi in bands:
    m=ok&(R29>=lo)&(R29<=hi)
    if m.sum()==0: print("  band R29 in [%.2f,%.2f]: no config"%  (lo,hi)); continue
    i=int(np.argmin(np.where(m,H3N6,np.inf)))
    print("  band R29 in [%.2f,%.2f]: %d configs, min H3..N6=%.3f at dOO=%.2f O1N6=%.3f O1C4=%.3f"%(lo,hi,int(m.sum()),H3N6[i],dO7[i],dN6[i],dC4[i]))
i=int(np.argmin(np.where(ok,H3N6,np.inf)))
print("unconstrained-min H3..N6=%.3f at dOO=%.2f R29=%.3f O1N6=%.3f"%(H3N6[i],dO7[i],R29[i],dN6[i]))
