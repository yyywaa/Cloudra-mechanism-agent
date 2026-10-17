# post-freeze asset: probe every geometry frame of 1074 after scan#6 to establish traversal order (serpentine vs grid-reset)
import numpy as np
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
ls = open(p).read().splitlines()
start = [i for i, l in enumerate(ls) if 'Optimization completed' in l][-1]
def blocks_from(i0):
    out = []
    for h in range(i0, len(ls)):
        if 'Standard orientation' not in ls[h]:
            continue
        d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
        if len(d) < 2:
            continue
        a = []; k = d[1] + 1; ok = True
        while not ls[k].strip().startswith('-----'):
            q = ls[k].split()
            if len(q) < 6:
                ok = False; break
            a.append((float(q[3]), float(q[4]), float(q[5]))); k += 1
        if ok and len(a) == 41:
            out.append((h + 1, np.array(a)))
    return out
bl = blocks_from(start)
print("frames after scan#6:", len(bl))
for h, X in bl:
    scf = [k for k in range(h - 1, 0, -1) if 'SCF Done' in ls[k]]
    E = float(ls[scf[0]].split('=')[1].split()[0]) if scf else float('nan')
    d = lambda u, v: float(np.linalg.norm(X[u-1] - X[v-1]))
    step = [k for k in range(h, min(h + 400, len(ls))) if 'Step number' in ls[k]]
    st = ls[step[0]].strip() if step else ''
    print("hdr L%d R(2,4)=%.4f R(25,26)=%.4f R(4,26)=%.4f R(2,25)=%.4f E=%.9f | %s" % (h, d(2, 4), d(25, 26), d(4, 26), d(2, 25), E, st))
