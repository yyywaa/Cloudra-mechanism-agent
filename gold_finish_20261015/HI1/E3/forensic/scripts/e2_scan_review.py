#!/usr/bin/env python3
"""
E2 1D constrained scan (job 1075) -- READ-ONLY profile reviewer.
Owner: ts_0011 forensic lane (as_b8536002aacb48e3). Zero submissions; reads the log only.

Discipline encoded here:
  * every orientation block asserted: exactly 41 atom rows between the 2nd dashed line and a closing dashed line;
  * element order asserted against the frozen seed ts/ts_0009/build/input_0004/reactant/seed.xyz (sha c9d59aea...);
  * only frames AFTER 'Optimization completed.' belong to a converged point; process frames never tabulated;
  * energy = last 'SCF Done' of that converged block (line reported), referenced to the FIRST converged point;
  * Kabsch RMSD with det=+1 ONLY (mirror images are refused, not 'fixed'), heavy atoms only, count printed;
  * the RMSD routine must pass three synthetic self-checks before any number is accepted:
        (i) known rotation+translation -> 0, (ii) mirror image -> != 0, (iii) identical copy -> 0.
Usage: python3 e2_scan_review.py [log] [--table]
"""
import hashlib, math, sys
import numpy as np

LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
SEED = "/home/ly/Cloudra-mechanism-agent/ts/ts_0009/build/input_0004/reactant/seed.xyz"
H2K = 627.5094740631
NAT = 41
Z2SYM = {1: "H", 6: "C", 7: "N", 8: "O"}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def read_xyz_syms(p):
    L = open(p).read().splitlines()
    n = int(L[0].split()[0])
    return [q.split()[0] for q in L[2:2 + n]]

DASH = lambda s: s.strip().startswith("-----") and len(s.strip()) > 20

def parse(L):
    frames, i = [], 0
    while i < len(L):
        s = L[i].strip()
        if s.startswith("Standard orientation:") or s.startswith("Input orientation:"):
            j, dsh = i + 1, []
            while len(dsh) < 2:
                if DASH(L[j]): dsh.append(j)
                j += 1
            st = dsh[1] + 1; a = []; k = st
            while len(a) < NAT:
                q = L[k].split()
                assert len(q) == 6 and q[0].isdigit(), "bad atom row L%d: %r" % (k + 1, L[k])
                a.append((Z2SYM[int(q[1])], *map(float, q[3:6]))); k += 1
            assert DASH(L[k]), "no closing dashes after L%d" % (k + 1)
            frames.append({"hdr": i + 1, "first": st + 1, "kind": "Std" if s.startswith("Standard") else "Inp", "atoms": a})
            i = k
        else:
            i += 1
    scf = [(n, float(s.split()[s.split().index("=") + 1])) for n, s in enumerate(L, 1) if "SCF Done:" in s]
    pts = []
    for n, s in enumerate(L, 1):
        if "on scan point" not in s or not s.strip().startswith("Step number"): continue
        right = s.split("on scan point")[1]
        a, b = right.split("out of")
        pts.append((n, int(a), int(b)))
    oc = [n for n, s in enumerate(L, 1) if "Optimization completed" in s]
    return frames, scf, pts, oc

# ---------------------------------------------------------------- geometry math
def kabsch_rmsd(A, B, heavy, label=""):
    """A,B: (41,3). det=+1 only. Returns (rmsd, det_sign_requested)."""
    A = np.asarray([a[1:] for a in A], float)[heavy]
    B = np.asarray([b[1:] for b in B], float)[heavy]
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Ac.T @ Bc)
    d = np.linalg.det(Vt.T @ U.T)
    if d < 0:
        raise ValueError("reflection-only solution for %s -- refusing (mirror guard)" % label)
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    D = (((R @ Ac.T).T - Bc) ** 2).sum(1)
    return float(np.sqrt(D.mean()))

def kabsch_rmsd_raw(A, B, heavy):
    """Reflection-ALLOWED fit, used ONLY for the mirror self-check (never for reported numbers)."""
    A = np.asarray([a[1:] for a in A], float)[heavy]
    B = np.asarray([b[1:] for b in B], float)[heavy]
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Ac.T @ Bc)
    R = Vt.T @ np.diag([1.0, 1.0, np.sign(np.linalg.det(Vt.T @ U.T))]) @ U.T
    return float(np.sqrt((((R @ Ac.T).T - Bc) ** 2).sum(1).mean()))

def selfcheck_kabsch(ref_atoms, heavy):
    """Three synthetic checks; returns list of (name, value, pass)."""
    A = [(s, *xyz) for s, *xyz in ref_atoms]
    P = np.array([a[1:] for a in A], float)
    # (i) known rotation + translation
    th = 0.7; ax = np.array([0.3, -0.5, 0.8]); ax = ax / np.linalg.norm(ax)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    Rm = np.eye(3) + math.sin(th) * K + (1 - math.cos(th)) * (K @ K)
    P1 = (Rm @ P.T).T + np.array([3.1, -2.2, 0.9])
    B = [(s, *p) for s, p in zip([a[0] for a in A], P1)]
    # (ii) mirror image (x -> -x)
    P2 = P * np.array([-1.0, 1.0, 1.0])
    C = [(s, *p) for s, p in zip([a[0] for a in A], P2)]
    # (iii) identical copy
    Dcpy = [(s, *p) for s, p in zip([a[0] for a in A], P.copy())]
    out = []
    out.append(("(i)  known rotation+translation -> 0", kabsch_rmsd(A, B, heavy, "rot"), True))
    v_mir = kabsch_rmsd_raw(A, C, heavy)
    refused = False
    try:
        kabsch_rmsd(A, C, heavy, "mirror")
    except ValueError:
        refused = True
    out.append(("(ii) mirror image -> != 0 (value, reflection-allowed fit)", v_mir, v_mir > 1e-3))
    out.append(("(ii-b) production fit REFUSES that mirror (det=+1)", 0.0 if refused else 1.0, refused))
    out.append(("(iii) identical copy -> 0", kabsch_rmsd(A, Dcpy, heavy, "copy"), True))
    return out

# ---------------------------------------------------------------------- driver
def main():
    path = LOG
    for a in sys.argv[1:]:
        if not a.startswith("--"): path = a
    table = "--table" in sys.argv
    import datetime
    blob = open(path, "rb").read()          # ONE read -> sha, byte count, line count and all numbers
    L = blob.decode(errors="replace").splitlines()
    print("# E2 1D scan read-only review  (snapshot mode: one byte read for sha + all numbers)")
    print("snapshot时刻 (CST) :", datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("log      :", path)
    print("log sha  :", hashlib.sha256(blob).hexdigest())
    print("log bytes:", len(blob), " file lines:", len(L))
    print("seed     :", SEED, sha(SEED))
    frames, scf, pts, oc = parse(L)
    seed_syms = read_xyz_syms(SEED)
    for f in frames:
        assert [a[0] for a in f["atoms"]] == seed_syms, "element order mismatch at L%d" % f["hdr"]
    print("frames   : %d orientation blocks (all 41 atoms, element order == seed)" % len(frames))
    print("SCF Done : %d ; last: L%d %.9f" % (len(scf), scf[-1][0], scf[-1][1]))
    print("'Optimization completed.' lines:", oc)
    term = [(n, s.strip()) for n, s in enumerate(L, 1) if "termination of Gaussian" in s]
    print("termination lines:", term)
    if pts:
        print("scan point markers: first L%d (point %d of %d), last L%d (point %d of %d), M=%d"
              % (pts[0][0], pts[0][1], pts[0][2], pts[-1][0], pts[-1][1], pts[-1][2], pts[-1][2]))
    heavy = [i for i, s in enumerate(seed_syms) if s != "H"]
    print("heavy atom set: %d atoms (indices %s...)" % (len(heavy), heavy[:6]))
    # converged points: for each OC line, energy = last SCF before it, geometry = last orientation block before it
    conv = []
    for o in oc:
        e = [s for s in scf if s[0] < o][-1]
        f = [fr for fr in frames if fr["hdr"] < o][-1]
        assert f["hdr"] < e[0], "geometry must print before its energy (L%d vs L%d)" % (f["hdr"], e[0])
        assert not [fr for fr in frames if e[0] < fr["hdr"] < o], "a later geometry precedes the block energy"
        conv.append({"oc": o, "E": e[1], "Eline": e[0], "atoms": f["atoms"], "hdr": f["hdr"]})
    print("converged points: %d" % len(conv))
    if not conv: return
    # point index for each converged block = last scan point marker before its OC line
    for c in conv:
        m = [p for p in pts if p[0] < c["oc"]]
        c["pt"] = m[-1][1] if m else 1
        c["M"] = m[-1][2] if m else None
    ref = conv[0]
    print("\n## synthetic Kabsch self-checks (must pass before any RMSD is quoted)")
    for name, v, ok in selfcheck_kabsch(ref["atoms"], heavy):
        print("   %-46s value=%.3e  %s" % (name, v, "PASS" if ok else "FAIL"))
    d = lambda a, i, j: math.dist(a[i-1][1:], a[j-1][1:])
    def tier(a):
        r28_24 = d(a, 28, 24); r11_24 = d(a, 11, 24)
        if r28_24 > 1.50: return "0", r28_24, r11_24
        if 1.20 <= r28_24 <= 1.50: return "1", r28_24, r11_24
        if r28_24 <= 1.10 and r11_24 >= 1.50: return "2", r28_24, r11_24
        return "1/2-border", r28_24, r11_24
    if table:
        rows = []
        for k, c in enumerate(conv):
            t, r28, r11 = tier(c["atoms"])
            rms = None if k == 0 else kabsch_rmsd(conv[k-1]["atoms"], c["atoms"], heavy, "pt%d" % c["pt"])
            rows.append({"pt": c["pt"], "M": c["M"], "R": d(c["atoms"], 1, 29), "E": c["E"], "EL": c["Eline"],
                         "hdr": c["hdr"], "dE": (c["E"] - ref["E"]) * H2K, "rms": rms,
                         "r28": r28, "r11": r11, "tier": t, "atoms": c["atoms"]})
        def emit(view_name, keep):
            sel = [r for r in rows if keep(r)]
            print("\n## %s -- 点数 %d / 已收敛 %d" % (view_name, len(sel), len(rows)))
            print("| pt/M | R(1,29) | E(Eh) | SCF L | frame hdr | dE vs pt1 (kcal/mol) | Kabsch rmsd vs prev conv. | R(28,24) | R(11,24) | tier |")
            print("|---|---|---|---|---|---|---|---|---|---|")
            for r in sel:
                print("| %d/%s | %.4f | %.9f | L%d | L%d | %+.2f | %s | %.4f | %.4f | %s |"
                      % (r["pt"], r["M"], r["R"], r["E"], r["EL"], r["hdr"], r["dE"],
                         "-" if r["rms"] is None else "%.4f" % r["rms"], r["r28"], r["r11"], r["tier"]))
            # monotonicity / internal maxima inside this view
            E = [r["E"] for r in sel]
            inc = all(E[i + 1] > E[i] for i in range(len(E) - 1))
            dec = all(E[i + 1] < E[i] for i in range(len(E) - 1))
            peaks = [i for i in range(1, len(E) - 1) if E[i] > E[i - 1] and E[i] > E[i + 1]]
            print("   monotonic: increasing=%s decreasing=%s ; internal maxima: %s"
                  % (inc, dec, [sel[i]["pt"] for i in peaks] if peaks else "none"))
            for i in peaks:
                r = sel[i]
                if r["tier"] == "1":
                    print("   PEAK at pt %d (tier 1) -> 只记「需二维扫描」，不作 TS 候选" % r["pt"])
                else:
                    print("   PEAK at pt %d (tier %s) -> 仅 TS 候选/上界（E=%.9f L%d），绝不写 dE-double-dagger"
                          % (r["pt"], r["tier"], r["E"], r["EL"]))
            # reversal / jump guards
            for i in range(1, len(sel)):
                if sel[i]["R"] > sel[i - 1]["R"] + 1e-4:
                    print("   !! R(1,29) REVERSAL: pt%d %.4f -> pt%d %.4f" % (sel[i-1]["pt"], sel[i-1]["R"], sel[i]["pt"], sel[i]["R"]))
                dE = (sel[i]["E"] - sel[i - 1]["E"]) * H2K
                if abs(dE) > 15.0:
                    print("   !! |dE| > 15 kcal/mol between pt%d and pt%d: %+.2f" % (sel[i-1]["pt"], sel[i]["pt"], dE))
                if sel[i]["rms"] is not None and sel[i]["rms"] > 0.3 and dE < 0:
                    print("   !! possible BRANCH SWITCH between pt%d and pt%d: rmsd=%.3f A, dE=%+.2f kcal/mol, "
                          "R(28,24) %.4f->%.4f" % (sel[i-1]["pt"], sel[i]["pt"], sel[i]["rms"], dE, sel[i-1]["r28"], sel[i]["r28"]))
            return sel
        emit("表 A | 含档 1 点（共享质子）", lambda r: True)
        emit("表 B | 排除档 1 点", lambda r: r["tier"] != "1")
        # unconverged scan points started but not completed
        done = set(r["pt"] for r in rows)
        started = []
        for n, p, m in pts:
            if p not in done and (not started or started[-1][0] != p):
                started.append((p, m, n))
        print("\n## 未收敛点（单列，不入任何表）")
        for p, m, n in started:
            e = [s for s in scf if s[0] < n]
            print("   scan point %d/%d in progress (marker L%d)%s"
                  % (p, m, n, "" if not e else "；过程读数 SCF L%d = %.9f（不入表）" % (e[-1][0], e[-1][1])))
    else:
        print("\n## single-point spot values (NOT a profile table)")
        for c in conv:
            t, r28, r11 = tier(c["atoms"])
            print("   pt %d/%s  R(1,29)=%.4f  E=%.9f (L%d)  R(28,24)=%.4f R(11,24)=%.4f tier=%s  frame hdr L%d"
                  % (c["pt"], c["M"], d(c["atoms"], 1, 29), c["E"], c["Eline"], r28, r11, t, c["hdr"]))

if __name__ == "__main__":
    main()
