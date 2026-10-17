import math, sys, os

def read_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    at = []
    for i in range(2, 2+n):
        f = L[i].split()
        at.append((f[0], float(f[1]), float(f[2]), float(f[3])))
    return at

def v(a,b): return (b[1]-a[1], b[2]-a[2], b[3]-a[3])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a,a))
def dist(at,i,j): return norm(v(at[i],at[j]))
def angle(at,i,j,k):
    a=v(at[j],at[i]); b=v(at[j],at[k])
    return math.degrees(math.acos(max(-1,min(1,dot(a,b)/(norm(a)*norm(b))))))
def dih(at,i,j,k,l):
    b1=v(at[i],at[j]); b2=v(at[j],at[k]); b3=v(at[k],at[l])
    n1=cross(b1,b2); n2=cross(b2,b3)
    m=cross(n1,b2); m=[x/norm(b2) for x in m]
    x=dot(n1,n2); y=dot(m,n2)
    return math.degrees(math.atan2(y,x))

base = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NY3/E1"
rc = read_xyz(os.path.join(base,"rc_dft_min_working_order.xyz"))

def metrics(at):
    return dict(d_O1C4=dist(at,1,5), Na_O1=dist(at,0,1), Na_O5=dist(at,0,6),
                D_Me=dih(at,7,3,4,5), D_OH=dih(at,0,1,2,10),
                aNaO1H6=angle(at,0,1,2), BD=angle(at,1,5,6),
                C4O5=dist(at,5,6), C4O1=dist(at,5,1))

def passes(m, ref):
    R = rc_m
    c1 = 2.10 <= m['d_O1C4'] <= 2.40
    c2 = abs(m['D_Me']-R['D_Me']) <= 10.0 and abs(m['D_OH']-R['D_OH']) <= 15.0
    c3 = m['Na_O1'] <= 2.60 and abs(m['aNaO1H6']-R['aNaO1H6']) <= 25.0
    return c1,c2,c3

rc_m = metrics(rc)
print("RCref  d_O1C4=%.3f Na_O1=%.3f Na_O5=%.3f D_Me=%.2f D_OH=%.2f aNaO1H6=%.2f BD=%.2f C4O5=%.3f C4O1=%.3f" % (
    rc_m['d_O1C4'],rc_m['Na_O1'],rc_m['Na_O5'],rc_m['D_Me'],rc_m['D_OH'],rc_m['aNaO1H6'],rc_m['BD'],rc_m['C4O5'],rc_m['C4O1']))
print()
print("frame  d_O1C4  Na_O1  Na_O5  D_Me(d)  D_OH(d)  aNaO1H6(d)  BD    c1 c2 c3")
nd = os.path.join(base,"e1_xtb_scan/native_scan_runs/native_scan_0001")
summ=[]
for i in range(1,15):
    p = os.path.join(nd, "point_%04d.xyz" % i)
    m = metrics(read_xyz(p))
    c1,c2,c3 = passes(m, rc_m)
    summ.append((i,m,c1,c2,c3))
    print("p%04d  %.3f  %.3f  %.3f  %.2f(%+.1f)  %.2f(%+.1f)  %.2f(%+.1f)  %.1f  %s %s %s" % (
        i, m['d_O1C4'], m['Na_O1'], m['Na_O5'], m['D_Me'], m['D_Me']-rc_m['D_Me'],
        m['D_OH'], m['D_OH']-rc_m['D_OH'], m['aNaO1H6'], m['aNaO1H6']-rc_m['aNaO1H6'], m['BD'],
        'Y' if c1 else 'n', 'Y' if c2 else 'n', 'Y' if c3 else 'n'))
npass = sum(1 for s in summ if s[2] and s[3] and s[4])
print()
print("frames passing all three hard criteria: %d/14" % npass)
# best combined violation
best=None
for i,m,c1,c2,c3 in summ:
    viol = max(0, 2.10-m['d_O1C4'], m['d_O1C4']-2.40)/0.30 + max(0, abs(m['D_Me']-rc_m['D_Me'])-10)/10.0 + max(0, abs(m['D_OH']-rc_m['D_OH'])-15)/15.0 + max(0, m['Na_O1']-2.60)/0.5 + max(0, abs(m['aNaO1H6']-rc_m['aNaO1H6'])-25)/25.0
    if best is None or viol<best[1]: best=(i,viol)
print("lowest combined normalized violation: p%04d (%.3f)" % best)
# also measure the geometry-construct candidates for cross-check
for f in ["e1_tsguess_rigid_swing_d230.xyz","e1_tsguess_rigid_swing_d220.xyz","e1_tsguess_img04_retorsion.xyz","interp/img_04.xyz","e1_tsguess_xtbscan_p0005.xyz","e1_tsguess_xtbscan_p0006.xyz","e1_tsguess_xtbscan_p0007.xyz"]:
    m = metrics(read_xyz(os.path.join(base,f)))
    c1,c2,c3 = passes(m, rc_m)
    print("CAND %-32s d=%.3f Na_O1=%.3f D_Me=%+.1f D_OH=%+.1f BD=%.1f aNaO1H6=%.1f  -> %s %s %s" % (
        f, m['d_O1C4'], m['Na_O1'], m['D_Me']-rc_m['D_Me'], m['D_OH']-rc_m['D_OH'], m['BD'], m['aNaO1H6']-rc_m['aNaO1H6'],
        'Y' if c1 else 'n', 'Y' if c2 else 'n', 'Y' if c3 else 'n'))
