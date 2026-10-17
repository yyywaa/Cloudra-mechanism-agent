#!/usr/bin/env python3
"""HI1_E1a cont1 (C2-N18 2.1920 -> 1.6920, 6 geometries) analysis.

Reporting contract agreed with the HI1 Coordinator / lane1:
  * the cont1 table is ONLY the branch-B bonding-side segment (R 2.1920 -> 1.6920);
    it must never be spliced onto branch A (sp1-sp4) nor subtracted across branches.
  * dE is taken relative to sp11 (= cont1 point 1, the branch-B anchor), labelled
    "relative to branch-B first point, NOT a dE-double-dagger".
  * RC_27 is printed in its own clearly-marked column as a denominator/reference
    context only; it is not used for any subtraction-based barrier claim.
  * per point: scan#, measured R(2,18) and |measured-target|, R(3,27), R(18,27),
    R(2,3) (C2-O3), R(13,19), SCF energy + SCF line, dE vs sp11, the
    "Optimization completed" line, plus the verbatim termination line(s).
  * 12-heavy-atom Kabsch RMSD between consecutive converged geometries (SVD,
    det=+1, R maps previous -> next) with three synthetic self-tests.
Peaks are TS candidates only; nothing here is a dE-double-dagger.
"""
import sys, json, math
import numpy as np

RC27 = -593.934532807      # denominator reference only (never subtract across methods)
EH2KCAL = 627.509474
S_TARGET0 = None           # first measured R(2,18) = branch-B anchor (sp11)


def read_lines(path):
    with open(path, "r", errors="replace") as fh:
        return fh.read().split("\n")


def parse_geo_block(lines, start):
    rows = []
    i = start + 5
    while i < len(lines):
        p = lines[i].split()
        if len(p) != 6:
            break
        try:
            _c, z, _t = int(p[0]), int(p[1]), int(p[2])
            x, y, zz = float(p[3]), float(p[4]), float(p[5])
        except ValueError:
            break
        rows.append((z, x, y, zz))
        i += 1
    return rows


def collect_scf(lines):
    geo_idx = [i for i, ln in enumerate(lines) if "Standard orientation:" in ln]
    scf = []
    for i, ln in enumerate(lines):
        if "SCF Done:" in ln:
            e = float(ln.split("=")[1].split()[0])
            prev = [g for g in geo_idx if g < i]
            geo = parse_geo_block(lines, prev[-1]) if prev else []
            scf.append({"line": i + 1, "E": e, "geo": geo})
    return scf


def kabsch_rmsd(P, Q):
    """RMSD of P onto Q after optimal rotation (SVD, det=+1 correction)."""
    P = np.asarray(P, float); Q = np.asarray(Q, float)
    Pc = P - P.mean(axis=0); Qc = Q - Q.mean(axis=0)
    U, S, Vt = np.linalg.svd(Pc.T @ Qc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T          # acts on P (column convention)
    diff = (R @ Pc.T).T - Qc
    dev = np.sqrt((diff ** 2).sum(axis=1))      # per-atom displacement after fit, Angstrom
    return math.sqrt((diff ** 2).sum() / len(P)), R, d, dev


def kabsch_self_test():
    rng = np.random.default_rng(20261017)
    X = rng.normal(size=(12, 3)) * 2.0
    th = math.radians(37.0)
    Rz = np.array([[math.cos(th), -math.sin(th), 0.0],
                   [math.sin(th), math.cos(th), 0.0],
                   [0.0, 0.0, 1.0]])
    Y = (Rz @ X.T).T + np.array([3.1, -2.4, 0.7])     # known rotation + translation
    a = kabsch_rmsd(X, Y)[0]
    M = X.copy(); M[:, 0] *= -1.0                     # mirror image
    b = kabsch_rmsd(X, M)[0]
    c = kabsch_rmsd(X, X.copy())[0]                   # identical copy
    return {"rot_trans_rmsd": a, "mirror_rmsd": b, "copy_rmsd": c,
            "pass_rot": a < 1e-9, "pass_mirror": b > 1e-3, "pass_copy": c < 1e-9}


def main():
    log = sys.argv[1]
    step = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1000   # scan step (negative direction)
    lines = read_lines(log)
    scf = collect_scf(lines)
    comp = [i for i, ln in enumerate(lines) if "Optimization completed" in ln]
    term = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
            if ln.startswith(" Normal termination") or "Error termination" in ln]

    print("LOG", log)
    print("lines_total", len(lines))
    print("scf_done_count", len(scf))
    print("optimization_completed_count", len(comp), "at_lines", [i + 1 for i in comp])
    print("termination_lines", term)

    pts = []
    for k, ci in enumerate(comp):
        cand = [s for s in scf if s["line"] <= ci]
        if not cand:
            continue
        s = cand[-1]
        lo = 0 if k == 0 else comp[k - 1]
        ncyc = len([x for x in scf if lo < x["line"] <= ci])
        pts.append({"point": k + 1, "scf_line": s["line"], "E": s["E"], "geo": s["geo"],
                    "n_opt_cycles": ncyc, "completed_line": ci + 1})

    print()
    print("SCAN | R(2,18)meas | |d-target| | R(3,27) | R(18,27) | R(2,3)C2-O3 | R(13,19) |"
          " SCFline | E(Eh) | dE_vs_sp11(Eh) | dE_vs_sp11(kcal) | compl_line | optcycles |"
          " heavy12_Kabsch(prev->this) | RC27ref_column_only")
    prev = None
    anchor = None
    rows_out = []
    for p in pts:
        g = p["geo"]
        heavy_idx = [i for i, a in enumerate(g) if a[0] != 1]
        def d(i, j):
            a, b = g[i - 1], g[j - 1]
            return math.sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2 + (a[3] - b[3]) ** 2)
        r218 = d(2, 18)
        if anchor is None:
            anchor = r218
        target = round(anchor + step * (p["point"] - 1), 4)
        hv = [g[i][1:] for i in heavy_idx]
        if prev is None:
            rms = None
            maxdev = None
        else:
            rms, _R, _det, dev = kabsch_rmsd(prev, hv)
            maxdev = float(dev.max())
        dE = p["E"] - (pts[0]["E"])
        ref = p["E"] - RC27
        print("%4d | %11.4f | %10.4f | %8.4f | %8.4f | %10.4f | %8.4f | %7d | %.9f | %+15.6f | %+16.2f | %10d | %9d | %s | %s | %+9.6f"
              % (p["point"], r218, abs(r218 - target), d(3, 27), d(18, 27), d(2, 3), d(13, 19),
                 p["scf_line"], p["E"], dE, dE * EH2KCAL, p["completed_line"], p["n_opt_cycles"],
                 ("%.4f" % rms) if rms is not None else "-",
                 ("%.4f" % maxdev) if maxdev is not None else "-", ref))
        # proton-migration guard: H27 on O3 instead of N18
        flag = ""
        if d(3, 27) < 1.30 and d(18, 27) > 1.10:
            flag = "H27 MIGRATED N18->O3: chemical channel changed at this step"
        rows_out.append({"point": p["point"], "R_2_18": round(r218, 4), "target": target,
                         "abs_dev_target": round(abs(r218 - target), 4),
                         "R_3_27": round(d(3, 27), 4), "R_18_27": round(d(18, 27), 4),
                         "R_2_3": round(d(2, 3), 4), "R_13_19": round(d(13, 19), 4),
                         "scf_line": p["scf_line"], "E": p["E"],
                         "dE_vs_sp11_Eh": dE, "dE_vs_sp11_kcal": dE * EH2KCAL,
                         "completed_line": p["completed_line"], "n_opt_cycles": p["n_opt_cycles"],
                         "heavy12_kabsch_prev_to_this": None if rms is None else round(rms, 4),
                         "heavy12_single_atom_max_dev": None if maxdev is None else round(maxdev, 4),
                         "rc27_reference_column_only": ref, "proton_flag": flag})
        prev = hv
    print()
    print("kabsch_self_test", json.dumps(kabsch_self_test()))
    out = {"log": log, "n_points": len(pts), "branch": "B bonding-side segment only (2.1920->1.6920)",
           "anchor": "cont1 point1 = job1072 sp11; dE is relative to this anchor, not a barrier",
           "termination_lines": term, "points": rows_out}
    with open(log + ".cont1_points.json", "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
