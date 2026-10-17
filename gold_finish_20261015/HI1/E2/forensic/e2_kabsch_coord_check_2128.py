import numpy as np, re, math
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])
path = 'gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log'
lines = open(path,'rb').read().decode('utf-8','replace').splitlines()
oc = [i for i,l in enumerate(lines) if l.strip().startswith('Optimization completed')]
print('Optimization completed lines:', [i+1 for i in oc])
def geom_before(idx):
    hdr = None
    for j in range(idx, max(0, idx-4000), -1):
        if 'Standard orientation:' in lines[j] or 'Input orientation:' in lines[j]:
            hdr = j; break
    k = hdr+5; atoms=[]
    while k < len(lines):
        if lines[k].strip().startswith('-----'): break
        p = lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms, hdr+1
frames=[]
for i in oc:
    a, h = geom_before(i)
    frames.append((a,h))
    # last SCF before i
    scf=None
    for j in range(i, max(0,i-4000), -1):
        if 'SCF Done' in lines[j]:
            scf=(j+1, lines[j].split()[4]); break
    print('conv at L%d: geom hdr L%d natoms=%d last SCF L%s = %s' % (i+1, h, len(a), scf[0], scf[1]))
Zs=[ [x[0] for x in f[0]] for f in frames]
print('element seqs equal across frames:', all(z==Zs[0] for z in Zs))
def heavy(A): 
    return [x[1:] for x in A if x[0]!=1]
for t in range(len(frames)-1):
    A=heavy(frames[t][0]); B=heavy(frames[t+1][0])
    r,m,det = kabsch(A,B)
    ra,ma,da = kabsch([x[1:] for x in frames[t][0]],[x[1:] for x in frames[t+1][0]])
    print('pair %d-%d: heavy20 RMSD=%.4f max=%.4f det=%+.2f | all41=%.4f max=%.4f' % (t+1,t+2,r,m,det,ra,ma))
