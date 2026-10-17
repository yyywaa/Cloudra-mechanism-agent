
import sys, math, re
log = sys.argv[1]; RC = -593.934532807; K = 627.5095
L = open(log, errors='replace').read().splitlines()
RAD = {'H':0.31,'C':0.76,'N':0.71,'O':0.66}
def sym(z): return {1:'H',6:'C',7:'N',8:'O'}[z]
# geometry blocks
blocks = []; i = 0
while i < len(L):
    if ('Input orientation:' in L[i]) or ('Standard orientation:' in L[i]):
        j = i+1; d = 0
        while j < len(L) and d < 2:
            if L[j].strip().startswith('---'): d += 1
            j += 1
        at = []
        while j < len(L):
            t = L[j].split()
            if len(t) == 6 and t[0].isdigit() and t[1].isdigit():
                at.append((sym(int(t[1])), float(t[3]), float(t[4]), float(t[5]))); j += 1
            else: break
        if at: blocks.append((j, at))
        i = j; continue
    i += 1
# converged points
pts = []; scfE = None; scfL = None
for idx, line in enumerate(L, 1):
    if 'SCF Done:' in line:
        m = re.search(r'E\(RB3LYP\)\s*=\s*(-?\d+\.\d+)', line)
        if m: scfE = float(m.group(1)); scfL = idx
    if 'Optimization completed' in line:
        pts.append((idx, line.strip(), scfE, scfL))
def d(a,b,A): return math.dist(A[a-1][1:], A[b-1][1:])
def classify(A):
    n = len(A)
    bonded = set()
    for a in range(1, n+1):
        for b in range(a+1, n+1):
            if d(a,b,A) < RAD[A[a-1][0]] + RAD[A[b-1][0]] + 0.45:
                bonded.add((a,b))
    adj = {k: set() for k in range(1, n+1)}
    for a,b in bonded:
        adj[a].add(b); adj[b].add(a)
    def order(a,b):
        if (min(a,b),max(a,b)) in bonded: return 1
        if adj[a] & adj[b]: return 2
        return 3
    return bonded, order
print('log lines', len(L))
print('%2s %6s %7s %18s %8s %8s %7s %8s %8s %8s %8s %8s' % ('pt','convL','scfL','E(RB3LYP)','R2-18','target','diff','dE_kcal','C2-O3','N18-H27','O3..H27','minsep'))
rows = []
for n,(convL, convTxt, E, scfL) in enumerate(pts, 1):
    cand = [b for b in blocks if b[0] < convL]
    _, A = cand[-1]
    target = 2.6920 - 0.0500*(n-1)
    bonded, order = classify(A)
    pairs = sorted(((d(a,b,A), a, b, order(a,b)) for a in range(1,len(A)+1) for b in range(a+1,len(A)+1)))
    ms = pairs[0]
    bmin = min([p for p in pairs if p[3]==1])
    omin = min([p for p in pairs if p[3]==2])
    nmin = min([p for p in pairs if p[3]==3])
    print('%2d %6d %7d %18.9f %8.4f %8.4f %+7.4f %8.2f %8.4f %8.4f %8.4f %8.4f' % (n, convL, scfL, E, d(2,18,A), target, d(2,18,A)-target, (E-RC)*K, d(2,3,A), d(18,27,A), d(3,27,A), ms[0]))
    print('     contacts: bonded %.4f (%d-%d) | 1-3 %.4f (%d-%d) | nonbonded %.4f (%d-%d) | conv="%s"' % (bmin[0],bmin[1],bmin[2], omin[0],omin[1],omin[2], nmin[0],nmin[1],nmin[2], convTxt))
    rows.append((n, d(2,18,A), target, d(2,18,A)-target, E, scfL, (E-RC)*K, d(2,3,A), d(18,27,A), d(3,27,A), ms[0], bmin, omin, nmin, len(A)))
print()
print('max |diff| =', max(abs(r[3]) for r in rows))
print('first/last R =', rows[0][1], rows[-1][1])
Es = [r[4] for r in rows]
print('E monotonic decreasing with n?', all(Es[i] > Es[i+1] for i in range(len(Es)-1)))
print('E by point:', ', '.join('%.6f' % e for e in Es))
