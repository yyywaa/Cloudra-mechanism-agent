#!/usr/bin/env python3
"""Part C: cross-checks -- Link1-segmented SCFs, imaginary-mode composition, declared-pair
   distance sanity (0-based vs 1-based reaction_center), bond-table diffs, atom_map consistency."""
import hashlib, json, math, os
from rdkit import Chem, RDLogger
from rdkit.Chem import rdDetermineBonds
RDLogger.DisableLog("rdApp.*")
ROOT = "/home/ly/Cloudra-mechanism-agent"
RUN = ROOT + "/ts/ts_0011"; JOB = RUN + "/jobs/declaration_0004"
E3 = ROOT + "/gold_finish_20261015/HI1/E3"
N = 41; H2K = 627.5094740631
Z2SYM = {1: "H", 6: "C", 7: "N", 8: "O"}
_s = {}
def sha(p):
    if p not in _s:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
        _s[p] = h.hexdigest()
    return _s[p]
def rel(p): return p.replace(ROOT + "/", "")
def rd(p):
    with open(p, "r", errors="replace") as f: return f.read().splitlines()
def read_xyz(p):
    L = rd(p); n = int(L[0].split()[0])
    return [(q.split()[0], *map(float, q.split()[1:4])) for q in L[2:2 + n]]
def D(a, i, j): return math.sqrt(sum((a[i-1][k+1]-a[j-1][k+1])**2 for k in range(3)))
OUT = []
def say(*a): OUT.append(" ".join(str(x) for x in a))

LOGS = {
 "ts_opt(999)": JOB + "/ts_opt/refine.log",
 "frequency(1029)": JOB + "/frequency/frequency.log",
 "irc(1033)": JOB + "/irc/irc.log",
 "product_opt(1041)": JOB + "/product_opt/product_opt.log",
 "product_freq(1043)": JOB + "/product_frequency/product_frequency.log",
 "P(1061)": E3 + "/runs/P_e3b/P_optfreq.log",
 "I2(961)": E3 + "/runs/I2_optfreq/I2_optfreq.log",
}

say("# Part C -- cross-checks")
say("\n## C1. Link1 segmentation of the combined Opt+Freq jobs")
for k in ("P(1061)", "I2(961)"):
    L = rd(LOGS[k]); S = [(n, float(s.split()[s.split().index("=")+1]))
                         for n, s in enumerate(L, 1) if s.startswith(" SCF Done:")]
    link = [(n, s.strip()) for n, s in enumerate(L, 1) if s.startswith(" Link1:")]
    bound = link[0][0] if link else 10**9
    step1 = [x for x in S if x[0] < bound]; step2 = [x for x in S if x[0] > bound]
    say(" %s : %d SCF total; Link1 at L%d" % (k, len(S), bound))
    say("   step1(last 3): %s" % step1[-3:])
    say("   step2(all)  : %s" % step2)
    say("   max |E1-E2| = %.2e Eh" % (abs(step1[-1][1]-step2[-1][1]) if step2 else -1))

say("\n## C2. Frequency-table completeness for every freq log")
for k in ("frequency(1029)", "product_freq(1043)", "P(1061)", "I2(961)"):
    L = rd(LOGS[k]); fr = [(n, s) for n, s in enumerate(L, 1) if s.startswith(" Frequencies --")]
    vals = []
    for n, s in fr: vals += [float(x) for x in s.split("--")[1].split()]
    neg = [(fr[0][0] + 0, v) for v in vals if v < 0]
    say(" %-18s groups=%2d values=%3d 3N-6=%d equal=%s negatives=%s"% (k, len(fr), len(vals), 3*N-6, len(vals)==3*N-6, [v for v in vals if v < 0]))
    say("    lowest 5 table values: %s   (first table line L%d)" % (sorted(vals)[:5], fr[0][0]))
    say("    imaginary header: %s" % [(n, s.strip()) for n, s in enumerate(L, 1) if "imaginary frequencies (negative" in s])
    say("    red.mass/frc of first group: L%d/L%d" % (fr[0][0]+1, fr[0][0]+2))

say("\n## C3. Imaginary mode composition, job 1029 (mode 1, -128.0397 cm-1)")
L = rd(LOGS["frequency(1029)"]); h = None
for n, s in enumerate(L, 1):
    if s.startswith(" Frequencies --") and "-128.0397" in s: h = n; break
say("   table header L%d: %r" % (h, L[h-1]))
say("   red.mass L%d: %r ; frc const L%d: %r" % (h+1, L[h].strip(), h+2, L[h+1].strip()))
# atom block: header line 'Atom AN X Y Z ...' then N atom lines, 3 modes per group
start = h + 4
disp = []
for i in range(N):
    p = L[start + i].split()
    assert len(p) == 11, "unexpected mode-vector line %r" % (L[start+i])
    disp.append((int(p[0]), int(p[1]), float(p[2]), float(p[3]), float(p[4])))
assert [x[0] for x in disp] == list(range(1, N+1))
tot = sum(x[2]**2 + x[3]**2 + x[4]**2 for x in disp)
say("   vector rows L%d..L%d asserted: %d rows, atom ids 1..41 in order" % (start, start+N-1, len(disp)))
say("   component table sorted by |d| (1-based work index; AN=6 C,7 N,8 O,1 H):")
for i, an, x, y, z in sorted(disp, key=lambda t: -(t[2]**2+t[3]**2+t[4]**2))[:12]:
    say("     w%-3d AN=%d  dx=%+0.2f dy=%+0.2f dz=%+0.2f  |d|=%.3f  share=%5.1f%%"
        % (i, an, x, y, z, math.sqrt(x*x+y*y+z*z), 100*(x*x+y*y+z*z)/tot))
groups = {"methyl Hs w14/w15/w16": [14, 15, 16], "declared C2 atom (w2)": [2], "N (w4)": [4],
          "water O (w25)": [25], "water H (w26)": [26], "water H (w27)": [27],
          "carboxyl O (w10)": [10], "carboxyl O (w11)": [11]}
for g, ids in groups.items():
    s = sum(disp[i-1][2]**2+disp[i-1][3]**2+disp[i-1][4]**2 for i in ids)
    say("   share on %-24s = %5.1f%%" % (g, 100*s/tot))
wp = {frozenset(p): 0.0 for p in [(2, 4), (2, 25), (25, 26), (4, 26), (25, 27), (10, 27), (2, 3)]}
for key in wp:
    i, j = sorted(key)
    prod = (disp[i-1][2]*disp[j-1][2] + disp[i-1][3]*disp[j-1][3] + disp[i-1][4]*disp[j-1][4])
    wp[key] = prod
say("   pair-projected dot products d_i.d_j/(sum|d|^2): %s" %
    " ".join("%d-%d:%.1f%%" % (sorted(k)[0], sorted(k)[1], 100*v/tot) for k, v in wp.items()))

say("\n## C4. Declared reaction_center: 1-based reading vs 0-based reading")
rc = json.load(open(RUN + "/process.json"))["input"]["reaction"]["reaction_center"]
proc = json.load(open(RUN + "/process.json"))
sym = [a["symbol"] for a in proc["structures"]["reactant"]["atoms"]]
fr = {}
for tag, p in {"I2_seed": RUN + "/build/input_0004/reactant/seed.xyz",
               "guess190": E3 + "/prep/guess_c2o25_190/ts_guess_c2o25_190.xyz",
               "ts_999_final": None}.items():
    if p: fr[tag] = read_xyz(p)
# ts final frame from log
L2 = rd(LOGS["ts_opt(999)"]); idx = [n for n, s in enumerate(L2, 1) if s.strip().startswith("Standard orientation:")][-1]
a = []
k = idx + 4
while len(a) < N:
    pp = L2[k].split()
    if len(pp) == 6 and pp[0].isdigit(): a.append((Z2SYM[int(pp[1])], float(pp[3]), float(pp[4]), float(pp[5]))); k += 1
    else: k += 1
fr["ts_999_final"] = a
say("| declared pair (as written) | 1-based reading (wI-wJ, elements, I2 d / guess d / TS d) | 0-based reading (+1 each, I2 d / guess d / TS d) |")
say("|---|---|---|")
for i, j in rc:
    def fmt(p, q):
        return "%d%s-%d%s  %.3f / %.3f / %.3f" % (p, sym[p-1], q, sym[q-1],
            D(fr["I2_seed"], p, q), D(fr["guess190"], p, q), D(fr["ts_999_final"], p, q))
    say("| (%d,%d) | %s | %s |" % (i, j, fmt(i, j), fmt(i+1, j+1)))

say("\n## C5. Bond-table diff: declared species vs built MOL vs optimized endpoints")
def mol_xyz(a, tag, ch=0):
    blk = "%d\n%s\n" % (len(a), tag) + "".join("%s %.8f %.8f %.8f\n" % x for x in a)
    m = Chem.MolFromXYZBlock(blk); rdDetermineBonds.DetermineBonds(m, charge=ch, allowChargedFragments=True, embedChiral=True); return m
def edge_set(m, mapping=None):
    out = set()
    for b in m.GetBonds():
        a1, a2 = b.GetBeginAtom(), b.GetEndAtom()
        i, j = a1.GetIdx()+1, a2.GetIdx()+1
        if mapping: i, j = mapping[i], mapping[j]
        out.add((min(i, j), max(i, j), str(b.GetBondType())[0]))
    return out
seed_p = Chem.MolFromMolFile(RUN + "/build/input_0004/product/seed.mol", removeHs=False, sanitize=True)
decl_p = Chem.AddHs(Chem.MolFromSmiles(proc["input"]["reaction"]["product_smiles"]))
say("   declared product: %d bonds ; built product MOL: %d bonds" % (decl_p.GetNumBonds(), seed_p.GetNumBonds()))
say("   InChIKey declared = %s" % __import__("rdkit.Chem.inchi", fromlist=["x"]).MolToInchiKey(decl_p))
say("   InChIKey built    = %s" % __import__("rdkit.Chem.inchi", fromlist=["x"]).MolToInchiKey(seed_p))
say("   (numbers compared by InChIKey, so no atom-order dependence)")

say("\n## C6. atom_map consistency (work index -> claimed partner) against the chemical correspondence")
amap = proc["input_binding"]["atom_map"]
s2w = {1:3, 2:2, 3:25, 4:1, 5:29, 6:28, 7:30, 8:31, 9:32, 10:33, 11:34, 12:35, 13:14, 14:15, 15:16,
       16:12, 17:13, 18:36, 19:24, 20:37, 21:38, 22:39, 23:40, 24:41, 25:11, 26:9, 27:10, 28:8, 29:7,
       30:6, 31:5, 32:4, 33:27, 34:23, 35:21, 36:22, 37:19, 38:20, 39:17, 40:18, 41:26}
w2s = {v: k for k, v in s2w.items()}
say("| work idx | element | atom_map value | that value read as product-seed idx -> element | chemically correct product-seed idx -> element |")
say("|---|---|---|---|---|")
for w in (1, 2, 3, 4, 5, 8, 9, 10, 11, 25, 26, 27, 28, 29):
    v = amap[w-1]
    say("| %d | %s | %d | %d %s | %d %s |" % (w, sym[w-1], v, v,
        ("CCOCCOCCCCCCHHHHHHHHHHHHOCOCCCCNHHHHHHHHH"[v-1] if 1 <= v <= 41 else "?"),
        w2s[w], "CCOCCOCCCCCCHHHHHHHHHHHHOCOCCCCNHHHHHHHHH"[w2s[w]-1]))
agree = sum(1 for w in range(1, 42) if amap[w-1] == w2s[w])
say("   atom_map agrees with the chemically derived mapping on %d/41 positions" % agree)
print("\n".join(OUT))
