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
mp = {1:3,2:2,3:25,4:1,5:29,6:28,7:30,8:35,9:34,10:33,11:32,12:31,25:11,26:9,27:10,28:8,29:7,30:6,31:5,32:4}
A = np.array([a73[i-1][1:] for i,j in mp.items()])
B = np.array([ap[j-1][1:] for i,j in mp.items()])
ca = A.mean(0); cb = B.mean(0)
H = (A-ca).T @ (B-cb)
U,S,Vt = np.linalg.svd(H); d = np.sign(np.linalg.det(Vt.T@U.T))
R = Vt.T @ np.diag([1.0,1.0,d]) @ U.T
dev = np.linalg.norm((A-ca)@R.T - (B-cb), axis=1)
keys = list(mp.items())
order = np.argsort(-dev)[:5]
for o in order:
    i,j = keys[o]
    print('1073 atom %2d (Z=%d) <-> P atom %2d (Z=%d) : dev %.4f' % (i, a73[i-1][0], j, ap[j-1][0], dev[o]))
print('RMSD=%.4f max=%.4f det=%+.2f' % (np.sqrt((dev**2).mean()), dev.max(), np.linalg.det(R)))
