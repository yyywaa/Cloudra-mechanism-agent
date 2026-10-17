import numpy as np, math
exec(open('gold_finish_20261015/HI1/E3/prep/diag_kabsch_validate_2043.py').read().split('# ---------- 1)')[0])

def block_at(path, start_line):
    lines = open(path,'rb').read().decode('utf-8','replace').splitlines()
    i = start_line-1
    k = i+5; atoms=[]
    while k < len(lines):
        if lines[k].strip().startswith('-----'): break
        p = lines[k].split()
        if len(p)==6 and p[0].isdigit(): atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        k+=1
    return atoms

a73 = block_at('gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log', 49159)
a28,_ = last_geom('gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log')
ap,_ = last_geom('gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log')
Z73 = [a[0] for a in a73]; Z28=[a[0] for a in a28]; Zp=[a[0] for a in ap]
print('n atoms 1073/1028/P:', len(a73), len(Z28), len(Zp))
print('Z seq equal 1073 vs 1028 (index-wise):', Z73 == Z28)
print('Z seq equal 1073 vs P    (index-wise):', Z73 == Zp)
print('Z73 =', Z73)
print('Z28 =', Z28)
# formula counts
from collections import Counter
print('counts 1073:', dict(Counter(Z73)), ' 1028:', dict(Counter(Z28)))
