
import re, numpy as np, hashlib, datetime, os

CONT1 = "gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.log"
K = 627.509474
E_PT1 = -939.297687579      # cont1 pt1
E_MAIN1 = -939.308205969    # 主扫 pt1


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
                    zs.append(int(p[1])); xyz.append([float(p[3]), float(p[4]), float(p[5])])
                j += 1
            blocks.append((hdr, zs, np.array(xyz)))
            i = j
        i += 1
    return lines, blocks, scf


def geometry_at(blocks, scf, upto):
    e = None
    for k, (ln, _) in enumerate(scf):
        if ln <= upto:
            e = k
    if e is None:
        return None, None
    sln = scf[e][0]
    best = None
    for hdr, zs, xyz in blocks:
        if hdr < sln:
            best = (hdr, zs, xyz)
    return scf[e], best


def kabsch(P, Q):
    Pc, Qc = P - P.mean(axis=0), Q - Q.mean(axis=0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    per = np.sqrt(((Pc @ R.T - Qc) ** 2).sum(axis=1))
    return float(np.sqrt((per ** 2).mean())), float(per.max()), int(per.argmax()) + 1, float(np.linalg.det(R))


def selfcheck():
    rng = np.random.default_rng(11)
    P = rng.normal(size=(11, 3)) * 1.7
    th = -0.9
    Q = P @ np.array([[np.cos(th), 0, np.sin(th)], [0, 1.0, 0], [-np.sin(th), 0, np.cos(th)]], float).T + np.array([-2.0, 4.0, 0.5])
    a = kabsch(P, Q); b = kabsch(P, P * np.array([1.0, -1.0, 1.0])); c = kabsch(P, P.copy())
    print("SELFCHECK rot+trans rms=%.3e det=%+.6f" % (a[0], a[3]))
    print("SELFCHECK mirror    rms=%.4f det=%+.6f" % (b[0], b[3]))
    print("SELFCHECK copy      rms=%.3e det=%+.6f" % (c[0], c[3]))


print("=== script:", os.path.basename(os.path.abspath(__file__)), "sha256:", sha(os.path.abspath(__file__)))
print("=== time:", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
print("=== cont1 log sha256:", sha(CONT1), " lines:", sum(1 for _ in open(CONT1, errors="replace")), " bytes:", os.path.getsize(CONT1))
selfcheck()

lines, blocks, scf = parse_blocks(CONT1)
conv = [i + 1 for i, l in enumerate(lines) if l.strip().startswith("Optimization completed")]
print("blocks=%d scf=%d  Optimization completed=%d  Stationary point found=%d" % (
    len(blocks), len(scf), len(conv), sum(1 for l in lines if "Stationary point found" in l)))
term = [l for l in lines if "Normal termination" in l or "Error termination" in l]
print("termination lines:", len(term), term[:2])

pts = []
for ln in conv:
    s, g = geometry_at(blocks, scf, ln)
    if s is None or g is None:
        print("  MISSING line", ln); continue
    hdr, zs, xyz = g
    d = lambda a, b: float(np.linalg.norm(xyz[a - 1] - xyz[b - 1]))
    pts.append(dict(opt=ln, scf=s[0], E=s[1], hdr=hdr, zs=zs, xyz=xyz,
                    r129=d(1, 29), r24=d(2, 4), r1124=d(11, 24), oh=d(10, 27), n4h26=d(4, 26)))

print("\natoms=%d" % len(pts[0]["zs"]))
print(" n  optL   SCFL     E              dE_vs_cont1pt1  dE_vs_main_pt1   R(1,29) R(2,4) R(11,24) O10-H27 R(4,26)")
for k, p in enumerate(pts, 1):
    print("%2d %6d %7d %13.9f %+13.4f %+14.4f  %7.4f %6.4f %7.4f %7.4f %7.4f" % (
        k, p["opt"], p["scf"], p["E"], (p["E"] - E_PT1) * K, (p["E"] - E_MAIN1) * K,
        p["r129"], p["r24"], p["r1124"], p["oh"], p["n4h26"]))

if len(pts) >= 2:
    A, B = pts[-2], pts[-1]
    assert A["zs"] == B["zs"], "element mismatch"
    heavy = [i for i, z in enumerate(A["zs"]) if z != 1]
    print("\n=== Kabsch pt%d -> pt%d (SVD, det=+1, R applied P->Q)" % (len(pts) - 1, len(pts)))
    for tag, idx in (("heavy%d" % len(heavy), heavy), ("all%d" % len(A["zs"]), list(range(len(A["zs"]))))):
        rms, mx, at, det = kabsch(A["xyz"][idx], B["xyz"][idx])
        print("  %-7s rms=%.4f max=%.4f worst_atom=%d det=%+.1f" % (tag, rms, mx, idx[at - 1] + 1, det))
    print("  (ref) pt1->pt2 branch switch heavy20 0.9859 / max 1.5271 / atom 28 ; pt2->pt3 0.0937 / 0.1786 / 3")
