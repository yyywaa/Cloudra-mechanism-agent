#!/usr/bin/env python3
"""Exact search for two rotations that place H6 (atom 11) of an E3 guess onto the point
T = O1 + 1.25*unit(O3-O1) after the methoxide azimuth op1.  Prints tool ops; writes no coordinates."""
import math
import numpy as np

def read_xyz(p):
    L = open(p).read().splitlines(); n = int(L[0].split()[0])
    el = []; X = []
    for l in L[2:2+n]:
        s = l.split(); el.append(s[0]); X.append([float(s[1]), float(s[2]), float(s[3])])
    return el, np.array(X)

def rot1(p, ap, u, deg):
    a = math.radians(deg); v = p - ap; par = u*(v@u); per = v - par
    return ap + par + per*math.cos(a) + np.cross(u, per)*math.sin(a)

def rot(P, ap, u, deg):
    a = math.radians(deg); v = P - ap
    par = np.outer(v@u, u); per = v - par
    cr = np.cross(np.tile(u, (len(P), 1)), per)
    return ap + par + per*math.cos(a) + cr*math.sin(a)

el, X = read_xyz("gold_finish_20261015/NY3/prep/i2.xyz")
Na, O3, C4, O1, H6 = X[0], X[2], X[6], X[8], X[10]
u1 = (C4-Na)/np.linalg.norm(C4-Na)
# op1: methoxide {2..6} about Na...C4, O1...O3 -> 2.500
best = min(((abs(np.linalg.norm(O1-rot1(O3, Na, u1, d)) - 2.5), d) for d in np.arange(-180, 180.0001, 0.01)))
deg1 = best[1]
X1 = X.copy(); X1[[1, 2, 3, 4, 5]] = rot(X[[1, 2, 3, 4, 5]], Na, u1, deg1)
O1, O3, H6 = X1[8], X1[2], X1[10]
T = O1 + 1.25*(O3-O1)/np.linalg.norm(O3-O1)
print("op1: rotate atoms [2,3,4,5,6] axis_atoms [1,7] %.2f deg -> |O1-O3| = %.4f" % (deg1, np.linalg.norm(O1-O3)))
print("T: |T-O1| = %.4f  |T-O3| = %.4f" % (np.linalg.norm(T-O1), np.linalg.norm(T-O3)))

lines = [(i, j, X1[i], (X1[j]-X1[i])/np.linalg.norm(X1[j]-X1[i])) for i in range(11) for j in range(11) if i != j]
sols = []
for (i, j, ap1, ua) in lines:
    c1 = ap1 + ua*((H6-ap1)@ua); r1 = np.linalg.norm(H6-c1)
    e1 = (H6-c1)/r1
    e2 = np.cross(ua, e1)
    a1s = np.arange(0, 360, 0.25)
    P = c1[None, :] + r1*(np.cos(np.radians(a1s))[:, None]*e1[None, :] + np.sin(np.radians(a1s))[:, None]*e2[None, :])
    for (k, l, ap2, ub) in lines:
        if (k, l) == (i, j): continue
        rt = np.linalg.norm(T - ap2 - ub*((T-ap2)@ub))
        d = P - ap2
        f = np.einsum('ij,ij->i', d, d) - (d@ub)**2 - rt*rt
        sgn = np.sign(f); ch = np.where(sgn[:-1]*sgn[1:] < 0)[0]
        for c in ch:
            lo, hi = a1s[c], a1s[c+1]
            flo = f[c]
            for _ in range(40):
                mid = 0.5*(lo+hi)
                pm = c1 + r1*(math.cos(math.radians(mid))*e1 + math.sin(math.radians(mid))*e2)
                dm = pm - ap2; fm = dm@dm - (dm@ub)**2 - rt*rt
                if flo*fm <= 0: hi = mid
                else: lo, flo = mid, fm
            a1 = 0.5*(lo+hi)
            p1 = c1 + r1*(math.cos(math.radians(a1))*e1 + math.sin(math.radians(a1))*e2)
            v1 = p1 - ap2; q1 = v1 - ub*(v1@ub)
            vt = T - ap2; qt = vt - ub*(vt@ub)
            cc = (q1@qt)/(np.linalg.norm(q1)*np.linalg.norm(qt))
            a2 = math.degrees(math.acos(max(-1.0, min(1.0, cc))))
            if np.dot(np.cross(q1, qt), ub) < 0: a2 = -a2
            err = np.linalg.norm(rot1(p1, ap2, ub, a2) - T)
            if err < 1e-6:
                sols.append((i+1, j+1, round(a1, 2), k+1, l+1, round(a2, 2), err))
print("exact two-rotation solutions:", len(sols))
for s in sols[:30]:
    print("  rot[11] ax(%d,%d) %.2f  then rot[11] ax(%d,%d) %.2f   (err %.2e)" % s)
