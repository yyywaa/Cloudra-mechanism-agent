#!/usr/bin/env python3
"""HI1_E1b D1 (a)(b) judge -- parse a Gaussian 16 frequency log and report the
imaginary mode composition (three normalisations) plus the net displacement
direction on each declared watch pair.

Declared reaction centre (working order = INT1_27 order, 1-based):
  form  (2,4) C2-C3 , (3,10) O4-H22
  break (4,10) C3-H22 , (2,3) C2-O4
For pair (i,j): u = (r_j - r_i)/|r_j - r_i| ; s = (d_j - d_i).u
  s<0 -> distance decreasing ; s>0 -> increasing.
  form pairs must have s<0 ; break pairs must have s>0  (same direction as bond_changes).
Normalisations: unweighted squared Cartesian displacement over the whole mode vector.
  share_center = sum_{a in declared pair atoms} |d_a|^2 / total
  share_heavy  = sum_{a heavy} |d_a|^2 / total
  share_max    = max_a |d_a|^2 / total  (which atom / which Cartesian component)
"""
import sys, math, hashlib

FORM  = [(2, 4), (3, 10)]
BREAK = [(4, 10), (2, 3)]
PAIR_ATOMS = sorted({a for p in FORM + BREAK for a in p})

def read_lines(p):
    return open(p, errors="replace").read().split("\n")

def orientation_blocks(L):
    out = []
    i = 0
    while i < len(L):
        if L[i].strip() in ("Standard orientation:", "Input orientation:"):
            j = i
            while j < len(L) and "-----" not in L[j]:
                j += 1
            j += 1
            while j < len(L) and "-----" not in L[j]:
                j += 1
            j += 1
            tab = []
            while j < len(L) and "-----" not in L[j]:
                s = L[j].split()
                if len(s) == 6 and s[0].isdigit():
                    tab.append((int(s[0]), int(s[1]), float(s[3]), float(s[4]), float(s[5])))
                j += 1
            if tab:
                out.append((i + 1, L[i].strip()[:4], tab))
            i = j
        else:
            i += 1
    return out

def freq_blocks(L):
    out = []
    i = 0
    while i < len(L):
        if L[i].startswith(" Frequencies --"):
            freqs = [float(x) for x in L[i].split("--")[1].split()]
            ncol = len(freqs)
            j = i
            while j < len(L) and not L[j].startswith("  Atom  AN"):
                j += 1
            j += 1
            cols = [dict() for _ in range(ncol)]
            while j < len(L):
                s = L[j].split()
                if len(s) != 2 + 3 * ncol:
                    break
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
    path = sys.argv[1]
    L = read_lines(path)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print("log            :", path)
    print("sha256         :", sha)
    print("lines          :", len(L))
    ob = orientation_blocks(L)
    fb = freq_blocks(L)
    nat = max(len(t) for _, _, t in ob)
    print("orientation blocks: %d  natoms(last)=%d  header(last)=%s" % (len(ob), len(ob[-1][2]), ob[-1][1]))
    print("freq groups    : %d  modes total: %d  (3N-6 = %d)" % (
        len(fb), sum(len(b["freqs"]) for b in fb), 3 * nat - 6))
    term = [i + 1 for i, l in enumerate(L) if "Normal termination" in l]
    err = [i + 1 for i, l in enumerate(L) if "Error termination" in l]
    print("Normal termination lines:", term, " Error termination lines:", err)
    lowf = [(i + 1, l.strip()) for i, l in enumerate(L) if l.startswith(" Low frequencies")]
    for x in lowf:
        print("  lowfreq", x[0], x[1])
    entries = []
    for b in fb:
        for k, f in enumerate(b["freqs"]):
            entries.append((f, b["line"], k, b["modes"][k]))
    imag = [e for e in entries if e[0] < 0]
    print("imaginary      :", len(imag), ["%.4f (line %d)" % (e[0], e[1]) for e in imag])
    if not entries:
        print("no modes parsed"); return
    sel = imag if imag else entries[:1]
    for f, line, k, d in sel:
        geo = None
        for st, kind, tab in ob:
            if st < line and len(tab) == nat and kind == "Inpu":
                geo = tab
        if geo is None:
            for st, kind, tab in ob:
                if st < line and len(tab) == nat:
                    geo = tab
        pos = {t[0]: (t[2], t[3], t[4]) for t in geo}
        print("geometry source: last Input orientation block before freq (Input order = mode-vector order)")
        heavy = [t[0] for t in geo if t[1] != 1]
        tot = sum(d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2 for a in d)
        print("")
        print("=== mode %d  %+.4f cm-1  (Frequencies line %d) ===" % (k + 1, f, line))
        print("atoms in mode vector:", len(d), " total |d|^2 = %.6f a.u.^2" % tot)
        cen = sum(d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2 for a in PAIR_ATOMS)
        hv = sum(d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2 for a in heavy)
        frac = {a: (d[a][0] ** 2 + d[a][1] ** 2 + d[a][2] ** 2) / tot for a in d}
        top = max(frac.items(), key=lambda kv: kv[1])
        print("(b) share_center(declared pair atoms %s) = %.4f" % (PAIR_ATOMS, cen / tot))
        print("(b) share_all_heavy                     = %.4f" % (hv / tot))
        print("(b) share_max_single_atom               = %.4f  at atom %d (%s)" % (
            top[1], top[0], "heavy" if top[0] in heavy else "H"))
        a = top[0]
        comp = max(range(3), key=lambda c: abs(d[a][c]))
        print("(b) largest DOF                         = atom %d %s (|d| = %.4f a.u.)" % (
            a, "xyz"[comp], abs(d[a][comp])))
        print("top per-atom fractions:")
        for at, fr in sorted(frac.items(), key=lambda kv: -kv[1])[:8]:
            print("    atom %2d  %.4f" % (at, fr))
        print("(a) pair direction test (form wants s<0, break wants s>0):")
        ok = True
        for kind, pairs in (("form", FORM), ("break", BREAK)):
            for (i, j) in pairs:
                ux = pos[j][0] - pos[i][0]; uy = pos[j][1] - pos[i][1]; uz = pos[j][2] - pos[i][2]
                n = math.sqrt(ux * ux + uy * uy + uz * uz)
                u = (ux / n, uy / n, uz / n)
                s = (d[j][0] - d[i][0]) * u[0] + (d[j][1] - d[i][1]) * u[1] + (d[j][2] - d[i][2]) * u[2]
                want = -1 if kind == "form" else 1
                good = (s * want) > 0
                ok = ok and good
                print("    %-5s (%2d,%2d)  r = %.4f  s = %+.4f  %-8s %s" % (
                    kind, i, j, n, s, "OK" if good else "MISMATCH",
                    "decreasing" if s < 0 else "increasing"))
        print("(a) verdict:", "same direction as bond_changes" if ok else "PSEUDO-SADDLE (reverse direction)")
main()
