# post-freeze asset: E1a dihedral audit v2 — BOTH sign conventions with self-tests (IUPAC: cis/syn-periplanar = 0, anti = 180)
import numpy as np
from rdkit import Chem
PT = Chem.GetPeriodicTable()
p = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split/E1A_constrained_scan_R2692_2192_stepneg.log"
ls = open(p).read().splitlines()

def dih_raw(p1, p2, p3, p4):          # cross-product order as in my earlier scripts (gives 180-tau)
    b1 = p2 - p1; b2 = p3 - p2; b3 = p4 - p3
    n1 = np.cross(b1, b2); n2 = np.cross(b2, b3)
    m = np.cross(n1, b2 / np.linalg.norm(b2))
    return float(np.degrees(np.arctan2(float(np.dot(m, n2)), float(np.dot(n1, n2)))))

def dih_std(p1, p2, p3, p4):          # IUPAC-ish: n2 order flipped -> cis = 0
    return -dih_raw(p1, p2, p3, p4)

# --- self tests (planar cases) ---
p1 = np.array([0., 0., 0.]); p2 = np.array([1., 0., 0.]); p3 = np.array([1.5, 1., 0.])
cis = np.array([2.5, 1., 0.]); anti = np.array([2.5, -1., 0.])
perp = np.array([2.5, 0.0, 1.0])
print("ST cis(syn)   raw=%8.3f std=%8.3f  (expect std 0)" % (dih_raw(p1, p2, p3, cis), dih_std(p1, p2, p3, cis)))
print("ST anti       raw=%8.3f std=%8.3f  (expect std +-180)" % (dih_raw(p1, p2, p3, anti), dih_std(p1, p2, p3, anti)))
print("ST perp(~90)  raw=%8.3f std=%8.3f  (expect std ~+-90)" % (dih_raw(p1, p2, p3, perp), dih_std(p1, p2, p3, perp)))

oc = [i for i, l in enumerate(ls) if 'Optimization completed' in l]
def frame_before(idx):
    h = [j for j in range(idx) if 'Standard orientation' in ls[j]][-1]
    d = [k for k in range(h, h + 10) if ls[k].strip().startswith('-----')]
    at = []; k = d[1] + 1
    while not ls[k].strip().startswith('-----'):
        q = ls[k].split(); at.append((int(q[1]), float(q[3]), float(q[4]), float(q[5]))); k += 1
    assert len(at) == 27
    return h + 1, at

rows = []
for n, i in enumerate(oc, 1):
    hdr, at = frame_before(i)
    X = np.array([[x, y, z] for _, x, y, z in at])
    j = [k for k in range(i) if 'SCF Done' in ls[k]][-1]
    E = float(ls[j].split('=')[1].split()[0])
    raw = dih_raw(X[2], X[1], X[17], X[13]); std = -raw
    rows.append((n, hdr, j + 1, E, float(np.linalg.norm(X[1] - X[17])), raw, std))
print("elems 1..27:", ''.join(PT.GetElementSymbol(at[i - 1][0]) for i in range(1, 28)), "| atoms 3,2,18,14 =",
      PT.GetElementSymbol(at[2][0]), PT.GetElementSymbol(at[1][0]), PT.GetElementSymbol(at[17][0]), PT.GetElementSymbol(at[13][0]))
for r in rows:
    print("sp%-2d hdr L%-6d SCF L%-6d E=%.9f R(2,18)=%.4f  tau_raw=%8.2f  tau_std=%8.2f" % r)
raw = [r[5] for r in rows]; std = [r[6] for r in rows]
print("raw  sp1..sp11:", " ".join("%.2f" % v for v in raw))
print("std  sp1..sp11:", " ".join("%.2f" % v for v in std))
def unwrap(seq):
    out = [seq[0]]
    for v in seq[1:]:
        prev = out[-1]; d = v - prev
        while d > 180: d -= 360
        while d < -180: d += 360
        out.append(prev + d)
    return out
ur = unwrap(raw); us = unwrap(std)
print("raw unwrapped:", " ".join("%.1f" % v for v in ur), "=> total change %.2f" % (ur[-1] - ur[0]))
print("std unwrapped:", " ".join("%.1f" % v for v in us), "=> total change %.2f" % (us[-1] - us[0]))
print("sp4->sp5: raw %.2f -> %.2f (naive %.2f, wrapped %.2f) ; std %.2f -> %.2f (wrapped %.2f)" % (
    raw[3], raw[4], raw[4] - raw[3], ((raw[4] - raw[3] + 180) % 360) - 180, std[3], std[4], ((std[4] - std[3] + 180) % 360) - 180))
print("360-(139.03+152.93) = %.2f" % (360 - (139.03 + 152.93)))
