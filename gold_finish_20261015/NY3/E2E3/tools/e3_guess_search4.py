#!/usr/bin/env python3
"""E3-guess ops search (v4): rotations only (the Na...H6 contact makes any 'stretch' an illegal
non-rigid op on the perceived graph).  Search: rotate the methoxide about the Na...C4 line by theta,
then rotate H6 (atom 11) about an atom-pair line by a, such that the final H6 is 1.25 A from BOTH
O1 and O3 (with |O1...O3| kept close to 2.50 and |C4...O3| untouched at the I2 value)."""
import math
import numpy as np

def read_xyz(p):
    L = open(p).read().splitlines(); n = int(L[0].split()[0]); el = []; X = []
    for l in L[2:2+n]:
        s = l.split(); el.append(s[0]); X.append([float(s[1]), float(s[2]), float(s[3])])
    return el, np.array(X)

el, X = read_xyz("gold_finish_20261015/NY3/prep/i2.xyz")
Na, O3, C4, O1, H6 = X[0], X[2], X[6], X[8], X[10]
ua = (C4-Na)/np.linalg.norm(C4-Na)

def rot1(p, ap, u, deg):
    a = math.radians(deg); v = p-ap; par = u*(v@u); per = v-par
    return ap + par + per*math.cos(a) + np.cross(u, per)*math.sin(a)

lines = [(i, j, X[i], (X[j]-X[i])/np.linalg.norm(X[j]-X[i])) for i in range(11) for j in range(11) if i != j]
sols = []
for theta in np.arange(-180, 180, 0.05):
    O3t = rot1(O3, Na, ua, theta)
    d13 = np.linalg.norm(O1-O3t)
    if not (2.30 <= d13 <= 2.502): continue
    for (i, j, ap, u) in lines:
        if i in (0, 1, 2, 3, 4, 5) and j in (0, 1, 2, 3, 4, 5) and i != 0:
            pass
        v = H6-ap; par = u*(v@u); per = v-par; r = np.linalg.norm(per)
        if r < 1e-6: continue
        e1 = per/r; e2 = np.cross(u, e1)
        m = (ap+par)-O1
        A = m@m + r*r; B = 2*r*(m@e1); C = 2*r*(m@e2)
        K = 1.25**2 - A; R = math.hypot(B, C)
        if abs(K) > R: continue
        phi = math.atan2(C, B)
        for s in (1, -1):
            a_ang = math.asin(max(-1, min(1, K/R)))
            av = (a_ang if s > 0 else math.pi - a_ang) - phi
            p = ap + par + r*(math.cos(av)*e1 + math.sin(av)*e2)
            d1 = np.linalg.norm(p-O1); d3 = np.linalg.norm(p-O3t)
            if abs(d1-1.25) > 0.005 or abs(d3-1.25) > 0.005: continue
            ang13 = math.degrees(math.acos(max(-1, min(1, ((O1-p)@(O3t-p))/(np.linalg.norm(O1-p)*np.linalg.norm(O3t-p))))))
            if ang13 < 150: continue
            # clash check with all other atoms
            mind = 9.0; arg = None
            for k in range(11):
                if k in (8, 2, 10): continue
                dd = np.linalg.norm(p-X[k])
                if dd < mind: mind, arg = dd, k+1
            sols.append(dict(theta=round(float(theta), 2), i=i+1, j=j+1, a=round(math.degrees(av), 2),
                             d13=round(d13, 3), ang13=round(ang13, 1), mind=round(mind, 2), arg=arg))
print("solutions:", len(sols))
sols.sort(key=lambda s: (-s["ang13"], -s["mind"]))
for s in sols[:20]: print("  ", s)
