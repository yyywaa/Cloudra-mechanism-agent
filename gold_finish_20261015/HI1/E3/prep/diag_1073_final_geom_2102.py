import numpy as np, math
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])
def lastgeom_all(path):
    lines = open(path,'rb').read().decode('utf-8','replace').splitlines()
    idx = [i for i,l in enumerate(lines) if ('Standard orientation:' in l or 'Input orientation:' in l)]
    s = idx[-1]; k = s+5; atoms=[]
    while k < len(lines):
        if lines[k].strip().startswith('-----'): break
        p = lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms, s+1
a73, s73 = lastgeom_all('gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log')
ap, sp = lastgeom_all('gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log')
a28, s28 = lastgeom_all('gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log')
mp = {1:3,2:2,3:25,4:1,5:29,6:28,7:30,8:35,9:34,10:33,11:32,12:31,13:14,14:15,15:16,16:12,17:13,18:36,19:24,20:41,21:40,22:39,23:38,24:37,25:11,26:9,27:10,28:8,29:7,30:6,31:5,32:4,33:27,34:23,35:21,36:22,37:19,38:20,39:17,40:18,41:26}
inv = {v:k for k,v in mp.items()}   # E3/P index -> 1073 index
print('1073 last block starts L%d (%d atoms); P L%d; 1028 L%d' % (s73, len(a73), sp, s28))
def d(a,i,j): return math.dist(a[i-1][1:], a[j-1][1:])
def d73(i_e3, j_e3):
    return math.dist(a73[inv[i_e3]-1][1:], a73[inv[j_e3]-1][1:])
pairs = [(2,4,'C2-N4'),(2,25,'C2-O25'),(4,26,'N4-H26'),(25,26,'O25-H26'),(10,27,'O10-H27'),(9,10,'C9-O10'),(9,11,'C9-O11'),(2,3,'C2-O3'),(2,18,'C2-N18')]
print('label           1073(mapped to E3 order)   P(1061)   1028')
for i,j,lab in pairs:
    print('%-12s %10.4f %14.4f %10.4f' % (lab, d73(i,j), d(ap,i,j), d(a28,i,j)))
print('check 1073 atom2->E3:', inv[2], 'atom32->E3:', inv[4])
