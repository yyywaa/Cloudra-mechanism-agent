#!/usr/bin/env python3
"""Read-only E2 continuation (cont1) table builder - same conventions as the main-scan v2 judge.
Conventions: converged frame = last Standard orientation block before each 'Optimization completed.';
energy = last SCF Done of that block (assert hdr < scf, no new geometry in between);
Kabsch over the 20 heavy atoms, SVD, C = Q^T P, Qp = Q R^T, rmsd = sqrt(sum d^2 / N), det(R)=+1 enforced;
tiers: 0 = R(28,24) > 1.50 ; 1 = [1.20,1.50] ; 2 = R(28,24)<=1.10 and R(11,24)>=1.50 ;
dE always vs MAIN-scan first point -939.308205969 Eh.
"""
import hashlib, math, sys, datetime
import numpy as np

CONT1 = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan_cont1.log"
MAIN  = "/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E2/scan_1d/build/E2_1D_scan.log"
SEED  = "/home/ly/Cloudra-mechanism-agent/ts/ts_0009/build/input_0004/reactant/seed.xyz"
E0    = -939.308205969          # main-scan point 1 (reference for dE)
HARTREE = 627.5094740631

def read(p):
    b = open(p, "rb").read()
    return b.decode("utf-8", "replace").splitlines(), hashlib.sha256(b).hexdigest(), len(b)

def blocks(L):
    out=[]; i=0; n=len(L)
    while i < n:
        if L[i].strip().startswith("Standard orientation:"):
            j=i+1; d=0
            while j<n and d<2:
                if L[j].strip().startswith("-----"): d+=1
                j+=1
            co={}; k=j; cnt=0
            while k<n and not L[k].strip().startswith("-----"):
                p=L[k].split()
                if len(p)==6:
                    co[int(p[0])]=(int(p[1]), float(p[3]), float(p[4]), float(p[5])); cnt+=1
                k+=1
            assert cnt==41, f"block at L{i+1} has {cnt} atoms, expected 41"
            out.append((i+1, k+1, co)); i=k
        else: i+=1
    return out

def conv_frames(L, bl, tag):
    oc=[i+1 for i,l in enumerate(L) if "Optimization completed" in l]
    fr=[]
    for d in oc:
        cand=[b for b in bl if b[1] < d]
        assert cand, f"{tag}: no geometry block before Optimization completed at L{d}"
        hdr, end, co = cand[-1]
        scf=[(i+1, l) for i,l in enumerate(L) if "SCF Done" in l and hdr < i+1 < d]
        assert scf, f"{tag}: no SCF Done between L{hdr} and L{d}"
        assert hdr < scf[-1][0]
        e=float(scf[-1][1].split("=")[1].split("A.U.")[0])
        fr.append(dict(oc=d, hdr=hdr, scf=scf[-1][0], E=e, co=co))
    return fr

def elements_order_ok(co):
    S=[l.split() for l in open(SEED).read().splitlines()[2:] if len(l.split())==4]
    return [int(s[0].replace('H','1')) if s[0].isdigit() else s[0] for s in S], len(S), \
           [co[i][0] for i in sorted(co)]

def kab(A, B, idx):
    P=np.array([A[i][1:] for i in idx]); Q=np.array([B[i][1:] for i in idx])
    P=P-P.mean(0); Q=Q-Q.mean(0)
    C=Q.T@P
    U,S,Vt=np.linalg.svd(C)
    d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T
    Qp=Q@R.T
    dist=np.linalg.norm(P-Qp, axis=1)
    return float(np.sqrt((dist**2).mean())), float(dist.max()), float(d)

def dist(co,a,b): return math.dist(co[a][1:], co[b][1:])

def tier(r2824, r1124):
    if r2824 > 1.50: return 0
    if r2824 <= 1.10 and r1124 >= 1.50: return 2
    if 1.20 <= r2824 <= 1.50: return 1
    return "uncertain"

def main():
    Lc, shac, bc = read(CONT1)
    Lm, sham, bm = read(MAIN)
    print(f"# snapshot {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}")
    print(f"# cont1 log: {CONT1}\n#   lines={len(Lc)} bytes={bc} sha256={shac}")
    print(f"# main  log: {MAIN}\n#   lines={len(Lm)} bytes={bm} sha256={sham}")
    blc = blocks(Lc); fc = conv_frames(Lc, blc, "cont1")
    blm = blocks(Lm); fm = conv_frames(Lm, blm, "main")
    print(f"# cont1 converged frames: {len(fc)}  (oc lines {[f['oc'] for f in fc]})")
    m_pt8 = fm[7]     # main-scan point 8 (index 7)
    assert abs(m_pt8["E"] - (-939.297687588)) < 1e-9, "main pt8 energy mismatch"
    print(f"# main pt8: hdr L{m_pt8['hdr']} scf L{m_pt8['scf']} E={m_pt8['E']:.9f}")
    heavy=[i for i in sorted(m_pt8["co"]) if m_pt8["co"][i][0]!=1]
    print(f"# heavy atoms: {len(heavy)}")
    print("# pt | R(1,29) | E(Eh) | SCF L | hdr L | dE vs main-pt1 (kcal/mol) | Kabsch vs prev cont1 rmsd/max/det | Kabsch vs MAIN pt8 rmsd/max | R(28,24) | R(11,24) | tier")
    prev=None
    for n,f in enumerate(fc, start=1):
        r129 = dist(f["co"],1,29); r2824 = dist(f["co"],28,24); r1124=dist(f["co"],11,24)
        dE = (f["E"]-E0)*HARTREE
        if prev is None:
            k_prev = "—"
        else:
            r,m,d = kab(prev["co"], f["co"], heavy); k_prev=f"{r:.4f}/{m:.4f}/det={d:+.0f}"
        r8,m8,_ = kab(m_pt8["co"], f["co"], heavy)
        print(f"{n} | {r129:.4f} | {f['E']:.9f} | L{f['scf']} | L{f['hdr']} | {dE:+.2f} | {k_prev} | {r8:.4f}/{m8:.4f} | {r2824:.4f} | {r1124:.4f} | {tier(r2824,r1124)}")
        prev=f
    # un-converged marker
    marks=[(i+1,l.strip()) for i,l in enumerate(Lc) if "on scan point" in l and "Step number" in l]
    if marks:
        print(f"# last step line: L{marks[-1][0]}: {marks[-1][1]}")
    oc=[i+1 for i,l in enumerate(Lc) if "Optimization completed" in l]
    last_mark=[(i+1,l.strip()) for i,l in enumerate(Lc) if "on scan point" in l and "Step number" in l][-1]
    print(f"# converged markers: {oc}")
    print(f"# terminations: {[ (i+1,l.strip()) for i,l in enumerate(Lc) if 'Normal termination' in l or 'Error termination' in l ]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
