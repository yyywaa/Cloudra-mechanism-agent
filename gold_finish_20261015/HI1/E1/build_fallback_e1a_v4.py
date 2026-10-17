#!/usr/bin/env python3
"""Fallback (a) for HI1_E1a, v4: keep the RC_27 acetone fragment RIGID and slide it
along the C2->N18 axis until R(C2-N18) = 2.10 A. Proline fragment and H21 are taken
unchanged from RC_27 (the transferring proton therefore stays on N18).
No rotation is applied, so every internal acetone distance is preserved exactly and
R(C2-N18) is strictly monotonic in the displacement. Inputs are on-disk tool frames."""
import numpy as np
from numpy.linalg import norm

S = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E1/split"
A_PATH = S + "/RC_27_opt_frame.xyz"
OUT    = S + "/E1A_fallback_earlyattack_R210.xyz"
TARGET = 2.10

L = open(A_PATH).read().splitlines(); n = int(L[0].split()[0])
els = [f.split()[0] for f in L[2:2+n]]
X = np.array([[float(x) for x in f.split()[1:4]] for f in L[2:2+n]])
assert n == 27
C2, O3, C3, H22, N18, H21 = 1, 2, 3, 9, 17, 26
ACETONE = list(range(0, 10))

R0 = float(norm(X[C2] - X[N18]))
u = (X[N18] - X[C2]) / R0
delta = R0 - TARGET
Y = X.copy()
Y[ACETONE] = X[ACETONE] + delta * u

def r(Z, i, j): return float(norm(Z[i] - Z[j]))
print("RC_27 R(C2-N18) = %.4f A ; displacement along the C2->N18 axis = %.4f A" % (R0, delta))
print("u (C2->N18 unit vector) = (%.6f, %.6f, %.6f)" % tuple(u))
print("")
print("after the slide:")
for nm, (i, j) in [("R(C2-N18)", (C2, N18)), ("R(C2-O3)", (C2, O3)), ("R(N18-H21)", (N18, H21)),
                   ("R(O3-H21)", (O3, H21)), ("R(O3-N18)", (O3, N18)), ("R(C1-C2)", (0, 1)),
                   ("R(C2-C3)", (C2, C3)), ("R(C3-H22)", (C3, H22)), ("R(O13-H19)", (12, 18))]:
    print("  %-12s: %.4f" % (nm, r(Y, i, j)))
print("")
print("table (fraction f of the same slide direction; f=1.0 gives 2.10 A):")
prev = None; mono = True; rows = []
for fr in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0]:
    Z = X.copy(); Z[ACETONE] = X[ACETONE] + fr * delta * u
    val = r(Z, C2, N18)
    ms = min(norm(Z[i] - Z[j]) for i in range(27) for j in range(i+1, 27))
    rows.append((fr, val, ms))
for fr, val, ms in rows:
    print("  f=%.1f  R(C2-N18)=%.4f  minsep=%.4f  (minsep atoms below)" % (fr, val, ms))
sv = [row[1] for row in rows]
mono = all(sv[i] > sv[i+1] for i in range(len(sv)-1))
print("strictly monotonic decreasing =", mono)

ms = None; pair = None
for i in range(27):
    for j in range(i+1, 27):
        d = r(Y, i, j)
        if ms is None or d < ms: ms, pair = d, (i+1, j+1, els[i], els[j])
print("minsep at the target frame: %.4f A between atoms %d(%s) and %d(%s)" % (ms, pair[0], pair[2], pair[1], pair[3]))

with open(OUT, "w") as fh:
    fh.write("%d\n" % n)
    fh.write("E1a fallback(a) early attack: RC_27 acetone slid %.3f A along C2->N18 (no rotation); R(C2-N18)=%.3f A; proline+H21 unchanged from RC_27" % (delta, r(Y, C2, N18)))
    fh.write("\n")
    for e, c in zip(els, Y):
        fh.write("%-2s %14.8f %14.8f %14.8f\n" % (e, c[0], c[1], c[2]))
print("written:", OUT)
