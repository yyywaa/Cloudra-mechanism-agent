#!/usr/bin/env python3
"""Read-only forensics for the last (un-converged) frame of a Gaussian scan log and for the
Error-termination context. Prints only; writes nothing.
Usage: python3 diag_lastframe.py <log>"""
import sys, math

ELEM = {1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne"}
MASS = {"H":1.008,"C":12.011,"N":14.007,"O":15.999}

log = sys.argv[1]
L = open(log, "r", errors="replace").read().split(chr(10))

def parse(start):
    i = start + 1
    while not L[i].strip().startswith("---"):
        i += 1
    i += 1
    while not L[i].strip().startswith("---"):
        i += 1
    i += 1
    a = []
    while not L[i].strip().startswith("---"):
        t = L[i].split()
        if len(t) >= 6:
            a.append((ELEM.get(int(t[1]), "X"), [float(t[3]), float(t[4]), float(t[5])]))
        i += 1
    return a

def d(a, b):
    return math.sqrt(sum((a[k] - b[k]) ** 2 for k in range(3)))

so = [i for i, l in enumerate(L) if "Standard orientation:" in l]
scf = [i for i, l in enumerate(L) if l.strip().startswith("SCF Done:")]
print("### last frame in the log (line %d)" % (so[-1] + 1))
A = parse(so[-1])
print("- atoms parsed:", len(A))
print("- R(1,29) = %.4f  (design value for scan point 9 = %.4f)" % (d(A[0][1], A[28][1]), 4.3543 - 8 * 0.2))
print("- R(28,24) = R(O28-H24) = %.4f ; R(O11-H24) = %.4f ; R(28,29) = %.4f ; R(2,4) = %.4f"
      % (d(A[27][1], A[23][1]), d(A[10][1], A[23][1]), d(A[27][1], A[28][1]), d(A[1][1], A[3][1])))
mins = (9e9, "")
for i in range(len(A)):
    for j in range(i + 1, len(A)):
        m = d(A[i][1], A[j][1])
        if m < mins[0]:
            mins = (m, "%s%d-%s%d" % (A[i][0], i + 1, A[j][0], j + 1))
print("- minsep = %.4f (%s)" % mins)
print("- last SCF Done: L%d %s" % (scf[-1] + 1, L[scf[-1]].strip()))
print()
print("### termination context, verbatim (last 20 lines of the log)")
for i in range(max(0, len(L) - 20), len(L)):
    print("%7d: %r" % (i + 1, L[i]))
print()
print("### failure counters")
print("- total lines with 'New curvilinear step failed':", sum(1 for l in L if "New curvilinear step failed" in l))
print("- total lines with 'FormB failed':", sum(1 for l in L if "FormB failed" in l))
print("- first 'FormB failed' line:", [i + 1 for i, l in enumerate(L) if "FormB failed" in l][:3])
print("- 'Error imposing constraints' line:", [i + 1 for i, l in enumerate(L) if "Error imposing constraints" in l])
print("- 'Error termination' line:", [i + 1 for i, l in enumerate(L) if "Error termination" in l])
print()
print("### scan point reach summary")
oc = [i + 1 for i, l in enumerate(L) if l.strip() == "Optimization completed."]
print("- Optimization completed at lines:", oc)
print("- number of converged scan points:", len(oc))
lastpt = None
for l in L:
    if "on scan point" in l:
        lastpt = l.strip()
print("- last scan-point/step line:", lastpt)
print("- M declared in log:", sorted(set(int(l.split("out of")[-1].split()[0]) for l in L if "on scan point" in l)))