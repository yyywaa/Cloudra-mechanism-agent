# post-freeze asset: 1071 global-min / parametric uncertainty (never use "last SCF" as min)
p = "/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
K = 627.5095; REF = -939.312626605; P = -939.319540184
ls = open(p).read().splitlines()
rows = [(i + 1, float(l.split('=')[1].split()[0])) for i, l in enumerate(ls) if 'SCF Done' in l]
def d(E): return (E - REF) * K
rows_sorted = sorted(rows, key=lambda t: t[1])
print("lines %d | SCF count %d" % (len(ls), len(rows)))
print("lowest 4:", " | ".join("L%d %.4f" % (n, d(E)) for n, E in rows_sorted[:4]))
print("last     : L%d %.4f  (NOT necessarily the min)" % (rows[-1][0], d(rows[-1][1])))
lo = rows_sorted[0]
print("uncertainty floor = |%.4f - (%.4f)| = %.4f  ->  >= %.2f" % (d(lo[1]), d(P), d(P) - d(lo[1]), d(P) - d(lo[1])))
print("instant spread (1073 -2.7297 vs min) = %.4f" % ((-2.7297) - d(lo[1])))
print("step line:", [l.strip() for l in ls if 'Step number' in l][-1])
print("termination NL/EL:", sum(1 for l in ls if 'Normal termination' in l), sum(1 for l in ls if 'Error termination' in l))
