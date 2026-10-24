#!/usr/bin/env python3
"""HL1_E1 mode-analysis: imaginary-mode direction + composition.

Usage: analyze_mode.py <gaussian_freq.log> [--center 1,2,9] [--break 1,2] [--form 2,9] [--heavy 1,5,6,7,8,9,10]

Rules (primary-coordinator ruling 1):
  (a) direction gate: for the declared bond_changes the imaginary mode must shorten the
      forming pair and lengthen the breaking pair.
  (b) record-only composition shares: declared reaction-centre atoms / all heavy atoms /
      largest single atom (all normalised on the unweighted squared Cartesian displacements
      of the whole mode).
No percentage threshold is applied.
"""
import sys, math, re

def read_log(path):
    return open(path, errors="replace").read().splitlines()

def parse_geoms(lines):
    geoms = []
    i = 0
    while i < len(lines):
        if "Standard orientation:" in lines[i] or "Input orientation:" in lines[i]:
            j = i + 5
            atoms = []
            while j < len(lines) and "-----" not in lines[j]:
                f = lines[j].split()
                if len(f) >= 6:
                    try:
                        atoms.append((int(f[0]), int(f[1]), float(f[3]), float(f[4]), float(f[5])))
                    except ValueError:
                        pass
                j += 1
            if atoms:
                geoms.append((i + 1, atoms))
            i = j
        i += 1
    return geoms

def parse_modes(lines):
    """Return list of dicts: freq, atoms{idx:[x,y,z]} (Gaussian eigenvector table)."""
    modes = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("Frequencies --"):
            vals = [float(x) for x in re.findall(r"-?\d+\.\d+", lines[i])]
            ncol = len(vals)
            # find the atom table header after this line
            k = i + 1
            rows = {}
            while k < len(lines) and k < i + 8:
                if "Atom" in lines[k] and "AN" in lines[k]:
                    k += 1
                    while k < len(lines):
                        f = lines[k].split()
                        if len(f) < 2 + 3 * ncol:
                            break
                        try:
                            an = int(f[0])
                            nums = [float(x) for x in f[2:2 + 3 * ncol]]
                        except ValueError:
                            break
                        rows[an] = nums
                        k += 1
                    break
                k += 1
            for c in range(ncol):
                vec = {}
                for an, nums in rows.items():
                    vec[an] = nums[3 * c:3 * c + 3]
                modes.append({"freq": vals[c], "vec": vec})
            i = k
        i += 1
    return modes

def dist(g, a, b):
    pa, pb = g[a - 1][2:], g[b - 1][2:]
    return math.dist(pa, pb)

def unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return [c / n for c in v] if n else [0, 0, 0]

def report(logpath, center=(1, 2, 9), brk=(1, 2), form=(2, 9), heavy=(1, 5, 6, 7, 8, 9, 10), amp=None):
    lines = read_log(logpath)
    geoms = parse_geoms(lines)
    modes = parse_modes(lines)
    if not modes:
        print("NO mode table found"); return
    imag = [m for m in modes if m["freq"] < 0]
    print(f"log: {logpath}")
    print(f"modes parsed: {len(modes)}  imaginary: {len(imag)}  values: {[round(m['freq'],4) for m in imag]}")
    if not imag:
        print("(a) DIRECTION GATE: no imaginary mode -> not a TS"); return
    # geometry: last geometry block before the first Frequencies line
    firstfreq_line = next(i for i, l in enumerate(lines) if l.lstrip().startswith("Frequencies --"))
    cand = [g for g in geoms if g[0] < firstfreq_line + 1]
    geom = (cand[-1] if cand else geoms[-1])[1]
    n = len(geom)
    m0 = imag[0]
    vec = m0["vec"]
    if not vec:
        print("no eigenvector table"); return
    # scale: Gaussian prints normalised (unit-norm over mass-weighted?) eigenvectors.
    # Use raw vector; also report a 0.10 amplitude image for distance changes.
    s2 = sum(c * c for a in vec.values() for c in a)
    print(f"mode freq = {m0['freq']:.4f} cm-1 ; atom rows = {len(vec)} ; sum(d^2) = {s2:.6f} ; unit-norm-per-block assumed")
    for a, v in sorted(vec.items()):
        vn = math.sqrt(sum(c * c for c in v))
        print(f"  atom {a:2d} {geom[a-1][1]:2d}  d=({v[0]: .4f},{v[1]: .4f},{v[2]: .4f}) |d|={vn:.4f} share={vn*vn/max(s2,1e-12):.4f}")
    # (a) direction
    scale = amp if amp else 0.10
    print(f"--- (a) DIRECTION (image displacement amplitude {scale} A along the raw eigenvector) ---")
    res = {}
    for pair in (brk, form, (brk[0], form[1])):
        d0 = dist(geom, *pair)
        plus = [tuple(geom[a - 1][2 + k] + scale * vec[a][k] for k in range(3)) for a in range(1, n + 1)]
        minus = [tuple(geom[a - 1][2 + k] - scale * vec[a][k] for k in range(3)) for a in range(1, n + 1)]
        dp = math.dist(plus[pair[0] - 1], plus[pair[1] - 1])
        dm = math.dist(minus[pair[0] - 1], minus[pair[1] - 1])
        res[pair] = (d0, dp, dm)
        print(f"  R{pair} = {d0:.4f} A ; +img = {dp:.4f} (d={dp-d0:+.4f}) ; -img = {dm:.4f} (d={dm-d0:+.4f})")
    d0b, dpb, dmb = res[brk]
    d0f, dpf, dmf = res[form]
    print(f"  breaking pair {brk}: +img {'LENGTHENS' if dpb>d0b else 'shortens'} ({dpb-d0b:+.4f}); "
          f"forming pair {form}: +img {'SHORTENS' if dpf<d0f else 'lengthens'} ({dpf-d0f:+.4f})")
    ok = (dpb > d0b) and (dpf < d0f)
    print(f"  (a) verdict: {'PASS (same sign as declared bond_changes, +img direction)' if ok else 'FAIL for +img; check -img'}")
    if (dmb < d0b) and (dmf > d0f):
        print("  (a) note: -img image is the reaction-forward direction (same sign as declared); gate is sign-symmetric.")
    # amplitude sanity: is the watch-pair motion above the numerical-noise level set by the
    # dominant atom? (reported, no threshold)
    pair_amp = max(math.sqrt(sum(c * c for c in vec[a])) for a in set(center) if a in vec)
    topa = max(math.sqrt(sum(c * c for c in v)) for v in vec.values())
    print(f"  amplitude: max |d| on declared centre = {pair_amp:.4f} ; max |d| over all atoms = {topa:.4f} ; "
          f"ratio = {pair_amp/topa if topa else float('nan'):.4f}")
    # projection of H2 displacement onto O1->O7 axis
    o1 = geom[0][2:]; o7 = geom[8][2:]
    u = unit([o7[k] - o1[k] for k in range(3)])
    dh = vec[2]
    print(f"  u(O1->O7) = ({u[0]: .4f},{u[1]: .4f},{u[2]: .4f}) ; d(H2) = ({dh[0]: .4f},{dh[1]: .4f},{dh[2]: .4f}) "
          f"; u.d(H2) = {sum(u[k]*dh[k] for k in range(3)): .4f}")
    # (b) composition shares
    tot = sum(sum(c * c for c in a) for a in vec.values())
    def share(atoms):
        return sum(sum(c * c for c in vec[a]) for a in atoms if a in vec) / tot
    cshare = share(center)
    hshare = share(heavy)
    print("--- (b) COMPOSITION (record only, no threshold) ---")
    print(f"  share on declared reaction-centre atoms {tuple(center)} = {cshare:.4f}")
    print(f"  share on all heavy atoms {tuple(heavy)} = {hshare:.4f}")
    top = max(vec.items(), key=lambda kv: sum(c * c for c in kv[1]))
    tv = top[1]
    tn = math.sqrt(sum(c * c for c in tv))
    comp = ["x", "y", "z"][max(range(3), key=lambda k: abs(tv[k]))]
    print(f"  largest single atom = atom {top[0]} ({geom[top[0]-1][1]}, {'H' if geom[top[0]-1][1]==1 else 'heavy'}) "
          f"share = {tn*tn/tot:.4f}, dominant Cartesian component = {comp} ({tv[max(range(3), key=lambda k: abs(tv[k]))]:+.4f})")
    soft = ""
    if top[0] not in center:
        soft = "soft-mode-dominated (largest share on an atom outside the declared centre)"
    print(f"  (b) note: {soft if soft else 'largest share inside declared reaction centre'}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--amp", type=float, default=0.10)
    a = ap.parse_args()
    report(a.log, amp=a.amp)
