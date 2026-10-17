
import sys, math
def read_xyz(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    atoms = []
    for line in L[2:2+n]:
        t = line.split()
        atoms.append((t[0], float(t[1]), float(t[2]), float(t[3])))
    return n, atoms, L[1]
def dist(a, b, A): return math.dist(A[a-1][1:], A[b-1][1:])
def minsep(A):
    best = min(((dist(a,b,A), a, b) for a in range(1,len(A)+1) for b in range(a+1,len(A)+1)))
    return best
def kabsch(A, B, idx):
    try:
        import numpy as np
    except Exception:
        return None
    PA = np.array([[A[i-1][1],A[i-1][2],A[i-1][3]] for i in idx])
    PB = np.array([[B[i-1][1],B[i-1][2],B[i-1][3]] for i in idx])
    cA = PA.mean(axis=0); cB = PB.mean(axis=0)
    QA = PA - cA; QB = PB - cB
    H = QB.T @ QA
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    R = Vt.T @ D @ U.T
    QB2 = (R @ QB.T).T
    disp = np.linalg.norm(QB2 - QA, axis=1)
    rmsd = float(np.sqrt((disp**2).mean()))
    return rmsd, float(disp.max()), [float(x) for x in disp]

scan = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_scan_p1_R2692_QMrelaxed.xyz"
guess = "/home/ly/Cloudra-mechanism-agent/ts/ts_0015/path/input_0001/provided.xyz"
seed  = "/home/ly/Cloudra-mechanism-agent/ts/ts_0015/build/input_0001/reactant/seed.xyz"
frames = [("S = E1A_scan_p1_R2692_QMrelaxed (job1070 pt1)", scan),
          ("G = ts_0015 provided.xyz (current_ts_guess)", guess),
          ("R = ts_0015 build reactant seed (= RC_27_opt_frame)", seed)]
data = {}
for name, p in frames:
    n, atoms, comment = read_xyz(p)
    data[name] = (n, atoms, comment)
    print("=== %s\n   file %s\n   natoms %d  comment: %s" % (name, p, n, comment[:110]))
    seq = ' '.join(a[0] for a in atoms)
    print("   elements:", seq)
    print("   R(2,18)=%.4f  R(2,3)=%.4f  R(18,27)=%.4f  R(3,27)=%.4f  R(13,19)=%.4f  R(2,4)=%.4f" %
          (dist(2,18,atoms), dist(2,3,atoms), dist(18,27,atoms), dist(3,27,atoms), dist(13,19,atoms), dist(2,4,atoms)))
    ms = minsep(atoms)
    ms4 = sorted(((dist(a,b,atoms), a, b) for a in range(1,len(atoms)+1) for b in range(a+1,len(atoms)+1)))[:4]
    print("   minsep %.4f (%d-%d) ; tightest4: %s" % (ms[0], ms[1], ms[2], ' | '.join('%.4f %d-%d'%(m[0],m[1],m[2]) for m in ms4)))
names = [n for n,_ in frames]
import itertools
for ia, ib in itertools.combinations(range(len(names)), 2):
    nmA, nmB = names[ia], names[ib]
    n0, A0, _ = data[nmA]
    n1, B1, _ = data[nmB]
    print("\n--- compare %s (reference) vs %s" % (nmA, nmB))
    print("    natoms equal:", n0 == n1, "| element sequence equal:", all(A0[i][0]==B1[i][0] for i in range(min(n0,n1))))
    heavy = [i+1 for i in range(n0) if A0[i][0] != 'H']
    allidx = list(range(1, n0+1))
    for label, idx in (("all 27 atoms (incl. H)", allidx), ("heavy atoms only (%d)" % len(heavy), heavy)):
        r = kabsch(A0, B1, idx)
        if r is None:
            print("    %s: numpy unavailable" % label); continue
        rmsd, mx, disp = r
        top = sorted(((d, i+1) for i, d in enumerate(disp)), reverse=True)[:4]
        print("    %s: RMSD %.3f A, max |dr| %.3f A, top displ: %s" % (label, rmsd, mx, ' | '.join('%.3f atom%d'%(d,i) for d,i in top)))
