import numpy as np, math
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])
def block_at(path, start_line):
    lines = open(path,'rb').read().decode('utf-8','replace').splitlines()
    i = start_line-1; k = i+5; atoms=[]
    while k < len(lines):
        if lines[k].strip().startswith('-----'): break
        p = lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms
a73 = block_at('gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log', 49159)
ap,_ = last_geom('gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log')
mp = {1:3,2:2,3:25,4:1,5:29,6:28,7:30,8:35,9:34,10:33,11:32,12:31,13:14,14:15,15:16,16:12,17:13,18:36,19:24,20:41,21:40,22:39,23:38,24:37,25:11,26:9,27:10,28:8,29:7,30:6,31:5,32:4,33:27,34:23,35:21,36:22,37:19,38:20,39:17,40:18,41:26}
print('n map entries:', len(mp), 'src coverage ok:', sorted(mp)==list(range(1,42)), 'tgt bijection:', sorted(mp.values())==list(range(1,42)))
bad = [(i,j,a73[i-1][0],ap[j-1][0]) for i,j in mp.items() if a73[i-1][0]!=ap[j-1][0]]
print('element mismatches:', bad)
A = np.array([a73[i-1][1:] for i,j in mp.items()]); B = np.array([ap[j-1][1:] for i,j in mp.items()])
r,m,det = kabsch(A,B); print('ALL-41 with supplied map: RMSD=%.4f max=%.4f det=%+.2f' % (r,m,det))
hv = [k for k,(i,j) in enumerate(mp.items()) if a73[i-1][0]!=1]
r2,m2,d2 = kabsch(A[hv],B[hv]); print('heavy-20 subset: RMSD=%.4f max=%.4f det=%+.2f' % (r2,m2,d2))
