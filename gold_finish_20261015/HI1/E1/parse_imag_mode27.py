#!/usr/bin/env python3
"""Characterise imaginary modes of a Gaussian frequency log (HI1_E1 27-atom split model).
All numbers are read from the log; atom identity follows the file order (working order 1-based)."""
import sys, math

WORK = {2:"C2", 3:"O4(carbonyl)", 4:"C3", 10:"H22", 18:"N20", 27:"H21",
        12:"C(COOH)", 11:"O(=O)", 13:"O(OH)", 14:"Calpha", 19:"H(COOH)"}
MAP  = {2:"map2", 3:"map4", 4:"map3", 10:"map22", 18:"map20", 27:"map21",
        12:"map14", 11:"map13", 13:"map15", 14:"map16", 19:"-"}
WATCH = [(2,18,"C2-N20"), (3,27,"O4-H21"), (18,27,"N20-H21"), (2,3,"C2=O4")]

def num(s):
    out = []
    for t in s.replace(",", " ").split():
        try: out.append(float(t))
        except ValueError: pass
    return out

def parse(path):
    lines = open(path, errors="replace").read().splitlines()
    natoms = 0
    for L in lines:
        s = L.strip()
        if s.startswith("NAtoms="):
            natoms = int(s.split("=")[1].split()[0]); break
    imag_hdr = [(i+1, L.strip()) for i, L in enumerate(lines) if "imaginary frequencies" in L]
    bands = []
    for i, L in enumerate(lines):
        s = L.strip()
        if s.startswith("Frequencies --"):
            fr = num(s.split("--", 1)[1])
            red = num(lines[i+1].split("--", 1)[1]) if i+1 < len(lines) else []
            frc = num(lines[i+2].split("--", 1)[1]) if i+2 < len(lines) else []
            bands.append({"line": i+1, "freq": fr, "red": red, "frc": frc, "start": i})
    modes = []
    for b in bands:
        j = b["start"]
        while j < len(lines) and not ("Atom" in lines[j] and "AN" in lines[j]):
            j += 1
        if j >= len(lines): continue
        rows = []
        for k in range(natoms):
            parts = lines[j+1+k].split()
            if len(parts) < 5: break
            rows.append((int(parts[0]), [float(x) for x in parts[2:]]))
        for c in range(3):
            vec = [(an, vals[3*c:3*c+3]) for an, vals in rows if len(vals) >= 3*c+3]
            modes.append({"freq": b["freq"][c] if c < len(b["freq"]) else None,
                          "red": b["red"][c] if c < len(b["red"]) else None,
                          "frc": b["frc"][c] if c < len(b["frc"]) else None,
                          "line": b["line"], "vec": vec})
    return natoms, imag_hdr, bands, modes

def main(path):
    natoms, imag_hdr, bands, modes = parse(path)
    print("natoms =", natoms, "| Frequencies blocks =", len(bands), "| total modes =", 3*len(bands))
    print("imaginary header lines:", imag_hdr if imag_hdr else "NONE")
    neg = [(i+1, m) for i, m in enumerate(modes) if m["freq"] is not None and m["freq"] < 0]
    print("negative modes from band table:", [(k, m["freq"]) for k, m in neg])
    if bands: print("lowest real band (first table value):", bands[0]["freq"][0], "at line", bands[0]["line"])
    for k, m in neg:
        v = {an: vec for an, vec in m["vec"]}
        mag = {an: math.sqrt(sum(c*c for c in vec)) for an, vec in v.items()}
        tot = sum(mag.values())
        print("")
        print("=== imaginary mode #%d freq=%.4f cm-1 red.mass=%.4f frc.const=%.6f (table line %d)" % (k, m["freq"], m["red"], m["frc"], m["line"]))
        for an in sorted(mag, key=lambda a: -mag[a]):
            print("  atom %2d %-14s %-6s |d|=%.4f share=%.3f" % (an, WORK.get(an,""), MAP.get(an,""), mag[an], mag[an]/tot))
        print("  sum|d| = %.4f" % tot)
        for i, j, name in WATCH:
            if i in v and j in v:
                di, dj = v[i], v[j]
                cos = sum(di[t]*dj[t] for t in range(3))/(mag[i]*mag[j]) if mag[i]*mag[j] > 0 else 0.0
                print("  watch %-8s (%d,%d) frac=%.3f cos=%.3f" % (name, i, j, (mag[i]+mag[j])/tot, cos))
        if 27 in v: print("  H21 vector:", ["%.4f" % c for c in v[27]])
        print("  top:", [(a, WORK.get(a,""), round(mag[a]/tot,3)) for a in sorted(mag, key=lambda a: -mag[a])[:6]])
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
