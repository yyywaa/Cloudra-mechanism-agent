#!/usr/bin/env python3
"""
HI1/E3 ts_0011 forensics -- part B: native-log numbers (energies, frames, distances, IRC, frequencies).
READ-ONLY. No submissions, no writes outside forensic/.
Every number: file + line + same-run sha256.
"""
import hashlib, json, math, os
import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import rdDetermineBonds
RDLogger.DisableLog("rdApp.*")

ROOT = "/home/ly/Cloudra-mechanism-agent"
RUN = ROOT + "/ts/ts_0011"
JOB = RUN + "/jobs/declaration_0004"
E3 = ROOT + "/gold_finish_20261015/HI1/E3"
N = 41
H2K = 627.5094740631
Z2SYM = {1: "H", 6: "C", 7: "N", 8: "O"}

_sha = {}
def sha(p):
    if p not in _sha:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for c in iter(lambda: fh.read(1 << 20), b""): h.update(c)
        _sha[p] = h.hexdigest()
    return _sha[p]
def rel(p): return p.replace(ROOT + "/", "")
def rd(p):
    with open(p, "r", errors="replace") as fh: return fh.read().splitlines()
def read_xyz(p):
    L = rd(p); n = int(L[0].split()[0]); a = []
    for k in range(n):
        q = L[2 + k].split(); a.append((q[0], float(q[1]), float(q[2]), float(q[3])))
    return a, L[1]
def D(a, i, j): return math.sqrt(sum((a[i - 1][k + 1] - a[j - 1][k + 1]) ** 2 for k in range(3)))

DASH = lambda s: s.strip().startswith("-----") and len(s.strip()) > 20
def gauss_frames(path):
    L = rd(path); out = []; i = 0
    while i < len(L):
        st = L[i].strip()
        if st.startswith("Standard orientation:") or st.startswith("Input orientation:"):
            j = i + 1; dsh = []
            while j < len(L) and len(dsh) < 2:
                if DASH(L[j]): dsh.append(j)
                j += 1
            assert len(dsh) == 2, "line %d: <2 dashed lines" % (i + 1)
            start = dsh[1] + 1; a = []; k = start
            while k < len(L):
                p = L[k].split()
                if len(p) == 6 and p[0].isdigit() and p[1].lstrip("-").isdigit():
                    a.append((Z2SYM[int(p[1])], float(p[3]), float(p[4]), float(p[5]))); k += 1
                else: break
            assert len(a) == N, "line %d: %d atoms != %d" % (i + 1, len(a), N)
            assert DASH(L[k]), "line %d: no closing dashes" % (start + 1)
            out.append({"hdr": i + 1, "first": start + 1, "atoms": a,
                        "kind": "Standard" if st.startswith("Standard") else "Input"})
            i = k
        else: i += 1
    return out

def scf(path):
    return [(n, float(s.split()[s.split().index("=") + 1]))
            for n, s in enumerate(rd(path), 1) if s.startswith(" SCF Done:")]

OUT = []
def say(*a): OUT.append(" ".join(str(x) for x in a))

LOGS = {
 "ts_opt(999)":      JOB + "/ts_opt/refine.log",
 "frequency(1029)":  JOB + "/frequency/frequency.log",
 "irc(1033)":        JOB + "/irc/irc.log",
 "reactant_opt(1035)": JOB + "/reactant_opt/reactant_opt.log",
 "reactant_freq(1038)": JOB + "/reactant_frequency/reactant_frequency.log",
 "product_opt(1041)":  JOB + "/product_opt/product_opt.log",
 "product_freq(1043)": JOB + "/product_frequency/product_frequency.log",
 "P(1061)":          E3 + "/runs/P_e3b/P_optfreq.log",
 "I2(961)":          E3 + "/runs/I2_optfreq/I2_optfreq.log",
}
HASHES = {k: sha(p) for k, p in LOGS.items()}

say("# HI1/E3 ts_0011 FORENSICS -- part B (native logs)")
say("\n## 1. LOG SHA256 (this run)")
for k, p in LOGS.items(): say("| %-22s | %-88s | sha256=%s |" % (k, rel(p), HASHES[k]))

# ------------------------------------------------------------------ energies
say("\n## 2. ENERGY / TERMINATION / STATIONARY-POINT LEDGER")
FINAL = {}
for k, p in LOGS.items():
    L = rd(p); S = scf(p)
    st = [(n, s.strip()) for n, s in enumerate(L, 1) if "Stationary point found" in s]
    nt = [(n, s.strip()) for n, s in enumerate(L, 1) if s.startswith(" Normal termination")]
    lk = [(n, s.strip()) for n, s in enumerate(L, 1) if "Link1" in s or "Gaussian 16" in s and "internal" in s]
    say("\n### %s   (%s)" % (k, rel(p)))
    say("   n SCF Done = %d ; last SCF = %.9f Eh at line %d" % (len(S), S[-1][1], S[-1][0]))
    if len(S) > 1:
        say("   first SCF = %.9f Eh at line %d" % (S[0][1], S[0][0]))
    say("   Normal termination lines: %s" % (nt if nt else "NONE"))
    say("   Stationary point lines  : %s" % (st if st else "NONE"))
    if lk: say("   link/internal-step marks: %s" % lk[:6])
    FINAL[k] = (S[-1][1], S[-1][0])

# ------------------------------------------------------------------ irc detail
say("\n## 3. IRC (job 1033) DETAIL")
p = LOGS["irc(1033)"]; L = rd(p)
pts = [(n, s.strip()) for n, s in enumerate(L, 1) if "Point Number" in s]
say("   point markers: %s" % pts)
tot = [(n, s.strip()) for n, s in enumerate(L, 1) if "Total number of points" in s]
say("   totals: %s" % tot)
say("   rx-coord lines: %s" % [(n, s.strip()) for n, s in enumerate(L, 1) if "rx=" in s or "IRC-IRC" in s and "Net displacement" in s][:10])
S = scf(p)
say("   SCF Done: %s" % S)

# ------------------------------------------------------------------ frames
say("\n## 4. FRAMES USED (all asserted = %d atoms between the 2nd dashed line and the closing dashes)" % N)
FR = {}
def add(name, logkey, which="last"):
    p = LOGS[logkey]; fr = gauss_frames(p)
    assert fr
    if which == "last": f = fr[-1]; extra = "frame %d/%d" % (len(fr), len(fr))
    elif which == "first": f = fr[0]; extra = "frame 1/%d" % len(fr)
    else: f = fr[which]; extra = "frame %d/%d" % (which + 1, len(fr))
    FR[name] = f["atoms"]
    say("| %-26s | %-70s hdr_line=%d atom_start_line=%d %s |" % (name, rel(p), f["hdr"], f["first"], extra))
    return f

add("ts_opt_999_final", "ts_opt(999)")
add("irc_1033_f0_initial", "irc(1033)", 0)
add("irc_1033_fwd_p1", "irc(1033)", 1)
add("irc_1033_rev_p1", "irc(1033)", 2)
add("reactant_opt_1035_final", "reactant_opt(1035)")
add("product_opt_1041_final", "product_opt(1041)")
add("P_1061_final", "P(1061)")
add("I2_961_final", "I2(961)")

# symbol order assertion vs canonical work table
proc = json.load(open(RUN + "/process.json"))
work_sym = "".join(a["symbol"] for a in proc["structures"]["reactant"]["atoms"])
for k, a in FR.items():
    s = "".join(x[0] for x in a)
    say("   [%s] element order == canonical work table : %s" % (k, s == work_sym))
    assert s == work_sym, k

xyz_extra = {
 "reactant_seed_xyz": RUN + "/build/input_0004/reactant/seed.xyz",
 "ts_guess_190_xyz": E3 + "/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz",
 "P_seed41_workorder_xyz": E3 + "/prep/P_e3b_product_41_seed.xyz",
 "product_seed_built_xyz": RUN + "/build/input_0004/product/seed.xyz",
 "product_opt_source_xyz": JOB + "/product_opt/product_source.xyz",
 "reactant_opt_source_xyz": JOB + "/reactant_opt/reactant_source.xyz",
}
for k, p in xyz_extra.items():
    a, c = read_xyz(p); FR[k] = a
    say("| %-26s | %-70s sha256=%s comment=%r |" % (k, rel(p), sha(p), c[:90]))

# ------------------------------------------------------------------ distances
KEY = [(2, 4), (2, 25), (25, 26), (4, 26), (25, 27), (10, 27), (11, 27), (2, 3), (9, 10), (9, 11), (28, 29), (2, 29)]
say("\n## 5. KEY DISTANCES (Angstrom, 1-based canonical work order)")
hdr = "| frame | " + " | ".join("%d-%d" % p for p in KEY) + " |"
say(hdr); say("|" + "---|" * (len(KEY) + 1))
for k, a in FR.items():
    say("| %s | " % k + " | ".join("%.3f" % D(a, i, j) for i, j in KEY) + " |")
say("\nchemical reading of the columns (see part A bond tables): "
    "2-4 = C(iminium/ketone C)-N ; 2-25 = C-O(water O / ketone O) ; 25-26 = O-H(water) ; "
    "4-26 = N-H ; 25-27 = O-H(second water H) ; 10-27 = carboxyl O-H ; 11-27 = other carboxyl O-H ; "
    "2-3 = C-CH3 ; 9-10 / 9-11 = carboxyl C-O ; 28-29 = C-OH ; 2-29 = C-C(alpha)")

# ------------------------------------------------------------------ identity of frames
say("\n## 6. GEOMETRY-ONLY IDENTITY OF EACH FRAME (RDKit DetermineBonds, charge 0)")
def mol_xyz(a, tag):
    blk = "%d\n%s\n" % (len(a), tag) + "".join("%s %.8f %.8f %.8f\n" % x for x in a)
    m = Chem.MolFromXYZBlock(blk)
    rdDetermineBonds.DetermineBonds(m, charge=0, allowChargedFragments=True, embedChiral=True)
    return m
def ik(m):
    from rdkit.Chem.inchi import MolToInchiKey
    return MolToInchiKey(m)
def smi(m): return Chem.MolToSmiles(Chem.RemoveHs(m))
MOL = {}
for k, a in FR.items():
    try:
        m = mol_xyz(a, k); MOL[k] = m
        say("| %-26s | %-52s | %s |" % (k, smi(m), ik(m)))
    except Exception as exc:
        say("| %-26s | PERCEPTION FAILED: %s ||" % (k, exc))

# ------------------------------------------------------------------ RMSD
say("\n## 7. KABSCH RMSD (A, all 41 atoms, same work order; no symmetry re-labelling)")
def kab(A, B):
    A = np.array([x[1:] for x in A]); B = np.array([x[1:] for x in B])
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Ac.T @ Bc)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return float(np.sqrt(((R @ Ac.T).T - Bc) ** 2).sum(1).mean())
pairs = [("product_opt_1041_final", "reactant_seed_xyz"), ("product_opt_1041_final", "I2_961_final"),
         ("product_opt_1041_final", "P_1061_final"), ("reactant_opt_1035_final", "I2_961_final"),
         ("ts_opt_999_final", "I2_961_final"), ("ts_opt_999_final", "P_1061_final"),
         ("P_1061_final", "P_seed41_workorder_xyz"), ("product_opt_1041_final", "ts_opt_999_final"),
         ("irc_1033_rev_p1", "I2_961_final"), ("irc_1033_rev_p1", "ts_opt_999_final"),
         ("irc_1033_fwd_p1", "ts_opt_999_final")]
for a, b in pairs:
    if a in FR and b in FR:
        say("| RMSD(%s , %s) = %.4f |" % (a, b, kab(FR[a], FR[b])))

# ------------------------------------------------------------------ product seed mapping
say("\n## 8. BUILT PRODUCT SEED: mapping its own atom order onto the canonical work order")
seed = MOL["product_seed_built_xyz"]; ref = MOL["P_seed41_workorder_xyz"]
match = ref.GetSubstructMatch(seed, useChirality=True)
if not match: match = ref.GetSubstructMatch(seed, useChirality=False)
say("   substructure match (seed idx -> work idx) found: %s" % bool(match))
if match:
    s2w = {i + 1: match[i] + 1 for i in range(seed.GetNumAtoms())}
    say("   seed->work: " + " ".join("%d->%d" % (i, s2w[i]) for i in sorted(s2w)))
    say("   chirality-aware match: %s" % bool(ref.GetSubstructMatch(seed, useChirality=True)))
    us = ["%d->%d" % (i, s2w[i]) for i in (1, 2, 3, 4, 5, 6, 25, 26, 27, 28, 32, 33, 41)]
    say("   key seed atoms -> work: %s" % us)
    a = FR["product_seed_built_xyz"]
    for (i, j, name) in [(2, 3, "carbonyl C=O"), (2, 32, "C-N"), (32, 41, "N-H"), (25, 26, "carboxyl O=C"),
                         (27, 33, "carboxyl O-H"), (1, 2, "CH3-C"), (2, 4, "C-CH2"), (5, 6, "C-OH")]:
        say("   seed d(%d-%d)=%.4f A  %-14s  | as work d(%d-%d)" % (i, j, D(a, i, j), name, s2w[i], s2w[j]))

# ------------------------------------------------------------------ dE
say("\n## 9. ELECTRONIC ENERGY TABLE (Gaussian pure electronic, RB3LYP/def2SVP; NOT barriers)")
REF = FINAL["I2(961)"][0]
say("   reference: I2 = %.9f Eh (job 961, line %d, sha256=%s)" % (REF, FINAL["I2(961)"][1], HASHES["I2(961)"]))
say("| item | E(Eh) | line | dE vs I2 (kcal/mol) |")
say("|---|---|---|---|")
for k, (e, ln) in FINAL.items():
    say("| %s | %.9f | %d | %+.2f |" % (k, e, ln, (e - REF) * H2K))

# ------------------------------------------------------------------ frequency
say("\n## 10. FREQUENCY TABLE CHECK (job 1029)")
p = LOGS["frequency(1029)"]; L = rd(p)
fr = [(n, s) for n, s in enumerate(L, 1) if s.startswith(" Frequencies --")]
vals = []
for n, s in fr: vals += [float(x) for x in s.split("--")[1].split()]
say("   groups = %d ; values = %d ; 3N-6 = %d ; equal: %s" % (len(fr), len(vals), 3 * N - 6, len(vals) == 3 * N - 6))
say("   first group line %d: %r" % (fr[0][0], fr[0][1]))
say("   last  group line %d: %r" % (fr[-1][0], fr[-1][1]))
neg = [v for v in vals if v < 0]
say("   negative values in table: %s" % neg)
say("   imaginary header lines: %s" % [(n, s.strip()) for n, s in enumerate(L, 1) if "imaginary frequencies (negative" in s])
say("   low-frequency probe lines: %s" % [(n, s.strip()) for n, s in enumerate(L, 1) if s.startswith(" Low frequencies")])
say("   reduced mass / frc const lines after first table group:")
for n in range(fr[0][0], fr[0][0] + 4):
    say("      L%d: %s" % (n, L[n - 1].strip()))

print("\n".join(OUT))
