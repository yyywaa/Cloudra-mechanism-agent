import numpy as np
L=open('ts/ts_0008/jobs/declaration_0003/frequency/frequency.log').read().split(chr(10))
b=[k for k,l in enumerate(L) if l.strip().startswith('Atom  AN')][0]
print('eigenvector header L%d: %s'%(b+1,L[b].rstrip()))
rows=[]
for l in L[b+1:b+45]:
    p=l.split()
    if len(p)>=11 and p[0].isdigit(): rows.append(p)
    elif rows: break
print('atom rows parsed:',len(rows))
mode1=np.array([[float(r[2]),float(r[3]),float(r[4])] for r in rows])
mag=np.linalg.norm(mode1,axis=1)
tot=mag.sum()
print('sum|d| = %.4f'%tot)
top=np.argsort(-mag)[:8]+1
print('top displaced atoms (1-based, built order):',[(int(i), round(float(mag[i-1]/tot),3)) for i in top])
H=[5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,33,34,35,36,37,38,39,40,41]
H=[i for i in range(1,42) if i in (5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,26,27,33,34,35,36,37,38,39,40,41)]
print('all-H share of sum|d| = %.3f'%(sum(mag[i-1] for i in H)/tot))
print('H41 share = %.3f'%(mag[40]/tot))
for a,bb,lab in [(2,3,'C2-O4'),(4,10,'C3-H22'),(32,41,'N20-H21'),(2,4,'C2-C3'),(2,32,'C2..N20'),(3,41,'O4..H21'),(3,10,'O4..H22')]:
    print('  pair %-9s (%2d,%2d) normalized |d_a|+|d_b| = %.3f'%(lab,a,bb,(mag[a-1]+mag[bb-1])/tot))