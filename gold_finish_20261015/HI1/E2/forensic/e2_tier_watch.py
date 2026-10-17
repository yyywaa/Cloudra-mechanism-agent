#!/usr/bin/env python3
# read-only watcher for HI1/E2 1D scan: exits 0 (ready) once
#   (a) Normal/Error termination appears in the log, OR
#   (b) any *converged* scan point falls in proton tier 1 or tier 2
# Tier definitions (1-based working atom order, same as v2 judge):
#   R(28,24) = donor O...H ; R(11,24) = acceptor O...H
#   tier0: R(28,24) > 1.50
#   tier1: 1.20 <= R(28,24) <= 1.50
#   tier2: R(28,24) <= 1.10 and R(11,24) >= 1.50
# Extra flag 'shared' when tier1 and 1.0 <= R(11,24) <= 1.6
import sys, math

LOG = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"

def main():
    with open(LOG, "r", errors="replace") as fh:
        lines = fh.readlines()
    term = [i for i, l in enumerate(lines)
            if ("Normal termination" in l or "Error termination" in l)]
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        if lines[i].strip().startswith("Standard orientation:"):
            j = i + 1
            dashes = 0
            while j < n and dashes < 2:
                if lines[j].strip().startswith("-----"):
                    dashes += 1
                j += 1
            if dashes < 2:
                i += 1
                continue
            coords = {}
            k = j
            while k < n and not lines[k].strip().startswith("-----"):
                parts = lines[k].split()
                if len(parts) == 6:
                    try:
                        idx = int(parts[0]); Z = int(parts[1])
                        coords[idx] = (Z, float(parts[3]), float(parts[4]), float(parts[5]))
                    except ValueError:
                        pass
                k += 1
            blocks.append((k, coords))
            i = k
        else:
            i += 1
    done = [i for i, l in enumerate(lines) if "Optimization completed" in l]
    pts = []
    for d in done:
        cand = [b for b in blocks if b[0] < d]
        if not cand:
            continue
        coords = cand[-1][1]
        if not all(a in coords for a in (11, 24, 28)):
            continue
        def dist(a, b):
            pa, pb = coords[a], coords[b]
            return math.dist(pa[1:], pb[1:])
        r28_24 = dist(28, 24); r11_24 = dist(11, 24)
        if r28_24 > 1.50:
            tier = 0
        elif r28_24 <= 1.10 and r11_24 >= 1.50:
            tier = 2
        elif 1.20 <= r28_24 <= 1.50:
            tier = 1
        else:
            tier = "unclassified"
        shared = (tier == 1 and 1.0 <= r11_24 <= 1.6)
        pts.append(dict(line=d + 1, r28_24=round(r28_24, 4),
                        r11_24=round(r11_24, 4), tier=tier, shared=shared))
    hit_tier = [p for p in pts if p["tier"] in (1, 2)]
    ready = bool(term) or bool(hit_tier)
    print(dict(lines=len(lines), term_lines=[t + 1 for t in term],
               n_converged=len(pts), points=pts, hit_tier=hit_tier, ready=ready))
    return 0 if ready else 1

if __name__ == "__main__":
    sys.exit(main())
