
import re, sys, numpy as np, hashlib, datetime, os

GRID = "gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
E1028 = -939.312626605
K = 627.509474


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def parse_blocks(path):
    lines = open(path, errors="replace").read().splitlines()
    blocks = []
    scf = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]
        if "SCF Done:" in ln:
            m = re.search(r"=\s*(-?\d+\.\d+)\s+A\.U\.", ln)
            if m:
                scf.append((i + 1, float(m.group(1))))
        if ln.strip().startswith("Standard orientation"):
            hdr = i + 1
            j = i + 5
            els, xyz = [], []
            while j < n and not lines[j].strip().startswith("-----"):
                p = lines[j].split()
                if len(p) >= 6:
                    els.append(p[1])
                    xyz.append([float(p[3]), float(p[4]), float(p[5])])
                j += 1
            blocks.append((hdr, els, np.array(xyz)))
            i = j
        i += 1
    return lines, blocks, scf


def geometry_at(blocks, scf, upto_line):
    e_idx = None
    for k, (ln, e) in enumerate(scf):
        if ln <= upto_line:
            e_idx = k
    if e_idx is None:
        return None, None
    sln = scf[e_idx][0]
    best = None
    for hdr, els, xyz in blocks:
        if hdr < sln:
            best = (hdr, els, xyz)
    return scf[e_idx], best


def kabsch(P, Q):
    Pc = P - P.mean(axis=0)
    Qc = Q - Q.mean(axis=0)
    H = Pc.T @ Qc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    diff = Pc @ R.T - Qc
    per = np.sqrt((diff ** 2).sum(axis=1))
    return float(np.sqrt((per ** 2).mean())), float(per.max()), int(per.argmax()) + 1, float(np.linalg.det(R))


def selfcheck():
    rng = np.random.default_rng(7)
    P = rng.normal(size=(9, 3)) * 2.0
    th = 0.7
    Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1.0]])
    Q = P @ Rz.T + np.array([3.0, -1.5, 2.0])
    a = kabsch(P, Q)
    b = kabsch(P, P * np.array([1.0, 1.0, -1.0]))
    c = kabsch(P, P.copy())
    print("SELFCHECK rot+trans rms=%.3e max=%.3e det=%+.1f" % (a[0], a[1], a[3]))
    print("SELFCHECK mirror    rms=%.4f det=%+.1f" % (b[0], b[3]))
    print("SELFCHECK copy      rms=%.3e det=%+.1f" % (c[0], c[3]))


print("=== script:", os.path.basename(os.path.abspath(__file__)), "sha256:", sha(os.path.abspath(__file__)))
print("=== time:", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
print("=== grid log sha256:", sha(GRID), " lines:", sum(1 for _ in open(GRID, errors="replace")))
selfcheck()

lines, blocks, scf = parse_blocks(GRID)
print("blocks=%d scf=%d" % (len(blocks), len(scf)))
conv = [i + 1 for i, l in enumerate(lines) if l.strip().startswith("Optimization completed")]
print("Optimization completed count:", len(conv))

pts = []
for ln in conv:
    s, g = geometry_at(blocks, scf, ln)
    if s is None or g is None:
        print("  MISSING for line", ln); continue
    hdr, els, xyz = g
    d = lambda a, b: float(np.linalg.norm(xyz[a - 1] - xyz[b - 1]))
    pts.append(dict(opt_line=ln, scf_line=s[0], E=s[1], hdr=hdr, els=els, xyz=xyz,
                    r24=d(2, 4), r2526=d(25, 26), oh=d(10, 27), n4h26=d(4, 26),
                    c2o25=d(2, 25), c2h26=d(2, 26)))

print("\n n  optL   SCFL     E              dE(kcal)  R(2,4) R(25,26) O10-H27 N4-H26 C2-O25 C2-H26")
for k, p in enumerate(pts, 1):
    print("%2d %6d %7d %13.9f %+9.4f  %6.4f %7.4f %7.4f %7.4f %7.4f %7.4f" % (
        k, p["opt_line"], p["scf_line"], p["E"], (p["E"] - E1028) * K,
        p["r24"], p["r2526"], p["oh"], p["n4h26"], p["c2o25"], p["c2h26"]))

print("\n=== span recompute (native logs, same program/lane)")
paths = {
    "P_1061": "gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log",
    "1073": "gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log",
    "1071opt": "ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log",
}
vals = {}
for name, p in paths.items():
    _, _, sc = parse_blocks(p)
    e = min(x[1] for x in sc)
    vals[name] = e
    print("  %-8s scf=%4d min=%.9f last=%.9f dE_vs_1028=%+.4f sha=%s" % (
        name, len(sc), e, sc[-1][1], (e - E1028) * K, sha(p)[:16]))
lo = min(vals.values()); hi = max(vals.values())
print("  span = %.4f kcal/mol (%.9f -> %.9f)" % ((hi - lo) * K, lo, hi))
print("  1071 vs P = %+.4f" % ((vals["1071opt"] - vals["P_1061"]) * K))

if len(pts) >= 14:
    A, B = pts[12], pts[13]
    assert A["els"] == B["els"], "element mismatch"
    heavy = [i for i, e in enumerate(A["els"]) if e.upper() != "H"]
    print("\n=== Kabsch 13 -> 14 (SVD, det=+1, R applied P->Q)")
    for tag, idx in (("heavy%d" % len(heavy), heavy), ("all%d" % len(A["els"]), list(range(len(A["els"]))))):
        rms, mx, at, det = kabsch(A["xyz"][idx], B["xyz"][idx])
        print("  %-7s rms=%.4f max=%.4f worst_atom=%d det=%+.1f" % (tag, rms, mx, idx[at - 1] + 1, det))
