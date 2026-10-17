#!/usr/bin/env python3
"""Part E: single-implementation RMSD matrix (standard definition) + per-atom deviations.
   RMSD = sqrt( (1/N) * sum_i |r_i^A - r_i^B|^2 ) after proper-rotation Kabsch superposition,
   all N=41 atoms in the canonical work order, mass-unweighted."""
import numpy as np
from rdkit import Chem, RDLogger
RDLogger.DisableLog("rdApp.*")
ROOT = "/home/ly/Cloudra-mechanism-agent"
RUN = ROOT + "/ts/ts_0011"; JOB = RUN + "/jobs/declaration_0004"; E3 = ROOT + "/gold_finish_20261015/HI1/E3"
N = 41; Z = {1: "H", 6: "C", 7: "N", 8: "O"}
def rd(p):
    with open(p, errors="replace") as f: return f.read().splitlines()
def DASH(s): return s.strip().startswith("-----") and len(s.strip()) > 20
def last_frame(path):
    L = rd(path); hdr = None
    for k, s in enumerate(L):
        if s.strip().startswith("Standard orientation:"): hdr = k
    assert hdr is not None, path
    j = hdr + 1; dsh = []
    while len(dsh) < 2:
        if DASH(L[j]): dsh.append(j)
        j += 1
    start = dsh[1] + 1; a = []; k = start
    while len(a) < N:
        p = L[k].split()
        if len(p) == 6 and p[0].isdigit(): a.append((Z[int(p[1])], *map(float, p[3:6]))); k += 1
        else: raise AssertionError("bad row L%d %r" % (k + 1, L[k]))
    assert DASH(L[k]), "no closing dashes"
    return a, start + 1
def all_frames(path):
    L = rd(path); out = []; i = 0
    while i < len(L):
        s = L[i].strip()
        if s.startswith("Standard orientation:") or s.startswith("Input orientation:"):
            j = i + 1; dsh = []
            while len(dsh) < 2:
                if DASH(L[j]): dsh.append(j)
                j += 1
            st = dsh[1] + 1; a = []; k = st
            while len(a) < N:
                p = L[k].split(); a.append((Z[int(p[1])], *map(float, p[3:6]))); k += 1
            assert DASH(L[k]); out.append((a, st + 1)); i = k
        else: i += 1
    return out
def xyz(p):
    L = rd(p); n = int(L[0].split()[0])
    return [(q.split()[0], *map(float, q.split()[1:4])) for q in L[2:2 + n]]
def rmsd(A, B, sel=None):
    if sel is not None:
        A = [A[i] for i in sel]; B = [B[i] for i in sel]
    A = np.array([x[1:] for x in A], float); B = np.array([x[1:] for x in B], float)
    Ac = A - A.mean(0); Bc = B - B.mean(0)
    U, S, Vt = np.linalg.svd(Ac.T @ Bc)
    R = Vt.T @ np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]) @ U.T
    d = np.sqrt((((R @ Ac.T).T - Bc) ** 2).sum(1))
    return float(np.sqrt((d ** 2).mean())), d
F = {}
F["I2_min_961"], _ = last_frame(E3 + "/runs/I2_optfreq/I2_optfreq.log")
F["ts_999_final"], l = last_frame(JOB + "/ts_opt/refine.log");   print("ts final atoms start L%d" % l)
F["prod_opt_1041"], l = last_frame(JOB + "/product_opt/product_opt.log"); print("prod_opt final atoms start L%d" % l)
F["react_opt_1035"], l = last_frame(JOB + "/reactant_opt/reactant_opt.log"); print("react_opt final atoms start L%d" % l)
F["P_1061"], l = last_frame(E3 + "/runs/P_e3b/P_optfreq.log"); print("P final atoms start L%d" % l)
irc = all_frames(JOB + "/irc/irc.log")
print("irc frames:", [(i + 1, s) for i, (a, s) in enumerate(irc)])
F["irc_init"] = irc[0][0]; F["irc_fwd1"] = irc[1][0]; F["irc_rev1"] = irc[2][0]
F["I2_seed_xyz"] = xyz(RUN + "/build/input_0004/reactant/seed.xyz")
F["P_seed41_xyz"] = xyz(E3 + "/prep/P_e3b_product_41_seed.xyz")
print("\n## RMSD matrix (A, N=41, standard definition: sqrt(mean |dr|^2))")
names = list(F)
print("| pair | RMSD | RMSD(38 atoms, w/o methyl H 14,15,16) |")
print("|---|---|---|")
sel38 = [i for i in range(N) if i + 1 not in (14, 15, 16)]
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        r, _ = rmsd(F[names[i]], F[names[j]]); r38, _ = rmsd(F[names[i]], F[names[j]], sel38)
        if r > 3.0 and r38 > 3.0: continue
        print("| %s vs %s | %.4f | %.4f |" % (names[i], names[j], r, r38))
print("\n## per-atom deviation, prod_opt_1041 vs I2_min_961 (sorted)")
r, d = rmsd(F["prod_opt_1041"], F["I2_min_961"])
print("   RMSD=%.4f" % r)
for k in np.argsort(-d)[:10]:
    print("   w%-3d %s  dev=%.3f A" % (k + 1, F["I2_min_961"][k][0], d[k]))
print("   mean dev over the other 38 atoms = %.3f A" % np.sqrt((d[sel38] ** 2).mean()))
r2, d2 = rmsd(F["react_opt_1035"], F["I2_min_961"])
print("## per-atom deviation, react_opt_1035 vs I2_min_961: RMSD=%.4f max=%.3f" % (r2, d2.max()))
r3, d3 = rmsd(F["ts_999_final"], F["I2_min_961"])
print("## per-atom deviation, ts_999_final vs I2_min_961: RMSD=%.4f max=%.3f (atom w%d)" % (r3, d3.max(), int(np.argmax(d3)) + 1))
