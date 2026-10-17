#!/usr/bin/env python3
"""HI1 lane1: install the (S)-RC seed and the merged-TS guess into the ts_0004
canonical binding order.

Canonical order = ts/ts_0004 declared reactant order (heavy atoms in declared
reactant-SMILES order, then hydrogens in RDKit AddHs order), verified against
ts/ts_0004/build/input_0001/reactant/generated_seed.mol (41 atoms / 40 bonds).

Source files are in job_51/ORCA atom order (41 atoms); this script changes atom
ORDER ONLY - every coordinate is copied verbatim, nothing is re-optimised.
"""
import hashlib, os

BASE = "/home/ly/Cloudra-mechanism-agent"
RC       = BASE + "/gold_finish_20261015/HI1/E1/build/RC_start.xyz"
GUESS    = BASE + "/gold_finish_20261015/HI1/E1/build/TS_guess_merged.xyz"
CANONMOL = BASE + "/ts/ts_0004/build/input_0001/reactant/generated_seed.mol"
OUTDIR   = BASE + "/gold_finish_20261015/HI1/E1/lane1"
os.makedirs(OUTDIR, exist_ok=True)

# canonical index (1-based) -> job_51/ORCA index (1-based) in the two source files
PERM = {1:3, 2:2, 3:25, 4:1, 5:14, 6:15, 7:16, 8:12, 9:13, 10:27,
        11:28, 12:29, 13:30, 14:31, 15:32, 16:33, 17:34, 18:35, 19:36, 20:37,
        21:38, 22:39, 23:40, 24:41, 25:10, 26:9, 27:11, 28:8, 29:7, 30:6,
        31:5, 32:4, 33:24, 34:23, 35:21, 36:22, 37:19, 38:20, 39:17, 40:18, 41:26}
assert sorted(PERM.values()) == list(range(1, 42)), "not a bijection"

def read_xyz(path):
    lines = open(path).read().splitlines()
    n = int(lines[0].split()[0])
    A = []
    for ln in lines[2:2 + n]:
        f = ln.split()
        A.append((f[0], float(f[1]), float(f[2]), float(f[3])))
    assert len(A) == n
    return n, lines[1], A

def d(a, b):
    return ((a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2) ** 0.5

mlines = open(CANONMOL).read().splitlines()
cnt = mlines[3].split()
nat, nbo = int(cnt[0]), int(cnt[1])
assert nat == 41 and nbo == 40, (nat, nbo)
canon_lines = mlines[4:4+nat]
bonds = [(int(l.split()[0]), int(l.split()[1]), int(l.split()[2]))
         for l in mlines[4+nat:4+nat+nbo]]

n_rc, rc_com, rc = read_xyz(RC)
n_g, g_com, g = read_xyz(GUESS)
assert n_rc == 41

def reorder(A):
    return [A[PERM[i]-1] for i in range(1, 42)]

rc_c, g_c = reorder(rc), reorder(g)

# element identity: permuted source symbol must equal the canonical mol symbol
bad = []
for i in range(41):
    sym = canon_lines[i][31:34].strip()
    if sym != rc_c[i][0] or sym != g_c[i][0]:
        bad.append((i+1, sym, rc_c[i][0], g_c[i][0]))
print("element-identity mismatches:", bad)

def bondcheck(name, A):
    worst = (0.0, None)
    for (i, j, o) in bonds:
        dd = d(A[i-1], A[j-1])
        if dd > worst[0]:
            worst = (dd, (i, j, o))
    print(name + " max bond length = %.3f A at %s" % (worst[0], worst[1]))

bondcheck("RC_canonical", rc_c)
bondcheck("TS_guess_canonical", g_c)

PAIRS = [("C2-N20", 2, 32), ("C2=O4", 2, 3), ("C2-C3", 2, 4), ("C3-H22", 4, 10),
         ("N20-H21", 32, 41), ("O4-H22", 3, 10), ("O4-H21", 3, 41)]
for tag, A in (("RC", rc_c), ("TSguess", g_c)):
    print(tag + " " + "  ".join("%s=%.3f" % (n, d(A[i-1], A[j-1])) for n, i, j in PAIRS))

def write_xyz(path, comment, A):
    with open(path, "w") as fh:
        fh.write("41\n" + comment + "\n")
        for (s, x, y, z) in A:
            fh.write("%-2s %14.8f %14.8f %14.8f\n" % (s, x, y, z))

def write_mol(path, A):
    with open(path, "w") as fh:
        fh.write(mlines[0] + "\n" + mlines[1] + "\n" + mlines[2] + "\n" + mlines[3] + "\n")
        for i in range(41):
            fh.write("%10.4f%10.4f%10.4f" % (A[i][1], A[i][2], A[i][3]) + canon_lines[i][30:] + "\n")
        for (i, j, o) in bonds:
            fh.write("%3d%3d%3d  0\n" % (i, j, o))
        fh.write("M  END\n")

rc_xyz  = OUTDIR + "/RC_S_canonical.xyz"
rc_mol  = OUTDIR + "/RC_S_canonical.mol"
g_xyz   = OUTDIR + "/TS_guess_merged_canonical.xyz"
g_mol   = OUTDIR + "/TS_guess_merged_canonical.mol"
write_xyz(rc_xyz, "HI1_E1 (S)-RC seed (job 907 input geometry) reordered into ts_0004 canonical binding order; source E1/build/RC_start.xyz sha f4eb0ba6f085114c97cb13bcdbe03a8613a2f95262782bcb5fb9da5c6d9b93c0", rc_c)
write_mol(rc_mol, rc_c)
write_xyz(g_xyz, "HI1_E1 merged single-TS guess reordered into ts_0004 canonical binding order; source E1/build/TS_guess_merged.xyz sha 74d3d3e12d6c48398857a986a29034546b9fb93ace4388fe2a2d4fbbcc87fe13", g_c)
write_mol(g_mol, g_c)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

for p in (rc_xyz, rc_mol, g_xyz, g_mol):
    print("WROTE", p, sha(p))

try:
    from rdkit import Chem
    from rdkit.Chem import rdDetermineBonds
    def cip(path):
        m = Chem.MolFromXYZFile(path)
        m = Chem.Mol(m)
        rdDetermineBonds.DetermineBonds(m, charge=0)
        Chem.AssignStereochemistryFrom3D(m)
        Chem.AssignCIPLabels(m)
        return [(a.GetIdx()+1, a.GetSymbol(), a.GetProp("_CIPCode"))
                for a in m.GetAtoms() if a.HasProp("_CIPCode")]
    print("RDKit CIP (canonical idx, sym, CIP)  RC_canonical:", cip(rc_xyz))
    print("RDKit CIP (canonical idx, sym, CIP)  TSguess_canonical:", cip(g_xyz))
except Exception as e:
    print("RDKit CIP check unavailable:", repr(e))
