import math, numpy as np
exec(open('HI1/E2/forensic/e2_cont1_geomcheck_2340.py').read().split("A = get(")[0])
A = get('HI1/E2/scan_1d/build/E2_1D_scan_cont1.log', 3023)   # cont1 pt1 收敛帧
B8 = get('HI1/E2/scan_1d/build/E2_1D_scan.log', 85370)        # 主扫 pt8 收敛帧
def rep(tag, X, Y):
    P = [a[2:] for a in X if a[1] != 1]; Q = [b[2:] for b in Y if b[1] != 1]
    r = kabsch_rmsd(P, Q)
    Pa = [a[2:] for a in X]; Qa = [b[2:] for b in Y]
    r41 = kabsch_rmsd(Pa, Qa)
    print('%s heavy20 rmsd=%.4f max=%.4f worst=%d det=%.6f | all41 rmsd=%.4f max=%.4f worst=%d' % (tag, r[0], r[1], r[2], r[3], r41[0], r41[1], r41[2]))
rep('cont1pt1(conv) vs 主扫pt8(conv):', A, B8)
def d(a, b, at):
    D = {x[0]: x for x in at}
    return math.dist(D[a][2:], D[b][2:])
print('cont1 pt1 conv: R(1,29)=%.4f R(28,24)=%.4f R(11,24)=%.4f' % (d(1,29,A), d(28,24,A), d(11,24,A)))
