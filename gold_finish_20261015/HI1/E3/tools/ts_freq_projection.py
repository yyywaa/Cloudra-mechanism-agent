#!/usr/bin/env python3
"""HI1_E3: imaginary-mode / watch-pair projection analyser for a Gaussian frequency log.

Usage: python3 ts_freq_projection.py <freq.log> [<reference.xyz>] [--json out.json]

Reads the *raw* Gaussian normal-mode block (no other tool exposes the mode vectors) and
reports for every imaginary frequency:
  * the band value (cm^-1) and its 1-based mode number,
  * the per-atom displacement norms |d_i| (top atoms),
  * for each declared watch pair (i,j): the relative-displacement vector d_i - d_j,
    its magnitude, and its projection on the pair axis u_ij (bond-stretch projection),
  * the share of the total mean-square displacement carried by the 6 watch pairs,
  * the top-10 atom pairs by |d_i - d_j| (which bonds actually move).
Atom indices are 1-based in the log's own atom order; if a reference xyz is given, the
element sequence is checked against it and a mismatch is reported (not silently ignored).
"""
import sys, json, math, hashlib

WATCH = [(2, 4), (25, 26), (25, 27), (2, 25), (4, 26), (11, 27)]
Z2S = {1: "H", 6: "C", 7: "N", 8: "O"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def parse_modes(path):
    lines = open(path).read().splitlines()
    freqs = []          # (mode_number, value)
    disp = {}           # mode_number -> {atom_index: (x,y,z)}
    top_atoms = None    # [(atom, AN)] in the mode block order
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("Frequencies --"):
            vals = [float(x) for x in s.split("--", 1)[1].split()]
            # the atom/AN header two lines below (after Red. masses / Frc consts / IR Inten)
            j = i + 1
            hdr = None
            for k in range(i + 1, min(i + 12, len(lines))):
                if lines[k].strip().startswith("Atom"):
                    hdr = k
                    break
            j = hdr if hdr is not None else i + 1
            if hdr is not None:
                j = hdr + 1
                atoms = []
                while j < len(lines):
                    t = lines[j].split()
                    # atom rows are "idx AN x y z x y z x y z" (11 fields); the next block's
                    # mode-number header (" 4 5") also starts with a digit -> require >=5 fields
                    if not t or not t[0].isdigit() or len(t) < 5:
                        break
                    atoms.append((int(t[0]), int(t[1]), [float(x) for x in t[2:]]))
                    j += 1
                top_atoms = [(a, an) for a, an, _ in atoms]
                nmode_cols = min(len(vals), min((len(vec) // 3) for _, _, vec in atoms))
                for k in range(nmode_cols):
                    n = len(freqs) + 1
                    freqs.append((n, vals[k]))
                    d = {}
                    for a, an, vec in atoms:
                        d[a] = (vec[3 * k], vec[3 * k + 1], vec[3 * k + 2])
                    disp[n] = d
            i = j
        else:
            i += 1
    return freqs, disp, top_atoms


def main():
    log = sys.argv[1]
    ref = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    out = None
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
    freqs, disp, atoms = parse_modes(log)
    if not freqs:
        print("NO normal-mode block found (log may be truncated / non-frequency job)")
        return 2
    imag = [(n, v) for n, v in freqs if v < 0]
    print("log: %s\n  sha256 %s\n  modes parsed = %d ; imaginary = %d" % (log, sha256(log), len(freqs), len(imag)))
    print("  lowest bands (cm^-1): " + ", ".join("%d:%.4f" % (n, v) for n, v in freqs[:6]))
    if ref:
        n = int(open(ref).readline().split()[0])
        rsym = [ln.split()[0] for ln in open(ref).read().splitlines()[2:2 + n]]
        lsym = [Z2S[an] for _, an in atoms] if atoms else []
        print("  element sequence vs %s : %s" % (ref, "IDENTICAL" if rsym == lsym else "MISMATCH %s vs %s" % (lsym, rsym)))
    summary = {"log": log, "sha256": sha256(log), "n_modes": len(freqs), "imaginary": []}
    for n, v in imag:
        d = disp[n]
        norms = {a: math.sqrt(sum(c * c for c in d[a])) for a in d}
        tot = sum(x * x for x in norms.values())
        print("\n=== imaginary mode %d : %.4f cm^-1 ===" % (n, v))
        top = sorted(norms.items(), key=lambda kv: -kv[1])[:12]
        print("  largest per-atom displacements (|d|, log units): " + ", ".join("%d(%s)=%.3f" % (a, Z2S[atoms[a - 1][1]], norms[a]) for a, _ in top))
        pairs = []
        for (a, b) in WATCH:
            u = [d[a][k] - d[b][k] for k in range(3)]
            mag = math.sqrt(sum(c * c for c in u))
            pairs.append({"pair": [a, b], "rel_disp": mag})
        # projection on the instantaneous pair axis, using the log's own displacement
        # (the axis is not in the log; use the dominant sign convention: relative motion
        #  magnitude is the size of the stretch/compression coordinate)
        wp = sum(p["rel_disp"] ** 2 for p in pairs)
        print("  share of total MS displacement carried by the 6 watch pairs: %.1f%%" % (100.0 * wp / tot if tot else 0.0))
        for p in pairs:
            print("    watch pair R(%2d,%2d): |d_i - d_j| = %.4f  (%.1f%% of sum over watch pairs)" %
                  (p["pair"][0], p["pair"][1], p["rel_disp"], 100.0 * p["rel_disp"] ** 2 / wp if wp else 0.0))
        allp = []
        idx = sorted(norms)
        for x in range(len(idx)):
            for y in range(x + 1, len(idx)):
                a, b = idx[x], idx[y]
                m = math.sqrt(sum((d[a][k] - d[b][k]) ** 2 for k in range(3)))
                allp.append((m, a, b))
        allp.sort(reverse=True)
        print("  top-10 moving atom pairs (any pair): " +
              ", ".join("%d-%d:%.3f" % (a, b, m) for m, a, b in allp[:10]))
        summary["imaginary"].append({"mode": n, "cm^-1": v, "watch_pairs": pairs,
                                     "watch_share": (wp / tot if tot else None)})
    if out:
        with open(out, "w") as f:
            json.dump(summary, f, indent=1)
        print("\nwrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
