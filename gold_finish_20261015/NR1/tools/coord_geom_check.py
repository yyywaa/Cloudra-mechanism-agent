
import sys, re, math
import numpy as np

def parse(path):
    txt = open(path, errors="replace").read().splitlines()
    coord=None; energies=[]; imag=None; imline=None; nterm=None; imagval=None
    i=0
    while i < len(txt):
        L = txt[i]
        if "SCF Done:" in L:
            m = re.search(r"=\s*(-?\d+\.\d+)", L)
            if m: energies.append((i+1, float(m.group(1))))
        if "Standard orientation:" in L or "Input orientation:" in L:
            j = i+5; at=[]
            while j < len(txt) and "---" not in txt[j]:
                parts = txt[j].split()
                if len(parts) >= 6:
                    at.append((int(parts[0]), int(parts[1]), float(parts[3]), float(parts[4]), float(parts[5])))
                j += 1
            coord = at
        if "imaginary frequencies" in L and imag is None:
            m = re.search(r"(\d+) imaginary", L)
            if m: imag = int(m.group(1)); imline = i+1
        if "Normal termination" in L: nterm = i+1
        i += 1
    for k,L in enumerate(txt):
        m = re.match(r"\s*Frequencies\s*--\s*(-?\d+\.\d+)", L)
        if m and float(m.group(1)) < 0:
            imagval = (k+1, float(m.group(1))); break
    return dict(txt=txt, coord=coord, energies=energies, imag=imag, imline=imline, imagval=imagval, nterm=nterm)

Z={1:"H",6:"C",8:"O"}
def lab(a): return Z.get(a,str(a))
def kabsch_rmsd(A,B):
    A=A-A.mean(0); B=B-B.mean(0)
    V,S,W=np.linalg.svd(A.T@B)
    d=np.sign(np.linalg.det(V@W))
    D=np.diag([1,1,d])
    R=V@D@W
    Ar=A@R
    dv=np.linalg.norm(Ar-B,axis=1)
    return math.sqrt((dv**2).mean()), dv.max(), dv
# CLI: script.py ref.log mapping.json target1 target2 ...   (mapping optional)
args=sys.argv[1:]
ref=parse(args[0]); args=args[1:]
mp=None
if args and args[0].endswith(".json"):
    import json
    mp=json.load(open(args[0])); args=args[1:]
H2K=627.5094740631
def coords_of(p, order=None):
    d=parse(p); c=d["coord"]
    if order is None: return d,c
    idx={a[0]:a for a in c}
    return d,[idx[k] for k in order]
for p in args:
    d,c=coords_of(p)
    print("==",p)
    print("  lastE=%s@%s nSCF=%d nterm=%s imag=%s@%s first_neg=%s"%(d["energies"][-1][1], d["energies"][-1][0], len(d["energies"]), d["nterm"], d["imag"], d["imline"], d["imagval"]))
    print("  elems:","".join(lab(a[1]) for a in c))
    A=np.array([a[2:] for a in c]); B=np.array([a[2:] for a in ref["coord"]])
    rms,mx,dv=kabsch_rmsd(A,B)
    order=np.argsort(-dv)[:8]
    print("  ALIGNED-vs-%s rms=%.3f max=%.3f big8=%s"%(args[0] if False else p and "", rms, mx, " ".join("%s%d:%.2f"%(lab(c[i][1]),c[i][0],dv[i]) for i in order)))
    e1=d["energies"][-1][1]; e2=ref["energies"][-1][1]
    print("  dE_vs_ref_kcal=%.2f"%((e1-e2)*H2K))
