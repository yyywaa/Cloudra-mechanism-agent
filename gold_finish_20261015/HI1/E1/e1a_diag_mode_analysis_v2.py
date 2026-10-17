import numpy as np, re
log='gold_finish_20261015/HI1/E1/split/E1A_TS_diag_freq.log'
xyz='gold_finish_20261015/HI1/E1/split/E1A_TS_candidate_job1055.xyz'
S=[];X=[]
for L in open(xyz).read().splitlines()[2:]:
    p=L.split()
    if len(p)==4: S.append(p[0]); X.append([float(v) for v in p[1:]])
X=np.array(X); N=len(S)
lines=open(log,errors='ignore').read().splitlines()
i=[k for k,L in enumerate(lines) if L.startswith(' Frequencies --')][0]
fr=[float(x) for x in lines[i].split('--')[1].split()]
rm=[float(x) for x in lines[i+1].split('--')[1].split()]
fc=[float(x) for x in lines[i+2].split('--')[1].split()]
j=i+3
while not lines[j].strip().startswith('Atom  AN'): j+=1
disp={}; k=j+1
while k<len(lines) and lines[k].strip() and re.match(r'^\s*\d+\s+\d+',lines[k]):
    p=lines[k].split()
    if len(p)==2+3*len(fr): disp[int(p[0])]=np.array([float(x) for x in p[2:]])
    k+=1
print('mode block at line',i+1,'freqs',fr,'red.mass',rm,'frc',fc)
d={a:v[0:3] for a,v in disp.items()}
mass={'H':1.008,'C':12.011,'N':14.007,'O':15.999}
amp={a:d[a]/np.sqrt(mass[S[a-1]]) for a in d}
tot=sum(np.linalg.norm(v) for v in d.values())
print('sum|d| %.4f'%tot)
for a in (27,2,3,18,14,1):
    print('atom %2d %s |d|=%.4f share=%.4f cart_amp=%.5f d=%s'%(a,S[a-1],np.linalg.norm(d[a]),np.linalg.norm(d[a])/tot,np.linalg.norm(amp[a]),np.round(d[a],3)))
u=(X[17]-X[2]); R=np.linalg.norm(u); u=u/R
print('unit(O3->N18)=',np.round(u,4),'proj d(H27)=%.4f'%float(d[27].dot(u)))
def bond(a,b,lab):
    v=X[b-1]-X[a-1]; R=np.linalg.norm(v); v=v/R
    print('  %s R=%.4f dR=%+.4f'%(lab,R,float((amp[b]-amp[a]).dot(v))))
print('bond responses (per unit mode amplitude):')
bond(3,27,'O3-H27'); bond(18,27,'N18-H27'); bond(2,18,'C2-N18'); bond(2,3,'C2-O3')
shareH=sum(np.linalg.norm(d[a]) for a in d if S[a-1]=='H')/tot
print('share H %.4f heavy %.4f'%(shareH,1-shareH))