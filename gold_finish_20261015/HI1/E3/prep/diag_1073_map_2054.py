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
bad = [(i,j,a73[i-1][0],ap[j-1][0]) for i,j in mp.items() if a73[i-1][0] != ap[j-1][0]]
print('element-consistency of supplied map (mismatches):', bad)
A = [a73[i-1][1:] for i,j in mp.items()]
B = [ap[j-1][1:] for i,j in mp.items()]
r, m, det = kabsch(A, B)
print('REPRO with supplied map: heavy n=20 RMSD=%.4f max=%.4f det=%+.2f' % (r, m, det))
print('worst pair (1073 idx -> P idx):', list(mp.items())[int(np.argmax([np.linalg.norm(np.array(a)-np.array(b)) for a,b in zip(A,B)]))])
# ratio check: is 2.2976 consistent with distance-spectrum within mapped subset?
D73 = np.array([[np.linalg.norm(np.array(A[i])-np.array(A[j])) for j in range(20)] for i in range(20)])
DP  = np.array([[np.linalg.norm(np.array(B[i])-np.array(B[j])) for j in range(20)] for i in range(20)])
iu = np.triu_indices(20,1)
print('mapped-subset pair-distance |dD| mean=%.4f max=%.4f' % (np.abs(D73-DP)[iu].mean(), np.abs(D73-DP)[iu].max()))
