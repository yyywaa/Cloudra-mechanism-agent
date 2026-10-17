import re, sys, math
path = sys.argv[1]
L = open(path, errors="replace").read().splitlines()
seg = []
cur = None
pat = re.compile(r"on scan point\s+(\d+) out of\s+(\d+)")
for i, l in enumerate(L):
    m = pat.search(l)
    if m and "Step number" in l:
        n = int(m.group(1))
        if cur is None or n != cur:
            cur = n
            seg.append({"pt": n, "lines": [], "start": i+1})
    if cur is not None:
        seg[-1]["lines"].append(l)
def frame(lines):
    idx = [i for i, l in enumerate(lines) if "Input orientation" in l]
    if not idx: return None
    start = idx[-1] + 5
    at = []
    while start < len(lines) and len(at) < 60:
        p = lines[start].split()
        if len(p) != 6 or not p[0].isdigit(): break
        at.append((int(p[0]), int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        start += 1
    return at
def d(a, b): return math.dist(a[2:], b[2:])
RC = -593.934532807
H = 627.509474
print("pt conv(OPT) lastE Ry(R2-18) R(2-3) R(18-27) minsep  dE_kcal")
for s in seg:
    txt = "\n".join(s["lines"])
    conv = "Optimization completed." in txt
    es = [float(m.group(1)) for m in re.finditer(r"SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)", txt)]
    e = es[-1] if es else None
    at = frame(s["lines"])
    if not at: 
        print(s["pt"], conv, e); continue
    A = {a[0]: a for a in at}
    r2_18 = d(A[2], A[18]); r2_3 = d(A[2], A[3]); r18_27 = d(A[18], A[27]) if 27 in A else float('nan')
    mn = min(d(x, y) for i, x in enumerate(at) for y in at[i+1:])
    print("%2d  %-5s %s  %.4f  %.4f  %.4f  %.4f  %+.2f" % (s["pt"], conv, ("%.9f" % e) if e else "-", r2_18, r2_3, r18_27, mn, (e - RC) * H if e else float('nan')))
print("natoms_last_frame", len(frame(seg[-1]["lines"])) if frame(seg[-1]["lines"]) else 0)
