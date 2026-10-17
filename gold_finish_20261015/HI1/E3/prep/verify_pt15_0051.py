
import re, numpy as np, hashlib, datetime, os
GRID = "gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
E1028 = -939.312626605
K = 627.509474

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def parse(path):
    lines = open(path, errors="replace").read().splitlines()
    blocks, scf = [], []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if "SCF Done:" in ln:
            m = re.search(r"=\s*(-?\d+\.\d+)\s+A\.U\.", ln)
            if m:
                scf.append((i + 1, float(m.group(1))))
        if ln.strip().startswith("Standard orientation"):
            j = i + 5
            zs, xyz = [], []
            while j < n and not lines[j].strip().startswith("-----"):
                p = lines[j].split()
                if len(p) >= 6:
                    zs.append(int(p[1])); xyz.append([float(p[3]), float(p[4]), float(p[5])])
                j += 1
            blocks.append((i + 1, zs, np.array(xyz)))
            i = j
        i += 1
    return lines, blocks, scf

def kabsch(P, Q):
    Pc, Qc = P - P.mean(axis=0), Q - Q.mean(axis=0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    per = np.sqrt(((Pc @ R.T - Qc) ** 2).sum(axis=1))
    return float(np.sqrt((per ** 2).mean())), float(per.max()), int(per.argmax()) + 1, float(np.linalg.det(R))

def selfcheck():
    rng = np.random.default_rng(31)
    P = rng.normal(size=(9, 3)) * 2.1
    Q = P @ np.array([[0.6, -0.8, 0], [0.8, 0.6, 0], [0, 0, 1.0]]).T + np.array([-1.0, 0.5, 2.0])
    a = kabsch(P, Q); b = kabsch(P, P * np.array([1.0, 1.0, -1.0])); c = kabsch(P, P.copy())
    print("SELFCHECK rot+trans rms=%.3e | mirror rms=%.4f | copy rms=%.3e | det all %+.1f" % (a[0], b[0], c[0], a[3]))

print("=== script:", os.path.basename(os.path.abspath(__file__)), "sha256:", sha(os.path.abspath(__file__)))
print("=== time:", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
print("=== log sha256:", sha(GRID), "lines:", sum(1 for _ in open(GRID, errors="replace")), "bytes:", os.path.getsize(GRID))
selfcheck()
lines, blocks, scf = parse(GRID)
conv = [i + 1 for i, l in enumerate(lines) if l.strip().startswith("Optimization completed")]
print("conv=", len(conv), " scf=", len(scf))
pts = []
for ln in conv:
    k = None
    for idx, (sln, e) in enumerate(scf):
        if sln <= ln:
            k = idx
    sln, e = scf[k]
    best = None
    for hdr, zs, xyz in blocks:
        if hdr < sln:
            best = (hdr, zs, xyz)
    zs, xyz = best[1], best[2]
    d = lambda a, b: float(np.linalg.norm(xyz[a - 1] - xyz[b - 1]))
    pts.append(dict(opt=ln, scf=sln, E=e, hdr=best[0], zs=zs, xyz=xyz,
                    r24=d(2, 4), rp=d(25, 26), r1027=d(10, 27), r426=d(4, 26), r225=d(2, 25), r226=d(2, 26)))
print("\n n  optL    SCFL     E              dE       R(2,4) R(25,26) O10H27 N4H26 C2O25 C2H26")
for k, p in enumerate(pts, 1):
    print("%2d %7d %7d %13.9f %+9.4f %7.4f %7.4f %7.4f %7.4f %6.4f %6.4f" % (
        k, p["opt"], p["scf"], p["E"], (p["E"] - E1028) * K, p["r24"], p["rp"], p["r1027"], p["r426"], p["r225"], p["r226"]))
print("\n=== col3 along R(2,4) (proton axis fixed at 1.4693)")
col3 = [k for k, p in enumerate(pts, 1) if abs(p["rp"] - 1.4693) < 1e-3]
for k in col3:
    p = pts[k - 1]
    nb = [pts[j - 1] for j in (k - 1, k + 1) if 1 <= j <= len(pts) and abs(pts[j - 1]["rp"] - 1.4693) < 1e-3]
    if len(nb) == 2:
        lo, hi = nb
        print("  pt%d R(2,4)=%.4f dE=%+.4f | neighbour %.4f -> %+.4f (diff %+.4f) ; %.4f -> %+.4f (diff %+.4f) => %s" % (
            k, p["r24"], (p["E"] - E1028) * K, lo["r24"], (lo["E"] - E1028) * K, (p["E"] - lo["E"]) * K,
            hi["r24"], (hi["E"] - E1028) * K, (p["E"] - hi["E"]) * K,
            "LOCAL MAX" if (p["E"] > lo["E"] and p["E"] > hi["E"]) else "not-extremum"))
    else:
        print("  pt%d R(2,4)=%.4f dE=%+.4f | one side missing -> not judgeable" % (k, p["r24"], (p["E"] - E1028) * K))
print("\n=== Kabsch adjacent pairs #12-13, #13-14, #14-15 (heavy20 and all-41)")
for a, b in ((12, 13), (13, 14), (14, 15)):
    if b > len(pts):
        print("  #%d->#%d not available" % (a, b)); continue
    A, B = pts[a - 1], pts[b - 1]
    assert A["zs"] == B["zs"], "element mismatch"
    heavy = [i for i, z in enumerate(A["zs"]) if z != 1]
    rh = kabsch(A["xyz"][heavy], B["xyz"][heavy]); ra = kabsch(A["xyz"], B["xyz"])
    print("  #%d->#%d heavy20 %.4f / %.4f / a%d det %+.1f | all-41 %.4f / %.4f / a%d det %+.1f" % (
        a, b, rh[0], rh[1], heavy[rh[2] - 1] + 1, rh[3], ra[0], ra[1], ra[2], ra[3]))
