import sys,re,numpy as np
log="/home/ly/Cloudra-mechanism-agent/ts/ts_0016/jobs/declaration_0007/frequency/frequency.log"
lines=open(log,errors='ignore').read().splitlines()
idx=[i for i,L in enumerate(lines) if 'Standard orientation' in L or 'Input orientation' in L]
start=idx[-1]
dash=[i for i in range(start,start+20) if lines[i].strip().startswith('---')]
hdr=dash[1]
NAtoms=41
geo={}
for k in range(hdr+1, hdr+1+NAtoms):
    p=lines[k].split()
    assert len(p)==6, (k,p)
    geo[int(p[0])]=(int(p[1]), np.array([float(p[3]),float(p[4]),float(p[5])]))
assert len(geo)==NAtoms, len(geo)
print('geometry rows', hdr+1, 'to', hdr+NAtoms, 'count', len(geo), 'elements', [geo[a][0] for a in (2,4,9,10,11,25,26,27)])
def R(a,b): return float(np.linalg.norm(geo[a][1]-geo[b][1]))
for pair in [(2,25),(25,27),(10,27),(25,26),(2,4),(9,10),(9,11),(2,3),(5,4),(8,4),(10,11)]:
    print('R(%d-%d) = %.4f'%(pair[0],pair[1],R(*pair)))
def ang(a,b,c):
    v1=geo[a][1]-geo[b][1]; v2=geo[c][1]-geo[b][1]
    return float(np.degrees(np.arccos(np.dot(v1,v2)/np.linalg.norm(v1)/np.linalg.norm(v2))))
print('angle O25-H27...O10 = %.1f'%ang(25,27,10))
print('angle C2-O25-H27 = %.1f'%ang(2,25,27))
print('angle O25-H26...O10 = %.1f'%ang(25,26,10))
# min separation
best=(9,None)
for a in geo:
  for b in geo:
    if b<=a: continue
    d=R(a,b)
    if d<best[0]: best=(d,(a,b))
print('minsep %.4f between %s'%(best[0],best[1]))
def parse_mode(lines):
    for i,L in enumerate(lines):
        if L.startswith(' Frequencies --'):
            fr=[float(x) for x in L.split('--')[1].split()]
            if fr[0]<0:
                j=i+1
                while j<i+8 and not lines[j].strip().startswith('Atom  AN'): j+=1
                disp={}
                k=j+1
                while k<len(lines) and re.match(r'^\s*\d+\s+\d+', lines[k]):
                    p=lines[k].split()
                    if len(p)!=2+3*len(fr): k+=1; continue
                    disp[int(p[0])]=np.array([float(x) for x in p[2:2+3*len(fr)]])
                    k+=1
                return fr,disp,i+1
fr,disp,ln=parse_mode(lines)
vec={a:disp[a][0:3] for a in disp}
sq={a:float(np.dot(vec[a],vec[a])) for a in vec}
tot2=sum(sq.values()); tot1=sum(np.linalg.norm(vec[a]) for a in vec)
print('mode freq %.4f line %d  sum|d| %.4f  (L1-normalised shares below)'%(fr[0],ln,tot1))
for a in sorted(vec,key=lambda a:-sq[a])[:8]:
    print(' atom %2d el %d |d|=%.4f shareL1=%.4f shareL2=%.4f vec=%s'%(a,geo[a][0],np.linalg.norm(vec[a]),np.linalg.norm(vec[a])/tot1,sq[a]/tot2,np.round(vec[a],4)))
def bond_resp(a,b):
    u=(geo[b][1]-geo[a][1]); u=u/np.linalg.norm(u)
    return float(np.dot(vec[b]-vec[a],u))
print('bond responses (dR/dq, L1-normalised vec):')
for pair in [(2,25),(25,27),(10,27),(25,26),(2,4),(9,10),(9,11),(2,3),(6,31),(20,2)]:
    print('  dR(%d-%d) = %+.4f'%(pair[0],pair[1],bond_resp(*pair)))
u=(geo[10][1]-geo[25][1]); u=u/np.linalg.norm(u); h=vec[27]
print(' |dH27|=%.4f  dH27.u(O25->O10)=%+.4f cos=%.4f'%(np.linalg.norm(h),float(np.dot(h,u)),float(np.dot(h,u)/np.linalg.norm(h))))
u=(geo[2][1]-geo[25][1]); u=u/np.linalg.norm(u)
print(' dH27.u(O25->C2)=%+.4f'%float(np.dot(h,u)))
print(' L2 shares: H27 %.4f H26 %.4f C2 %.4f O25 %.4f O10 %.4f'%(sq[27]/tot2,sq[26]/tot2,sq[2]/tot2,sq[25]/tot2,sq[10]/tot2))
