import sys, re
path = sys.argv[1] if len(sys.argv)>1 else "gold_finish_20261015/HI1/E3/runs/build_seed_product_optfreq.log"
L=open(path).read().splitlines()
freq=[]; redm=[]; frc=[]; imaghdr=[]
for i,ln in enumerate(L):
    if ln.strip().startswith("Frequencies --"):
        vals=[float(x) for x in re.findall(r'-?\d+\.\d+', ln.split("--",1)[1])]
        freq += vals
    if ln.strip().startswith("Red. masses --"):
        redm += [float(x) for x in re.findall(r'-?\d+\.\d+', ln.split("--",1)[1])]
    if ln.strip().startswith("Frc consts  --"):
        frc += [float(x) for x in re.findall(r'-?\d+\.\d+', ln.split("--",1)[1])]
    if "imaginary" in ln:
        imaghdr.append((i+1, ln.strip()))
groups=sum(1 for ln in L if ln.strip().startswith("Frequencies --"))
nterm=[(i+1,ln.strip()) for i,ln in enumerate(L) if "Normal termination" in ln]
optdone=[(i+1,ln.strip()) for i,ln in enumerate(L) if "Optimization completed." in ln]
print("log:", path)
print("lines:", len(L))
for x in nterm: print("Normal termination:", x)
for x in optdone: print("Optimization completed:", x)
print("Frequencies -- groups:", groups, "| modes parsed:", len(freq), "| 3N-6 for N=41 =", 3*41-6, "| equal:", len(freq)==3*41-6)
neg=[(k+1,v) for k,v in enumerate(freq) if v<0]
print("negative values in band table:", len(neg), neg[:10])
print("imaginary header lines:", len(imaghdr), imaghdr[:5])
if neg:
    for k,v in neg[:5]:
        print("  imag mode idx %d: nu=%.4f cm-1  red.mass=%.6f amu  frc.const=%.6f mDyne/A" % (k, v, redm[k-1] if k-1<len(redm) else float('nan'), frc[k-1] if k-1<len(frc) else float('nan')))
real=[v for v in freq if v>0]
if real:
    print("lowest real mode: %.4f cm-1 | <20 cm-1:", real[0]<20, "| first 6 real:", ["%.4f"%x for x in real[:6]])
zpe=[ln.strip() for ln in L if "Zero-point correction" in ln]
print("ZPE lines:", zpe[-3:])
scf=[(i+1,ln.strip()) for i,ln in enumerate(L) if "SCF Done" in ln]
print("last SCF:", scf[-1] if scf else None)
