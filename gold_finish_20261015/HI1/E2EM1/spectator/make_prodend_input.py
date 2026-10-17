import sys, hashlib, math
IN=sys.argv[1]; OUT=sys.argv[2]
SMILES="CC(C[C@@H]([O-])c1ccccc1)=[N+]1CCC[C@H]1C(=O)O.O"
L=open(IN).read().splitlines()
n=int(L[0].split()[0]); rows=[l.split() for l in L[2:2+n]]
if n!=41: raise SystemExit("expected 41 atoms, got %d"%n)
el=[r[0] for r in rows]
EXP="C C C N C C C C C O O H H H H H H H H H H H H H O H H O C C C C C C C H H H H H H".split()
if el!=EXP: raise SystemExit("element order differs from TS/EM1 order: %s"%(" ".join(el)))
coords=[" ".join(r[:4]) for r in rows]
c=[[float(v) for v in r[1:4]] for r in rows]
head=("%chk="+OUT.replace(".gjf",".chk")+"
%nproc=8
%mem=10240MB
"
"#p opt freq B3LYP/def2SVP EmpiricalDispersion=GD3BJ Int(UltraFine) SCF=Tight SCRF=(CPCM,Solvent=DMSO)

"
"smiles: "+SMILES+" | HI1_EM1 product endpoint (M1) Opt+Freq, seed: "+IN.split("/")[-1]+"

0 1
")
open(OUT,"w").write(head+"
".join(coords)+"

")
print("wrote",OUT,"sha256",hashlib.sha256(open(OUT,"rb").read()).hexdigest())
print("d(1,29) of seed = %.3f"%math.dist(c[0],c[28]))
