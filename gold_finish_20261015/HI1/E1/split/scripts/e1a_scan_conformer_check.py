
import sys, math, re
import numpy as np
log = sys.argv[1]
L = open(log, errors='replace').read().splitlines()
def sym(z): return {1:'H',6:'C',7:'N',8:'O'}[z]
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
pts = [idx for idx, line in enumerate(L,1) if 'Optimization completed' in line]
frames = []
for n, convL in enumerate(pts, 1):
    _, A = [b for b in blocks if b[0] < convL][-1]
    frames.append(A)
heavy = [i for i,a in enumerate(frames[0]) if a[0] != 'H']
def kabsch(A,B,idx):
    PA = np.array([[A[i][1],A[i][2],A[i][3]] for i in idx]); PB = np.array([[B[i][1],B[i][2],B[i][3]] for i in idx])
    QA = PA-PA.mean(0); QB = PB-PB.mean(0)
    H = QB.T@QA; U,S,Vt = np.linalg.svd(H)
    dd = np.sign(np.linalg.det(Vt.T@U.T)); R = Vt.T@np.diag([1,1,dd])@U.T
    QB2 = (R@QB.T).T; disp = np.linalg.norm(QB2-QA,axis=1)
    return float(np.sqrt((disp**2).mean())), float(disp.max()), int(np.argmax(disp))+1
def dih(A,a,b,c,d):
    p = [np.array(A[i-1][1:]) for i in (a,b,c,d)]
    b0 = p[0]-p[1]; b1 = p[2]-p[1]; b2 = p[3]-p[2]
    b1n = b1/np.linalg.norm(b1)
    v = b0 - np.dot(b0,b1n)*b1n; w = b2 - np.dot(b2,b1n)*b1n
    x = np.dot(v,w); y = np.dot(np.cross(b1n,v),w)
    return math.degrees(math.atan2(y,x))
print('heavy atoms used for RMSD: %d (work indices %s)' % (len(heavy), [i+1 for i in heavy]))
for n in range(1, len(frames)):
    rmsd, mx, ai = kabsch(frames[n-1], frames[n], heavy)
    print('pt%d -> pt%d: heavy RMSD %.3f A, max |dr| %.3f A (atom %d) | O3..H27 %.3f -> %.3f | nonbonded-min-class change' % (n, n+1, rmsd, mx, [i+1 for i in heavy][ai-1], math.dist(frames[n-1][2][1:], frames[n-1][26][1:]), math.dist(frames[n][2][1:], frames[n][26][1:])))
# dihedral drift marker: C2-C3-C1?-? use ring pucker proxies: N18-C14-C15-C16 and N18-C14-C17-C16
for n,A in enumerate(frames,1):
    print('pt%2d: dihedral N18-C14-C15-C16 %8.1f deg | C2-C3-C14-N18 %8.1f deg | O3-C2-N18-C14 %8.1f' % (n, dih(A,18,14,15,16), dih(A,2,4,14,18) if True else 0.0, dih(A,3,2,18,14)))
