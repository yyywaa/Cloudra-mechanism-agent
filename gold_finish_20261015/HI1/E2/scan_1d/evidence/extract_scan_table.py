#!/usr/bin/env python3
"""Read-only per-scan-point table extractor for HI1 E2 1D relaxed scan (Gaussian 16).

Criteria = the FROZEN ones in REPORT_E2_1D_SCAN_PREP.md sec.4 (+ sec.6 corrections):
  * only converged frames enter the table: geometry = last "Standard orientation" block
    and energy = last "SCF Done" line strictly before "Optimization completed." +
    "-- Stationary point found."; the SCF Done log line number is always printed;
  * R(1,29) recomputed from the frame coordinates, never copied from the input;
  * dE vs the FIRST point, kcal/mol, 1 Ha = 627.509474 kcal/mol;
  * heavy-atom (non-H) Kabsch RMSD vs the PREVIOUS point (superpose first, then RMS);
  * tier 1: R(28,H24) in [1.20,1.50]; tier 2: R(28,H24) < 1.20 AND R(O28-H24) <= 1.05,
    judged on the SAME frame; R(11,H24) (donor O-H) printed as independent evidence;
  * design sec.4 extras: R(28,29), R(2,4), R(25,29), R(25,1), minsep + bonding class.
Read-only: opens the log for reading, prints markdown. Writes nothing.
Usage: python3 extract_scan_table.py <log>
"""
import sys, re, hashlib, datetime, math
import numpy as np

ELEM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne"}
RCOV = {"H":0.31,"C":0.76,"N":0.71,"O":0.66}
HA2KCAL = 627.509474

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

log = sys.argv[1]
raw = open(log, "r", errors="replace").read()
lines = raw.split("\n")

print("### provenance")
print("- now (host) :", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))
print("- log path   :", log)
print("- log sha256 :", sha256(log))
print("- log lines  :", raw.count("\n"))
print("- log bytes  :", len(raw))
print()

step_re = re.compile(r"Step number\s+(\d+) out of a maximum of\s+(\d+) on scan point\s+(\d+) out of\s+(\d+)")
step_idx, point_idx, mmax = [], [], set()
for i, ln in enumerate(lines):
    m = step_re.search(ln)
    if m:
        step_idx.append(i)
        point_idx.append(int(m.group(3)))
        mmax.add(int(m.group(4)))

oc_idx = [i for i, ln in enumerate(lines) if ln.strip() == "Optimization completed."]
sp_idx = [i for i, ln in enumerate(lines) if ln.strip() == "-- Stationary point found."]
scf_idx = [i for i, ln in enumerate(lines) if ln.strip().startswith("SCF Done:")]
so_idx = [i for i, ln in enumerate(lines) if "Standard orientation:" in ln]
M = max(mmax) if len(mmax) == 1 else sorted(mmax)

print("### log status (measured, not assumed)")
print("- M = number of scan points declared in the log:", M)
print("- optimization steps logged (Step number ... on scan point ...):", len(step_idx))
print("- points that reached \"Optimization completed.\":", [point_idx[max([j for j, si in enumerate(step_idx) if si < oc], default=0)] if any(si < oc for si in step_idx) else None for oc in oc_idx])
print("- \"Optimization completed.\" line numbers:", [i + 1 for i in oc_idx])
print("- \"-- Stationary point found.\" line numbers:", [i + 1 for i in sp_idx])
for pat in ("Normal termination", "Error termination"):
    hits = [i + 1 for i, ln in enumerate(lines) if pat in ln]
    print("- %-20s -> %s" % (pat, hits if hits else "none yet"))
print()

def parse_orientation(start):
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith("---"):
        i += 1
    i += 1
    while i < len(lines) and not lines[i].strip().startswith("---"):
        i += 1
    i += 1
    atoms = []
    while i < len(lines) and not lines[i].strip().startswith("---"):
        t = lines[i].split()
        if len(t) >= 6:
            atoms.append((ELEM.get(int(t[1]), "X"), float(t[3]), float(t[4]), float(t[5])))
        i += 1
    return atoms

def dist(a, b):
    return math.sqrt((a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2 + (a[3] - b[3]) ** 2)

def kabsch_rmsd(A, B):
    A = np.asarray(A, float); B = np.asarray(B, float)
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    H = Bc.T @ Ac
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    Ar = (R @ Ac.T).T
    return float(np.sqrt(((Ar - Bc) ** 2).sum() / A.shape[0]))

recs = []
for k, oc in enumerate(oc_idx):
    prev_oc = oc_idx[k - 1] if k > 0 else -1
    js = [j for j, si in enumerate(step_idx) if prev_oc < si < oc]
    if not js:
        continue
    pt = point_idx[js[-1]]
    sos = [s for s in so_idx if prev_oc < s < oc]
    scfs = [s for s in scf_idx if prev_oc < s < oc]
    if not sos or not scfs:
        continue
    conv_line, conv_ok, conv_detail = None, None, ""
    for i in range(oc - 1, max(prev_oc, oc - 400), -1):
        if "Converged?" in lines[i]:
            conv_line = i + 1
            items, detail = [], []
            for j in range(i + 1, min(i + 9, len(lines))):
                t = lines[j].split()
                if len(t) < 4 or t[-1] not in ("YES", "NO"):
                    break
                items.append(t[-1])
                detail.append("%s %s %s" % (" ".join(t[:-2]), t[-2], t[-1]))
            conv_ok = all(x == "YES" for x in items) if items else None
            conv_detail = "; ".join(detail)
            break
    recs.append(dict(point=pt, geo_line=sos[-1] + 1, e_line=scfs[-1] + 1,
                     e=float(lines[scfs[-1]].split("=")[1].split()[0]),
                     scf_cyc=lines[scfs[-1]].split("after")[1].split()[0],
                     nsteps=len(js), conv_line=conv_line, conv_ok=conv_ok,
                     conv_detail=conv_detail, atoms=parse_orientation(sos[-1]),
                     oc_line=oc + 1, sp_line=(sp_idx[k] + 1 if k < len(sp_idx) else None)))

print("### converged scan points found:", len(recs), "of M =", M)
print()
if not recs:
    sys.exit(0)

elems = [a[0] for a in recs[0]["atoms"]]
heavy = [i for i, e in enumerate(elems) if e != "H"]
print("- atoms per frame:", len(elems), "; heavy (non-H):", len(heavy), "; H:", len(elems) - len(heavy))
print("- element order identical in every frame:", all([a[0] for a in r["atoms"]] == elems for r in recs))
print()

def bonded(a, b):
    return dist(a, b) < 1.30 * (RCOV.get(a[0], 0.8) + RCOV.get(b[0], 0.8))

def minsep(A):
    best = (1e9, None, None)
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            d = dist(A[i], A[j])
            if d < best[0]:
                best = (d, i, j)
    d, i, j = best
    if bonded(A[i], A[j]):
        cls = "bonded"
    else:
        cls = "nonbonded"
        for k in range(len(A)):
            if k in (i, j):
                continue
            if bonded(A[i], A[k]) and bonded(A[j], A[k]):
                cls = "1-3"
                break
    return d, "%s%d-%s%d" % (elems[i], i + 1, elems[j], j + 1), cls

def min_nonbonded(A):
    best = (1e9, None)
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            if bonded(A[i], A[j]):
                continue
            d = dist(A[i], A[j])
            if d < best[0]:
                best = (d, "%s%d-%s%d" % (elems[i], i + 1, elems[j], j + 1))
    return best

rows = []
for idx, r in enumerate(recs):
    A = r["atoms"]
    ms, mspair, mscls = minsep(A)
    mnb, mnbpair = min_nonbonded(A)
    d_28_24 = dist(A[27], A[23])
    tier = 0
    if 1.20 <= d_28_24 <= 1.50:
        tier = 1
    if d_28_24 < 1.20 and d_28_24 <= 1.05:
        tier = 2
    rows.append(dict(idx=idx, point=r["point"], oc=r["oc_line"], sp=r["sp_line"], geo=r["geo_line"],
                     e_line=r["e_line"], e=r["e"], de=(r["e"] - recs[0]["e"]) * HA2KCAL,
                     d129=dist(A[0], A[28]), d2829=dist(A[27], A[28]), d24=dist(A[1], A[3]),
                     d2824=d_28_24, d1124=dist(A[10], A[23]), d2529=dist(A[24], A[28]),
                     d251=dist(A[24], A[0]), minsep=ms, mspair=mspair, mscls=mscls,
                     mnb=mnb, mnbpair=mnbpair,
                     rmsd=(None if idx == 0 else kabsch_rmsd([recs[idx - 1]["atoms"][i][1:] for i in heavy],
                                                             [A[i][1:] for i in heavy])),
                     tier=tier, nsteps=r["nsteps"], cyc=r["scf_cyc"], conv=r["conv_ok"],
                     conv_line=r["conv_line"], conv_detail=r["conv_detail"]))

print("### per-point table (converged frames only)")
print()
hdr = ["scan point N out of M", "converged?", "frame line", "SCF Done line", "E(RB3LYP)/Ha",
       "dE vs pt1 (kcal/mol)", "R(1,29)/A", "R(28,29)/A", "R(2,4)/A", "R(28...H24)/A",
       "R(O28-H24)/A", "R(O11-H24)/A", "R(25...29)/A", "R(25...1)/A", "minsep/A", "minsep pair",
       "minsep class", "min nonbonded/A", "min nonbonded pair", "heavy Kabsch RMSD vs prev/A",
       "tier", "opt steps", "SCF cycles"]
print("| " + " | ".join(hdr) + " |")
print("|" + "|".join(["---"] * len(hdr)) + "|")
for x in rows:
    vals = ["%d out of %s" % (x["point"], M), str(x["conv"]) + " (L%s)" % x["conv_line"],
            "L%d (Standard orientation)" % x["geo"], "L%d" % x["e_line"], "%.9f" % x["e"],
            "%+.3f" % x["de"], "%.4f" % x["d129"], "%.4f" % x["d2829"], "%.4f" % x["d24"],
            "%.4f" % x["d2824"], "%.4f" % x["d2824"], "%.4f" % x["d1124"], "%.4f" % x["d2529"],
            "%.4f" % x["d251"], "%.4f" % x["minsep"], x["mspair"], x["mscls"], "%.4f" % x["mnb"],
            x["mnbpair"], "n/a (first)" if x["rmsd"] is None else "%.3f" % x["rmsd"],
            {0: "0 (plain H-bond)", 1: "1 (shared proton)", 2: "2 (proton transferred)"}[x["tier"]],
            str(x["nsteps"]), str(x["cyc"])]
    print("| " + " | ".join(vals) + " |")
print()
print("Note: R(28...H24) and R(O28-H24) are the SAME atom pair (28-24) in this system, so the two columns are numerically identical in every frame; both are printed because the criteria ask for both, and the tier test uses that same-frame value with R(O11-H24) as the independent donor-bond evidence.")
print()
print("### scan-coordinate sanity (R(1,29) vs the designed sequence 4.3543 - 0.2000*(N-1))")
for x in rows:
    exp = 4.3543 - 0.2000 * (x["point"] - 1)
    print("- point %2d: R(1,29) = %.4f, designed %.4f, dev = %+.4f A" % (x["point"], x["d129"], exp, x["d129"] - exp))
print()
print("### convergence-check table quoted from the log (immediately above each \"Optimization completed.\")")
for x in rows:
    print("- point %2d (table at L%s, \"Optimization completed.\" at L%d): %s" % (x["point"], x["conv_line"], x["oc"], x["conv_detail"]))
print()
print("### tier assignment (same-frame rule)")
for x in rows:
    print("- point %2d: R(28...H24) = R(O28-H24) = %.4f A, R(O11-H24) = %.4f A -> tier %d"
          % (x["point"], x["d2824"], x["d1124"], x["tier"]))