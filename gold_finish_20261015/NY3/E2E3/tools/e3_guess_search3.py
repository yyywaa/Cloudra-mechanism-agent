#!/usr/bin/env python3
"""E3-guess ops search (v3): after the methoxide azimuth op, set |O1-H6| = 1.25 (stretch), then find the
single rotation of H6 (about an atom-pair line) that best aligns the O1->H6 direction with O1->O3,
then a final stretch back to exactly 1.25.  Prints tool ops only; no coordinates are written."""
import math
import numpy as np

def read_xyz(p):
    L = open(p).read().splitlines(); n = int(L[0].split()[0]); el = []; X = []
    for l in L[2:2+n]:
        s = l.split(); el.append(s[0]); X.append([float(s[1]), float(s[2]), float(s[3])])
    return el, np.array(X)

def rot1(p, ap, u, deg):
    a = math.radians(deg); v = p - ap; par = u*(v@u); per = v - par
    return ap + par + per*math.cos(a) + np.cross(u, per)*math.sin(a)
def rot(P, ap, u, deg):
    a = math.radians(deg); v = P - ap; par = np.outer(v@u, u); per = v - par
    return ap + par + per*math.cos(a) + np.cross(np.tile(u, (len(P), 1)), per)*math.sin(a)
def stretch(X, i, j, L):
    """translate the j-side fragment along i->j (single-atom j side: move atom j only)"""
    u = (X[j]-X[i])/np.linalg.norm(X[j]-X[i]); X2 = X.copy(); X2[j] = X[i] + L*u; return X2

el, X = read_xyz("gold_finish_20261015/NY3/prep/i2.xyz")
Na, O3, C4, O1, H6 = X[0], X[2], X[6], X[8], X[10]
u1 = (C4-Na)/np.linalg.norm(C4-Na)
sol = [(abs(np.linalg.norm(O1-rot1(O3, Na, u1, d))-2.5), d) for d in np.arange(-180, 180.0001, 0.01)]
deg1 = min(sol)[1]
X1 = X.copy(); X1[[1,2,3,4,5]] = rot(X[[1,2,3,4,5]], Na, u1, deg1)
print("op1 rotate [2,3,4,5,6] axis [1,7] %.2f deg -> |O1-O3| = %.4f (|Na-O3| %.3f, |C4...O3| %.3f)" % (
    deg1, np.linalg.norm(X1[8]-X1[2]), np.linalg.norm(X1[0]-X1[2]), np.linalg.norm(X1[6]-X1[2])))
X2 = stretch(X1, 8, 10, 1.25)                      # 0-based: 8=O1, 10=H6
print("op2 stretch [9,11] -> 1.25  (|O1-H6| = %.4f, |O3...H6| = %.4f)" % (
    np.linalg.norm(X2[8]-X2[10]), np.linalg.norm(X2[2]-X2[10])))
O1, O3, H6 = X2[8], X2[2], X2[10]
w = (O3-O1)/np.linalg.norm(O3-O1)
best = None
for i in range(11):
    for j in range(11):
        if i == j: continue
        u = (X2[j]-X2[i])/np.linalg.norm(X2[j]-X2[i]); ap = X2[i]
        ang = np.arange(-180, 180, 0.05)
        v = H6-ap; par = u*(v@u); per = v-par
        cr = np.cross(u, per)
        pos = ap + par + np.cos(np.radians(ang))[:, None]*per + np.sin(np.radians(ang))[:, None]*cr
        d = pos-O1; dn = d/np.linalg.norm(d, axis=1)[:, None]
        cosd = dn@w
        k = int(np.argmax(cosd))
        if best is None or cosd[k] > best[0]:
            best = (float(cosd[k]), i+1, j+1, float(ang[k]), float(np.degrees(np.arccos(min(1, cosd[k])))))
print("best op3: rotate [11] axis_atoms [%d,%d] %.2f deg -> direction error %.3f deg (cos %.6f)" % (
    best[1], best[2], best[3], best[4], best[0]))
X3 = X2.copy(); X3[10] = rot1(H6, X2[best[1]-1], (X2[best[2]-1]-X2[best[1]-1])/np.linalg.norm(X2[best[2]-1]-X2[best[1]-1]), best[3])
print("  after op3: |O1-H6| = %.4f |O3...H6| = %.4f" % (np.linalg.norm(X3[8]-X3[10]), np.linalg.norm(X3[2]-X3[10])))
X4 = stretch(X3, 8, 10, 1.25)
print("op4 stretch [9,11] -> 1.25  => FINAL |O1-H6| = %.4f  |O3...H6| = %.4f  |O1...O3| = %.4f  |C4...O3| = %.4f" % (
    np.linalg.norm(X4[8]-X4[10]), np.linalg.norm(X4[2]-X4[10]), np.linalg.norm(X4[8]-X4[2]), np.linalg.norm(X4[6]-X4[2])))
mind = 9; pair = None
for a in range(11):
    for b in range(a+1, 11):
        if {a, b} in ({0,1},{0,2},{0,6},{0,7},{0,8},{1,2},{1,3},{1,4},{1,5},{2,1}): continue
        dd = np.linalg.norm(X4[a]-X4[b])
        if dd < mind: mind, pair = dd, (a+1, b+1)
print("closest non-bonded-ish pair in final geometry: %s %.3f A" % (pair, mind))
print("final coordinate set:")
for k in range(11):
    print("   %-2s %12.6f %12.6f %12.6f" % (el[k], X4[k][0], X4[k][1], X4[k][2]))
