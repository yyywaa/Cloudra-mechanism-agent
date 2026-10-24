#!/usr/bin/env python3
"""HI1_E1b D1 report (self-contained, supersedes freq_mode_d1.py for reporting).

Print order (mandatory, D28 lesson -- never trust a bare atom number):
  0) identity table 1..27 (element + role asserted from the reactant geometry's neighbours)
  1) neighbour table (<2.0 A) for every candidate reaction-centre atom
  2) imaginary mode: value + line number, (b) three shares + largest single DOF
  3) (a) direction of each declared pair, with TWO explicit scales:
        s   = (d_j - d_i).u   , u unit vector along r_ij, d = Gaussian printed
              (unnormalised) Cartesian eigenvector (a.u., 2 decimals in the log)
        dR  = same quantity after rescaling the whole mode to |d|_total = 0.1 A
     verdict uses SIGNS only (form pairs must decrease, break pairs must increase).

Declared pairs (1-based, working order = INT1_27 order):
   form  (2,4) C2-C3 , (3,10) O4-H22
   break (4,10) C3-H22 , (2,3) C2-O4
Candidate atoms for the checks: 2,3,4,10 (pairs) + 18 (N20) + 27 (H21).
"""
import sys, math, hashlib, itertools

FORM  = [(2, 4), (3, 10)]
BREAK = [(4, 10), (2, 3)]
PAIR_ATOMS = sorted({a for p in FORM + BREAK for a in p})
CHECK_ATOMS = [2, 3, 4, 10, 18, 27]
ROLE = {1:"C1 methyl (map1)", 2:"C2 carbinolamine carbon (map2)", 3:"O4 hydroxyl O -> water O (map4)",
        4:"C3 alpha-methylene / enamine CH2 (map3)", 8:"H on C3", 9:"H on C3",
        10:"H22 alpha-H of C3 (map22)", 11:"O13 carboxyl C=O", 12:"C14 carboxyl C",
        13:"O15 carboxyl OH", 14:"C16 ring C-alpha (S)", 18:"N20 ring N (map20)", 27:"H21 N-H proton, now on O4 (map21)"}

def rd_xyz(p):
    L = open(p).read().split("\n")
    n = int(L[0].split()[0])
    at, X = [], []
    for l in L[2:2 + n]:
        s = l.split(); at.append(s[0]); X.append((float(s[1]), float(s[2]), float(s[3])))
    return at, X

def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

def orientation_blocks(L):
    out = []; i = 0
    while i < len(L):
        if L[i].strip() in ("Standard orientation:", "Input orientation:"):
            kind = L[i].strip()[:4]
            j = i
            while j < len(L) and "-----" not in L[j]: j += 1
            j += 1
            while j < len(L) and "-----" not in L[j]: j += 1
            j += 1
            tab = []
            while j < len(L) and "-----" not in L[j]:
                s = L[j].split()
                if len(s) == 6 and s[0].isdigit():
                    tab.append((int(s[0]), int(s[1]), float(s[3]), float(s[4]), float(s[5])))
                j += 1
            if tab: out.append((i + 1, kind, tab))
            i = j
        else:
            i += 1
    return out

def freq_blocks(L):
    out = []; i = 0
    while i < len(L):
        if L[i].startswith(" Frequencies --"):
            freqs = [float(x) for x in L[i].split("--")[1].split()]
            ncol = len(freqs); j = i
            while j < len(L) and not L[j].startswith("  Atom  AN"): j += 1
            j += 1
            cols = [dict() for _ in range(ncol)]
            while j < len(L):
                s = L[j].split()
                if len(s) != 2 + 3 * ncol: break
                an = int(s[0])
                for c in range(ncol):
                    cols[c][an] = (float(s[2 + 3 * c]), float(s[3 + 3 * c]), float(s[4 + 3 * c]))
                j += 1
            out.append(dict(line=i + 1, freqs=freqs, modes=cols))
            i = j
        else:
            i += 1
    return out

def main():
    freq_log = sys.argv[1]
    ref_xyz = sys.argv[2] if len(sys.argv) > 2 else "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/INT1_27_opt_frame.xyz"
    print("freq log :", freq_log)
    print("sha256   :", hashlib.sha256(open(freq_log, "rb").read()).hexdigest())
    L = open(freq_log, errors="replace").read().split("\n")
    print("lines    :", len(L))
    ob = orientation_blocks(L); fb = freq_blocks(L)
    print("orientation blocks=%d  freq groups=%d  modes=%d" % (len(ob), len(fb), sum(len(b["freqs"]) for b in fb)))
    print("Normal term lines:", [i + 1 for i, l in enumerate(L) if "Normal termination" in l],
          " Error term lines:", [i + 1 for i, l in enumerate(L) if "Error termination" in l])
    for i, l in enumerate(L):
        if l.startswith(" Frequencies --") and any(float(x) < 0 for x in l.split("--")[1].split()):
            print("IMAGINARY freq line:", i + 1, "->", l.strip())
            break
    entries = [(f, b["line"], k, b["modes"][k]) for b in fb for k, f in enumerate(b["freqs"])]
    imag = [e for e in entries if e[0] < 0]
    print("imaginary mode count:", len(imag), ["%+.4f" % e[0] for e in imag])

    # ---- 0) identity table from the reference reactant frame (geometry only) ----
    at, X = rd_xyz(ref_xyz)
    print("\n=== 0) atom identity table (source:", ref_xyz, ") ===")
    for i, e in enumerate(at, 1):
        print("  %2d %-2s  %s" % (i, e, ROLE.get(i, "")))

    # ---- 1) neighbour table ----
    print("\n=== 1) neighbour table, cutoff 2.0 A (from the reference reactant frame) ===")
    for a in CHECK_ATOMS:
        nb = sorted(((dist(X[a - 1], X[b]), b + 1, at[b]) for b in range(len(at)) if b + 1 != a))
        s = "  atom %2d (%s): " % (a, at[a - 1])
        s += ", ".join("%d%s %.3f" % (b, e, d) for d, b, e in nb if d < 2.0)
        print(s)

    if not imag:
        print("\nNo imaginary frequency parsed -> (a)(b) cannot be judged."); return
    f, line, k, d = imag[0]
    geo = None
    for st, kind, tab in ob:
        if st < line and len(tab) == len(at) and kind == "Inpu":
            geo = tab
    if geo is None:
        for st, kind, tab in ob:
            if st < line and len(tab) == len(at): geo = tab
    pos = {t[0]: (t[2], t[3], t[4]) for t in geo}
    heavy = [t[0] for t in geo if t[1] != 1]
    tot = sum(d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2 for a in d)
    print("\n=== 2) mode %d  %+.4f cm-1  (Frequencies line %d) ===" % (k + 1, f, line))
    print("atoms in vector:", len(d), " |d|_total = %.6f (Gaussian a.u.^2 units)" % math.sqrt(tot))
    cen = sum(d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2 for a in PAIR_ATOMS)
    hv = sum(d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2 for a in heavy)
    frac = {a: (d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2) / tot for a in d}
    top = max(frac.items(), key=lambda kv: kv[1])
    comp = max(range(3), key=lambda c: abs(d[top[0]][c]))
    print("(b) share_center  (declared pair atoms %s) = %.4f" % (PAIR_ATOMS, cen / tot))
    print("(b) share_all_heavy                       = %.4f" % (hv / tot))
    print("(b) share_max_single_atom                 = %.4f  at atom %d (%s)" % (
        top[1], top[0], "heavy" if top[0] in heavy else "H"))
    print("(b) largest single DOF                    = atom %d, %s component, |d| = %.4f a.u." % (
        top[0], "xyz"[comp], abs(d[top[0]][comp])))
    for a, fr in sorted(frac.items(), key=lambda kv: -kv[1])[:8]:
        print("      atom %2d %-2s %.4f" % (a, at[a - 1], fr))

    scale = 0.1 / math.sqrt(tot)   # rescale the mode so |d|_total = 0.1 A
    print("")
    print("=== 3) (a) pair geometry (SHAPE only -- the eigenvector sign is arbitrary) ===")
    print("scale for dR: whole mode rescaled to |d|_total = 0.1 A (factor %.5f)" % scale)
    print("NOTE: a global sign flip of the mode negates every s and every dR below, so no")
    print("      direction may be read off the printed eigenvector sign (HL1_E1 audit).")
    print("      The sign-free statement is the SIGN PATTERN: shape-consistent <=> all form")
    print("      pairs share one sign and all break pairs share the opposite sign.")
    print("      Which side is reactant/TS must be pinned by the IRC endpoints.")
    sgn = {}
    for kind, pairs in (("form", FORM), ("break", BREAK)):
        for (i, j) in pairs:
            ux = pos[j][0] - pos[i][0]; uy = pos[j][1] - pos[i][1]; uz = pos[j][2] - pos[i][2]
            n = math.sqrt(ux * ux + uy * uy + uz * uz)
            u = (ux / n, uy / n, uz / n)
            s = ((d[j][0] - d[i][0]) * u[0] + (d[j][1] - d[i][1]) * u[1] + (d[j][2] - d[i][2]) * u[2])
            sgn[(kind, i, j)] = s
            print("  %-5s (%2d,%2d) %s-%s  r=%.4f A   s=%+.5f a.u.   dR=%+.4f A   (as printed)   %s" % (
                kind, i, j, at[i - 1], at[j - 1], n, s, s * scale,
                "distance decreasing" if s < 0 else "distance increasing"))
    fs = [1 if sgn[("form", i, j)] > 0 else -1 for (i, j) in FORM]
    bs = [1 if sgn[("break", i, j)] > 0 else -1 for (i, j) in BREAK]
    form_uniform = len(set(fs)) == 1
    break_uniform = len(set(bs)) == 1
    opposite = form_uniform and break_uniform and fs[0] != bs[0]
    print("  sign pattern: form pairs %s ; break pairs %s" % (fs, bs))
    if opposite:
        print("(a) SHAPE VERDICT (sign-free): form and break pairs move in OPPOSITE senses with")
        print("    uniform sign inside each group == single reaction coordinate, structurally")
        print("    consistent with the declared bond_changes. DIRECTION (which side is reactant)")
        print("    is NOT judged here -- it must be pinned by the IRC endpoints.")
    else:
        print("(a) SHAPE VERDICT (sign-free): NOT consistent with the declared bond_changes under")
        print("    any overall sign (form/break signs are not opposite) -> pseudo-saddle for this")
        print("    pairing; inspect the vector before any further claim.")
main()
