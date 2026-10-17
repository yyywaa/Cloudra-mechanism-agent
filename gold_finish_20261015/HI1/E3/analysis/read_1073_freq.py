
import re, numpy as np
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, inchi, rdMolDescriptors
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

RUNS = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs"
LOG  = RUNS + "/build_seed_product_optfreq.log"
PLOG = RUNS + "/P_e3b/P_optfreq.log"
REF  = "SMPZMOQIWMNUBG-YBVIJTQESA-N"
PT = Chem.GetPeriodicTable()

def lines_of(p):
    with open(p) as f:
        return f.read().splitlines()

def frame_at(lines, hdr_idx):
    assert 'Standard orientation' in lines[hdr_idx], lines[hdr_idx]
    dashes = [j for j in range(hdr_idx, hdr_idx+10) if lines[j].strip().startswith('-----')]
    assert len(dashes) >= 2, dashes
    start = dashes[1] + 1
    atoms, j = [], start
    while not lines[j].strip().startswith('-----'):
        p = lines[j].split()
        assert len(p) == 6, (j+1, lines[j])
        atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5])))
        j += 1
    return atoms, start, j

def xyz_block(atoms, title):
    out = [str(len(atoms)), title]
    for z, x, y, zz in atoms:
        out.append("%-3s %14.8f %14.8f %14.8f" % (PT.GetElementSymbol(z), x, y, zz))
    return "\n".join(out) + "\n"

def perceive(atoms):
    m = Chem.MolFromXYZBlock(xyz_block(atoms, "frame"))
    assert m is not None
    rdDetermineBonds.DetermineBonds(m, charge=0)
    return m

def report(tag, atoms, hdr_line, abl, abr):
    m = perceive(atoms)
    s = inchi.MolToInchi(m); k = inchi.InchiToInchiKey(s)
    frags = Chem.GetMolFrags(m, asMols=True, sanitizeFrags=True)
    hb = sum(1 for b in m.GetBonds() if b.GetBeginAtom().GetAtomicNum()>1 and b.GetEndAtom().GetAtomicNum()>1)
    pos = np.array([[x,y,z] for _,x,y,z in atoms])
    print("### %s | hdr L%d | atom block L%d-L%d | NAtoms=%d" % (tag, hdr_line, abl, abr, len(atoms)))
    print("formula     :", rdMolDescriptors.CalcMolFormula(m))
    print("inchi       :", s)
    print("inchikey    :", k)
    print("ref         :", REF)
    print("key_match   :", k == REF, "| diff_positions:", ([] if k==REF else [i for i in range(min(len(k),len(REF))) if k[i]!=REF[i]]))
    print("components  :", [(rdMolDescriptors.CalcMolFormula(f), inchi.InchiToInchiKey(inchi.MolToInchi(f))) for f in frags])
    print("heavy_bonds :", hb, "| total_bonds:", m.GetNumBonds(), "| charged:", [(a.GetIdx()+1,a.GetSymbol(),a.GetFormalCharge()) for a in m.GetAtoms() if a.GetFormalCharge()!=0])
    if len(frags)==2:
        idx = Chem.GetMolFrags(m); A=pos[list(idx[0])]; B=pos[list(idx[1])]
        d = np.linalg.norm(A[:,None,:]-B[None,:,:],axis=2)
        print("min interfragment dist: %.4f A" % d.min())
    return m

L = lines_of(LOG)
hdrs = [i for i,l in enumerate(L) if 'Standard orientation' in l]
print("LOG 'Standard orientation' headers (1-based):", [i+1 for i in hdrs])
af, s1, e1 = frame_at(L, hdrs[-1])
ao, s2, e2 = frame_at(L, hdrs[-2])
print("freq final frame atom block: L%d-L%d (next line L%d starts dashes)" % (s1+1, e1, e1+1))
A = np.array([[x,y,z] for _,x,y,z in af]); B = np.array([[x,y,z] for _,x,y,z in ao])
print("max|delta| prev-block vs freq-final-block = %.6f A | elem seq identical = %s" % (np.abs(A-B).max(), [a[0] for a in af]==[a[0] for a in ao]))
m = report("1073 freq final frame", af, hdrs[-1]+1, s1+1, e1)
print("--- 1073 log-order distances ---")
def d(i,j): return float(np.linalg.norm(A[i-1]-A[j-1]))
for (i,j,lab) in [(2,4,'C2...N4'),(2,25,'C2-O25'),(4,26,'N4-H26'),(25,26,'O25-H26'),(10,27,'O10-H27'),(9,10,'C9-O10'),(9,11,'C9-O11'),(2,3,'C2-O3')]:
    print("  %-8s R(%2d,%2d)=%8.4f  (%s-%s)" % (lab,i,j,d(i,j),PT.GetElementSymbol(af[i-1][0]),PT.GetElementSymbol(af[j-1][0])))
freqs=[]; fstart=None
for i,l in enumerate(L):
    if 'Frequencies --' in l:
        if fstart is None: fstart=i+1
        freqs += [float(x) for x in re.findall(r'-?\d+\.\d+', l.split('--',1)[1])]
print("--- frequencies (first group line L%d) ---" % fstart)
print("groups=%d modes=%d 3N-6=%d" % (sum(1 for l in L if 'Frequencies --' in l), len(freqs), 3*len(af)-6))
print("negatives:", [f for f in freqs if f<0], "| 'imaginary' header lines:", sum(1 for l in L if 'imaginary' in l))
print("group1 first value: %.4f" % freqs[0])
for lo,hi,name in [(-1e9,200,'<200'),(200,800,'200-800'),(800,1800,'800-1800'),(1800,1e9,'>1800')]:
    print("  %-9s : %d" % (name, sum(1 for f in freqs if lo<=f<hi)))
print("min %.4f  max %.4f" % (min(freqs), max(freqs)))
P = lines_of(PLOG)
ph = [i for i,l in enumerate(P) if 'Standard orientation' in l]
print("P_optfreq.log headers total=%d last3=%s" % (len(ph), [i+1 for i in ph[-3:]]))
pa, ps, pe = frame_at(P, ph[-1])
report("P (job 1061) last frame", pa, ph[-1]+1, ps+1, pe)
open("gold_finish_20261015/HI1/E3/analysis/1073_freq_final_frame.xyz","w").write(xyz_block(af, "1073 freq final frame; source build_seed_product_optfreq.log L%d (41 atoms, log order)" % (s1+1)))
open("gold_finish_20261015/HI1/E3/analysis/P_1061_last_frame.xyz","w").write(xyz_block(pa, "P job1061 last frame; source P_optfreq.log L%d (41 atoms, log order)" % (ps+1)))
print("wrote xyz artifacts")
