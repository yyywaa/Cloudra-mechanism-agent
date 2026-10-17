import numpy as np, math
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])
path='gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log'
lines=open(path,'rb').read().decode('utf-8','replace').splitlines()
oc=[i for i,l in enumerate(lines) if l.strip().startswith('Optimization completed')]
print('OptCompleted lines:', [i+1 for i in oc])
def geom_before(idx):
    hdr=None
    for j in range(idx, max(0,idx-6000), -1):
        if 'Standard orientation:' in lines[j] or 'Input orientation:' in lines[j]:
            hdr=j; break
    k=hdr+5; atoms=[]
    while k<len(lines):
        if lines[k].strip().startswith('-----'): break
        p=lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms, hdr+1
frames=[]
for i in oc:
    a,h=geom_before(i)
    scf=None
    for j in range(i, max(0,i-6000), -1):
        if 'SCF Done' in lines[j]:
            scf=(j+1, lines[j].split()[4]); break
    # which scan point
    sp=None
    for j in range(i, max(0,i-6000), -1):
        if 'on scan point' in lines[j]:
            sp=' '.join(lines[j].split()[-5:]); break
    frames.append((a,h,scf,sp))
    print('conv L%d geom hdr L%d natoms %d SCF L%s=%s  [%s]' % (i+1,h,len(a),scf[0],scf[1],sp))
def d(a,i,j): return math.dist(a[i-1][1:], a[j-1][1:])
for t,(a,h,scf,sp) in enumerate(frames):
    print('pt%d: R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f' % (t+1, d(a,2,4), d(a,25,26), d(a,4,26), d(a,10,27), d(a,2,25)))
E0=float(frames[0][2][1])
for t,(a,h,scf,sp) in enumerate(frames):
    print('pt%d E=%s  dE vs pt1 = %+.2f kcal/mol' % (t+1, scf[1], (float(scf[1])-E0)*627.5095))
def heavy(a): return [x[1:] for x in a if x[0]!=1]
for t in range(len(frames)-1):
    r,m,det=kabsch(heavy(frames[t][0]), heavy(frames[t+1][0]))
    print('Kabsch heavy20 pt%d->pt%d: RMSD=%.4f max=%.4f det=%+.2f' % (t+1,t+2,r,m,det))
