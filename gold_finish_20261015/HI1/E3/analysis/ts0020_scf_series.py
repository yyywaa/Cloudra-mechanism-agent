# post-freeze asset: 1071 (ts/ts_0020) full SCF series vs 1028 reference, read-only
p = "/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
K = 627.5095; E1028 = -939.312626605
ls = open(p).read().splitlines()
rows = [(i + 1, float(l.split('=')[1].split()[0])) for i, l in enumerate(ls) if 'SCF Done' in l]
print("lines", len(ls), "SCF count", len(rows))
tail = rows[-8:]
for n, E in tail:
    print("  L%-7d %.9f  %+8.4f" % (n, E, (E - E1028) * K))
vals = [(E - E1028) * K for _, E in rows]
lo = min(range(len(rows)), key=lambda i: vals[i]); hi = max(range(len(rows)), key=lambda i: vals[i])
print("lowest  L%d %.4f ; highest-of-all L%d %.4f" % (rows[lo][0], vals[lo], rows[hi][0], vals[hi]))
print("band over last 10 SCF: %.4f .. %.4f" % (min(vals[-10:]), max(vals[-10:])))
print("term NL/EL:", sum(1 for l in ls if 'Normal termination' in l), sum(1 for l in ls if 'Error termination' in l))
for i, l in enumerate(ls, 1):
    if 'Optimization stopped' in l or 'Number of steps exceeded' in l or 'Stationary point found' in l:
        print("  marker L%d: %s" % (i, l.strip()))
