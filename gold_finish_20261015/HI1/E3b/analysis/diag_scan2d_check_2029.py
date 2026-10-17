import sys, math
seed = [l.split() for l in open(sys.argv[1]).read().splitlines()[2:] if l.strip()]
gjf  = [l.split() for l in open(sys.argv[2]).read().splitlines()[7:] if l.strip() and l.split()[0][0].isalpha()]
print("seed", len(seed), "gjf", len(gjf))
n = min(len(seed), len(gjf))
same = all(seed[i][0] == gjf[i][0] for i in range(n))
mx = max(abs(float(seed[i][k]) - float(gjf[i][k])) for i in range(n) for k in (1,2,3))
print("elem_identical", same, "max_abs_dev", round(mx, 6))