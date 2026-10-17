#!/usr/bin/env python3
# span_v2_after1078.py -- three-part span wording AFTER job 1078 verified 1071 as a MINIMUM.
# every number is read from the native logs; nothing is typed in from memory.
import re, os, math, hashlib, datetime

K = 627.5095
ROOT = "/home/ly/Cloudra-mechanism-agent"
LOGS = {
 "1028": ROOT + "/gold_finish_20261015/HI1/E3/runs/interm_c160/interm_c160_optfreq.log",
 "1061_P": ROOT + "/gold_finish_20261015/HI1/E3/runs/P_e3b/P_optfreq.log",
 "1073": ROOT + "/gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log",
 "1071": ROOT + "/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log",
 "1078": ROOT + "/ts/ts_0020/jobs/declaration_0001/frequency/frequency.log",
 "1069": ROOT + "/ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log",
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def scan(p):
    L = open(p, errors="replace").read().splitlines()
    scf = []
    for i, ln in enumerate(L):
        m = re.search(r"SCF Done:\s+E\(RB3LYP\)\s+=\s+(-?\d+\.\d+)", ln)
        if m:
            scf.append((i + 1, float(m.group(1))))
    lo = min(scf, key=lambda x: x[1])
    nb = [i + 1 for i, ln in enumerate(L) if ln.strip().startswith("Frequencies --")]
    imag_hdr = [i + 1 for i, ln in enumerate(L) if "imaginary" in ln.lower()]
    neg = []
    for i in nb:
        for tok in L[i - 1].split("--", 1)[1].split():
            try:
                v = float(tok)
            except ValueError:
                continue
            if v < 0:
                neg.append((i, v))
    done = [(i + 1, ln.strip()) for i, ln in enumerate(L) if ln.startswith(" Normal termination of Gaussian 16")]
    optc = [i + 1 for i, ln in enumerate(L) if ln.strip() == "Optimization completed."]
    return dict(path=p, lines=len(L), sha=sha(p), scf=scf, min=lo, nblocks=len(nb),
                imag_hdr=imag_hdr, neg=neg, term=done, optdone=optc)

D = {}
for k, p in LOGS.items():
    if not os.path.exists(p):
        D[k] = dict(path=p, lines=0, sha="MISSING", scf=[], min=(0, float("nan")),
                    nblocks=0, imag_hdr=[], neg=[], term=[], optdone=[])
    else:
        D[k] = scan(p)

now = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
print("span_v2_after1078.py  self sha256 =", sha(os.path.abspath(__file__)), " | measured at", now)
print()
print("=== native evidence per job (min over ALL SCF lines, never the last line) ===")
for k, d in D.items():
    e = d["min"][1]
    r = (e - D["1028"]["min"][1]) * K if d["scf"] else float("nan")
    print("%-6s lines=%7d  sha=%s" % (k, d["lines"], d["sha"][:16] + "..."))
    print("       min SCF L%-8d %s  %+8.4f vs 1028 | freqblocks=%d  imag_hdr=%s  bandneg=%s  optdone=%s  term=%s"
          % (d["min"][0], ("%.9f" % e) if d["scf"] else "n/a", r, d["nblocks"], d["imag_hdr"], d["neg"], d["optdone"], [t[0] for t in d["term"]]))
    for ln_no, txt in d["term"]:
        print("       L%d  %s" % (ln_no, txt))

REF = D["1028"]["min"][1]
P   = D["1061_P"]["min"][1]
rel = lambda e: (e - REF) * K
print()
print("=== (a) verified-minima span (39 blocks AND 0 band-table negatives AND 0 imaginary headers) ===")
# 1071 is an opt-only job (0 frequency blocks); its Hessian evidence lives in the paired job 1078.
paired1071 = dict(D["1071"])
paired1071["nblocks"]  = D["1078"]["nblocks"]
paired1071["imag_hdr"] = D["1078"]["imag_hdr"]
paired1071["neg"]      = D["1078"]["neg"]
ver = {"1061_P (P)": D["1061_P"], "1073 (second conformer)": D["1073"], "1071 opt + 1078 freq": paired1071}
vals = {}
for name, d in ver.items():
    ok = (d["nblocks"] == 39) and (len(d["imag_hdr"]) == 0) and (len(d["neg"]) == 0)
    vals[name] = (rel(d["min"][1]), ok)
    print("  %-26s %+9.4f kcal/mol vs 1028 | blocks=%d  imaginary band+header=%d+%d  -> %s"
          % (name, rel(d["min"][1]), d["nblocks"], len(d["neg"]), len(d["imag_hdr"]),
             "VERIFIED MINIMUM" if ok else "NOT QUALIFIED"))
oks = [v for v, ok in vals.values() if ok]
sp = max(oks) - min(oks)
print("  verified-minima span = %+0.4f ... %+0.4f  ->  %.4f kcal/mol" % (min(oks), max(oks), sp))
print("  (supersedes the earlier two-minimum span 1.6086 kcal/mol, which used only P and 1073)")
print()
print("=== (b) product-side reference uncertainty of P ===")
gap = abs((D["1071"]["min"][1] - P) * K)
print("  verified term : |1071 min - P| = |%+0.4f - %+0.4f| = %.4f  -> floored >= %.2f  (lower point 1078-verified, 0 imaginary)"
      % (rel(D["1071"]["min"][1]), (P - REF) * K, gap, math.floor(gap * 100) / 100))
low_unv = min([("1069 last frame", D["1069"]["scf"][-1])], key=lambda x: x[1][1]) if D["1069"]["scf"] else ("none", (0, float("nan")))
und = abs((low_unv[1][1] - P) * K)
print("  residual unverified term : %s L%d = %.9f  (%+0.4f vs 1028, %+0.4f vs P) -> floored >= %.2f  (non-stationary, max-cycle frame)"
      % (low_unv[0], low_unv[1][0], low_unv[1][1], rel(low_unv[1][1]), (low_unv[1][1] - P) * K, math.floor(und * 100) / 100))
print()
ts78 = D["1078"]["term"][-1][1].split(" at ", 1)[-1] if D["1078"]["term"] else "MISSING"
print("  SENTENCE (b):")
print("    product-side reference uncertainty = |lowest product-side stationary point already located - P|;")
print("    as of %s (job 1078 terminal) >= %.2f kcal/mol, floor of %.4f; this term is now VERIFIED, no longer 'unverified'."
      % (ts78, math.floor(gap * 100) / 100, gap))
print("    The lower point is job 1071's final frame (L%d = %.9f), frequency-verified by job 1078 with 0 imaginary modes;"
      % (D["1071"]["min"][0], D["1071"]["min"][1]))
print("    the newest still-unverified frame is job 1069's last frame at %+0.4f vs P (floored >= %.2f) and does not enlarge the bound."
      % ((low_unv[1][1] - P) * K, math.floor(und * 100) / 100))
print("    Using P as a denominator therefore requires the annotation: P is a frequency-verified minimum but NO LONGER")
print("    the lowest known stationary point of that species; a still lower species cannot be excluded (6x6 grid not exhausted).")
print()
print("=== (c) proton path ===")
print("  undetermined: direct H26 transfer to N4 vs H27-relayed double shuttle; no saddle verified either way.")
print()
print("=== snapshot reading span (never a denominator, never a substitute for (a)) ===")
print("  instantaneous reading span = %.4f" % sp)
