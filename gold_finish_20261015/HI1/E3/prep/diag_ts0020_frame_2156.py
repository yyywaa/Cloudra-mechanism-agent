import math
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])
path='ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log'
lines=open(path,'rb').read().decode('utf-8','replace').splitlines()
idx=[i for i,l in enumerate(lines) if 'Standard orientation:' in l or 'Input orientation:' in l]
s=idx[-1]; k=s+5; atoms=[]
while k<len(lines):
    if lines[k].strip().startswith('-----'): break
    p=lines[k].split()
    if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
    k+=1
print('last block hdr L%d, natoms=%d, file %d lines' % (s+1, len(atoms), len(lines)))
def d(i,j): return math.dist(atoms[i-1][1:], atoms[j-1][1:])
for lab,(i,j) in {'C2-N4':(2,4),'C2-O25':(2,25),'O25-H26':(25,26),'N4-H26':(4,26),'O10-H27':(10,27),'N4-H27':(4,27),'O10-H26':(10,26),'C2-O3':(2,3),'C9-O10':(9,10),'C9-O11':(9,11)}.items():
    print('%-9s %8.4f' % (lab, d(i,j)))
# nearest heavy to H26 and H27
for h in (26,27):
    best=min(((d(h,j), j) for j in range(1,len(atoms)+1) if atoms[j-1][0]!=1 and j!=h))
    print('H%d nearest heavy: atom %d (Z=%d) at %.4f' % (h, best[1], atoms[best[1]-1][0], best[0]))
scf=[ (i+1, lines[i].split()[4]) for i,l in enumerate(lines) if 'SCF Done' in l]
print('last SCF:', scf[-1])
