import numpy as np
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])
def block_at(path, start_line):
    lines = open(path,'rb').read().decode('utf-8','replace').splitlines()
    k = start_line-1+5; atoms=[]
    while k < len(lines):
        if lines[k].strip().startswith('-----'): break
        p = lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms
f='gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log'
a = block_at(f, 49159); b = block_at(f, 51477)
A = np.array([x[1:] for x in a]); B = np.array([x[1:] for x in b])
print('n:', len(a), len(b), 'elements equal:', [x[0] for x in a]==[x[0] for x in b])
print('max|delta| per atom = %.6f A ; mean = %.6f' % (np.abs(A-B).max(), np.abs(A-B).mean()))
# mapped map given by peer (20 pairs 1073->P)
mp = [(4,1),(2,2),(1,3),(32,4),(31,5),(30,6),(29,7),(28,8),(26,9),(27,10),(25,11),(3,25),(6,28),(5,29),(7,30),(12,31),(11,32),(10,33),(9,34),(8,35)]
ap,_ = last_geom('gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log')
A20 = np.array([a[i-1][1:] for i,j in mp]); B20 = np.array([ap[j-1][1:] for i,j in mp])
r,m,det = kabsch(A20,B20); print('mapping#2 heavy20 fit+eval: RMSD=%.4f max=%.4f det=%+.2f' % (r,m,det))
Af = np.array([x[1:] for x in a]); Bf = np.array([ap[j-1][1:] for i,j in [(i,j) for i,j in mp]])
