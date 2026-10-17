import re, sys, math, itertools
path = sys.argv[1]
L = open(path, errors="replace").read().splitlines()
# collect converged frames: each time we see "Optimization completed.", take the nearest preceding Input orientation block
frames = []
for i, l in enumerate(L):
    if "Optimization completed." in l:
        j = i
        while j > 0 and "Input orientation" not in L[j]:
            j -= 1
        start = j + 5
        at = []
        while start < len(L) and len(at) < 60:
            p = L[start].split()
            if len(p) != 6 or not p[0].isdigit(): break
            at.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
            start += 1
        frames.append((i+1, at))
print("converged_frames", len(frames), "natoms", [len(a) for _, a in frames])
def rmsd(A, B, idx):
    num = sum(math.dist(A[i][2:], B[i][2:]) ** 2 for i in idx)
    return math.sqrt(num / len(idx))
if len(frames) >= 5:
    A = {a[0]: a for a in frames[3][1]}
    B = {a[0]: a for a in frames[4][1]}
    heavy = [k for k in A if A[k][1] != 1]
    print("pt4(conv L%d) vs pt5(conv L%d): all-atom coord-RMSD %.3f A, heavy %.3f A" % (frames[3][0], frames[4][0], rmsd(frames[3][1], frames[4][1], range(len(frames[3][1]))), rmsd(frames[3][1], frames[4][1], [k-1 for k in heavy])))
    worst = sorted(((math.dist(A[k][2:], B[k][2:]), k) for k in A), reverse=True)[:4]
    print("largest per-atom shifts:", [(round(d,3), k) for d, k in worst])
