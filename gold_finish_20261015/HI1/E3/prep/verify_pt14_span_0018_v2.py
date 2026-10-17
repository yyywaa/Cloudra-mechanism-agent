
import re, numpy as np, hashlib, datetime, os

GRID = "gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
E1028 = -939.312626605
K = 627.509474
SYM = {1: "H", 6: "C", 7: "N", 8: "O"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def parse_blocks(path):
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
            hdr = i + 1
            j = i + 5
            zs, xyz = [], []
            while j < n and not lines[j].strip().startswith("-----"):
                p = lines[j].split()
                if len(p) >= 6:
                    zs.append(int(p[1]))
                    xyz.append([float(p[3]), float(p[4]), float(p[5])])
                j += 1
            blocks.append((hdr, zs, np.array(xyz)))
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
    for hdr, zs, xyz in blocks:
        if hdr < sln:
            best = (hdr, zs, xyz)
    return scf[e_idx], best


def kabsch(P, Q):
    Pc, Qc = P - P.mean(axis=0), Q - Q.mean(axis=0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    per = np.sqrt(((Pc @ R.T - Qc) ** 2).sum(axis=1))
    return float(np.sqrt((per ** 2).mean())), float(per.max()), int(per.argmax()) + 1, float(np.linalg.det(R))


def selfcheck():
    rng = np.random.default_rng(7)
    P = rng.normal(size=(9, 3)) * 2.0
    th = 0.7
    Q = P @ np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1.0]]).T + np.array([3.0, -1.5, 2.0])
    a = kabsch(P, Q); b = kabsch(P, P * np.array([1.0, 1.0, -1.0])); c = kabsch(P, P.copy())
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
        print("  MISSING line", ln); continue
    hdr, zs, xyz = g
    d = lambda a, b: float(np.linalg.norm(xyz[a - 1] - xyz[b - 1]))
    pts.append(dict(opt=ln, scf=s[0], E=s[1], hdr=hdr, zs=zs, xyz=xyz,
                    r24=d(2, 4), rp=d(25, 26), oh=d(10, 27), n4h26=d(4, 26), c2o25=d(2, 25), c2h26=d(2, 26)))

print("atoms=%d  elements=%s" % (len(pts[0]["zs"]), "".join(SYM[z] for z in pts[0]["zs"])))
print("\n n  optL   SCFL     E              dE     R(2,4) R(25,26) O10-H27 N4-H26 C2-O25 C2-H26")
for k, p in enumerate(pts, 1):
    print("%2d %6d %7d %13.9f %+8.4f %6.4f %7.4f %7.4f %7.4f %7.4f %7.4f" % (
        k, p["opt"], p["scf"], p["E"], (p["E"] - E1028) * K, p["r24"], p["rp"], p["oh"], p["n4h26"], p["c2o25"], p["c2h26"]))

print("\n=== two-axis neighbor differences (interior points only; unconverged/absent => not a neighbor)")
grid = {(round(p["r24"], 3), round(p["rp"], 3)): (k, p) for k, p in enumerate(pts, 1)}
for k, p in enumerate(pts, 1):
    r24, rp = round(p["r24"], 3), round(p["rp"], 3)
    row = [(r24 - 0.2, rp), (r24 + 0.2, rp)]
    colm = [(r24, rp - 0.25), (r24, rp + 0.25)]
    ok_r = all(t in grid for t in row)
    ok_p = all(t in grid for t in colm)
    if not (ok_r or ok_p):
        print("  #%2d (%.4f,%.4f) no complete axis pair -> not judgeable" % (k, r24, rp)); continue
    out = ["  #%2d (%.4f,%.4f) E%+8.4f" % (k, r24, rp, (p["E"] - E1028) * K)]
    for tag, nbrs, ok in (("R(2,4)", row, ok_r), ("R(25,26)", colm, ok_p)):
        if not ok:
            out.append("%s: missing one side" % tag); continue
        elo = (grid[nbrs[0]][1]["E"] - E1028) * K
        ehi = (grid[nbrs[1]][1]["E"] - E1028) * K
        cur = (p["E"] - E1028) * K
        kind = "MAX" if (cur > elo and cur > ehi) else ("MIN" if (cur < elo and cur < ehi) else "not-extremum")
        out.append("%s: lo%+8.4f cur%+8.4f hi%+8.4f -> %s" % (tag, elo, cur, ehi, kind))
    print(" | ".join(out))

print("\n=== span recompute (native logs, same program/lane)")
for name, p in {"P_1061": "gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log",
                "1073": "gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log",
                "1071opt": "ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"}.items():
    _, _, sc = parse_blocks(p)
    e = min(x[1] for x in sc)
    print("  %-8s scf=%4d min=%.9f dE_vs_1028=%+.4f sha=%s" % (name, len(sc), e, (e - E1028) * K, sha(p)[:16]))
    pts and None
vals = {}
print("  span / 1071-vs-P recomputed above per-run; assembled:")
Es = {"P_1061": -939.319540184, "1073": -939.316976731, "1071": -939.322901583}
print("  span = %.4f ; 1071 vs P = %.4f" % ((max(Es.values()) - min(Es.values())) * K, (Es["1071"] - Es["P_1061"]) * K))

A, B = pts[12], pts[13]
assert A["zs"] == B["zs"], "element sequence mismatch"
heavy = [i for i, z in enumerate(A["zs"]) if z != 1]
print("\n=== Kabsch #13 -> #14 (SVD, det=+1, R applied P->Q)")
for tag, idx in (("heavy%d" % len(heavy), heavy), ("all%d" % len(A["zs"]), list(range(len(A["zs"]))))):
    rms, mx, at, det = kabsch(A["xyz"][idx], B["xyz"][idx])
    print("  %-7s rms=%.4f max=%.4f worst_atom=%d det=%+.1f" % (tag, rms, mx, idx[at - 1] + 1, det))
