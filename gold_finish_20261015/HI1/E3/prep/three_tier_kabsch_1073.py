import numpy as np, json
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
def lastblock(path):
    L=open(path).read().splitlines(); blk=None; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co)<41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: blk=(i+1,np.array(co),el)
            i=k
        else: i+=1
    return blk
def fit(A,B):
    A=np.asarray(A,float); B=np.asarray(B,float)
    ca,cb=A.mean(0),B.mean(0)
    U,S,Vt=np.linalg.svd((A-ca).T@(B-cb)); d=np.sign(np.linalg.det(U@Vt))
    R=U@np.diag([1.0,1.0,d])@Vt
    return R,ca,cb,np.linalg.det(R)
def evalrms(A,B,R,ca,cb,sel):
    A=np.asarray(A,float);B=np.asarray(B,float)
    P=(A-ca)@R+cb
    D=((P-B)**2).sum(1)
    return float(np.sqrt(D[sel].sum()/sel.sum())), float(np.sqrt(D[sel].max()))
b1=lastblock(BASE+"runs/build_seed_product_optfreq.log"); X=b1[1]; elX=b1[2]
b2=lastblock(BASE+"runs/P_e3b/P_optfreq.log"); P=b2[1]; elP=b2[2]
rows=json.load(open(BASE+"prep/seed_to_P_mapping_v4.json"))["rows"]
def mapping(order): return [(i+1, order[i]) for i in range(41)]
def analyse(order,tag):
    mp=mapping(order)
    bad=[(a,e) for a,e in mp if elX[a-1]!=elP[e-1]]
    Xa=np.array([X[a-1] for a,e in mp]); Pa=np.array([P[e-1] for a,e in mp])
    heavy=np.array([elX[a-1]!=1 for a,e in mp])
    R,ca,cb,det=fit(Xa,Pa)
    r41,m41=evalrms(Xa,Pa,R,ca,cb,np.ones(41,bool))
    rheavy_fitheavy=fit(Xa[heavy],Pa[heavy]); Rh,cah,cbh,deth=rheavy_fitheavy
    r_hh,m_hh=evalrms(Xa[heavy],Pa[heavy],Rh,cah,cbh,np.ones(heavy.sum(),bool))
    r_41fit_hev,m_41fit_hev=evalrms(Xa,Pa,R,ca,cb,heavy)
    print("%s | element mismatches %d | 41fit+41eval %.4f (max %.4f) | heavy20 fit+eval %.4f (max %.4f) | 41fit + heavy20 eval %.4f (max %.4f) | det %+.2f/%+.2f" % (tag,len(bad),r41,m41,r_hh,m_hh,r_41fit_hev,m_41fit_hev,det,deth))
print("coordinator claims: 2.2976/4.7027 (heavy fit+eval), 2.4104/5.3753 (41 fit, heavy eval), 2.6798 (41/41); mapping#1 heavy 2.3538/4.3633")
for k,row in enumerate(rows):
    if row.get("complete"): analyse(row["order"], "mapping#%d (iso %d)" % (k if k else 1, row.get("iso")))
