
import re, numpy as np, hashlib, datetime, os

MAIN = "gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
CONT = "gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.log"
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


def frames(path):
    lines, blocks, scf = parse(path)
    conv = [i + 1 for i, l in enumerate(lines) if l.strip().startswith("Optimization completed")]
    out = []
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
        out.append(dict(opt=ln, scf=sln, E=e, hdr=best[0], zs=best[1], xyz=best[2]))
    return out


def kabsch(P, Q):
    Pc, Qc = P - P.mean(axis=0), Q - Q.mean(axis=0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    per = np.sqrt(((Pc @ R.T - Qc) ** 2).sum(axis=1))
    return float(np.sqrt((per ** 2).mean())), float(per.max()), int(per.argmax()) + 1, float(np.linalg.det(R))


def selfcheck():
    rng = np.random.default_rng(23)
    P = rng.normal(size=(13, 3)) * 1.3
    Q = P @ np.array([[1.0, 0, 0], [0, np.cos(0.4), -np.sin(0.4)], [0, np.sin(0.4), np.cos(0.4)]]).T + np.array([1.0, 2.0, -3.0])
    a = kabsch(P, Q); b = kabsch(P, P * np.array([-1.0, 1.0, 1.0])); c = kabsch(P, P.copy())
    print("SELFCHECK rot+trans rms=%.3e det=%+.6f | mirror rms=%.4f det=%+.6f | copy rms=%.3e det=%+.6f" % (a[0], a[3], b[0], b[3], c[0], c[3]))


print("=== script:", os.path.basename(os.path.abspath(__file__)), "sha256:", sha(os.path.abspath(__file__)))
print("=== time:", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
for p in (MAIN, CONT):
    print("=== %s sha256=%s lines=%d" % (p.split("/")[-1], sha(p), sum(1 for _ in open(p, errors="replace"))))
selfcheck()

M = frames(MAIN); C = frames(CONT)
print("main converged=%d  cont1 converged=%d" % (len(M), len(C)))
m8 = M[-1]
print("main pt8: opt L%d scf L%d E=%.9f" % (m8["opt"], m8["scf"], m8["E"]))
print("\n pt  R(1,29)   R(28,24)  R(11,24)  Kabsch heavy20 vs main pt8   dE_vs_main_pt1")
E0 = -939.308205969
d = lambda f, a, b: float(np.linalg.norm(f["xyz"][a - 1] - f["xyz"][b - 1]))
for k, f in enumerate(C, 1):
    heavy = [i for i, z in enumerate(f["zs"]) if z != 1]
    rms, mx, at, det = kabsch(f["xyz"][heavy], m8["xyz"][heavy])
    print("  %d  %7.4f  %7.4f  %7.4f    %.4f / %.4f / a%d (det %+.1f)   %+8.4f" % (
        k, d(f, 1, 29), d(f, 28, 24), d(f, 11, 24), rms, mx, heavy[at - 1] + 1, det, (f["E"] - E0) * K))

mins = [d(f, 28, 24) for f in C]; maxs = [d(f, 11, 24) for f in C]
print("\ntier check: min R(28,24)=%.4f  max R(11,24)=%.4f  -> tier1 (1.20<=R(28,24)<=1.50): %d ; tier2 (R(28,24)<=1.10 and R(11,24)>=1.50): %d" % (
    min(mins), max(maxs), sum(1 for x in mins if 1.20 <= x <= 1.50), sum(1 for f in C if d(f, 28, 24) <= 1.10 and d(f, 11, 24) >= 1.50)))
