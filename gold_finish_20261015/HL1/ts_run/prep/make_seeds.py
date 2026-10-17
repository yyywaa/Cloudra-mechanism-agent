
import numpy as np, json
base="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/prep"
src=f"{base}/csearch_RC2/guided_assembly/assembly/complex_candidate_000.xyz"
lines=open(src).read().split("\n"); n=int(lines[0])
rows=[l.split() for l in lines[2:2+n]]
sym=[r[0] for r in rows]; xyz=np.array([[float(x) for x in r[1:4]] for r in rows])
def d(i,j): return float(np.linalg.norm(xyz[i-1]-xyz[j-1]))
print("n=",n,"symbols:"," ".join(f"{i+1}{s}" for i,s in enumerate(sym)))
for h in (2,3,4):
    print(f"H{h}: d(O1)={d(1,h):.3f} d(O7)={d(h,9):.3f} d(N6)={d(h,8):.3f} d(C4)={d(h,7):.3f}")
print("O1-O7", round(d(1,9),3), "O1-N6", round(d(1,8),3), "O7-H16", round(d(9,16),3), "N6-O7", round(d(8,9),3))
donor=min((2,3,4), key=lambda h: d(h,9))
print("donor (closest H to oxime O7) =", donor, "d=", round(d(donor,9),3))
# --- RC seed file: verbatim geometry, annotated comment
def write_xyz(path, comment, coords, symbols):
    with open(path,"w") as f:
        f.write(f"{len(symbols)}\n{comment}\n")
        for s,c in zip(symbols,coords):
            f.write(f"{s:2s} {c[0]:14.8f} {c[1]:14.8f} {c[2]:14.8f}\n")
write_xyz(f"{base}/RC_seed.xyz",
  "smiles: [OH3+].CC/C(=N/O)/C ; HL1_E1 RC pre-reaction ion-dipole complex (H3O+ H-bonded to oxime O7); source=conformer_search guided assembly candidate_000",
  xyz, sym)
# --- PC seed: move donor H onto O7 (0.98 A along O7->H direction); order unchanged (identity atom map)
xyzp = xyz.copy()
u = xyz[donor-1]-xyz[8]           # O7 -> Hdonor direction
u = u/np.linalg.norm(u)
xyzp[donor-1] = xyz[8] + 0.98*u
write_xyz(f"{base}/PC_seed.xyz",
  "smiles: O.CC/C(C)=N/[OH2+] ; HL1_E1 product complex (H2O + O-protonated (E)-butanone oxime); constructed from RC_seed by moving donor H onto O7, same atom order",
  xyzp, sym)
print("PC: new d(donor,O7)=", round(float(np.linalg.norm(xyzp[donor-1]-xyzp[8])),3),
      " d(O1,donor)=", round(float(np.linalg.norm(xyzp[0]-xyzp[donor-1])),3),
      " d(O1,O7)=", round(float(np.linalg.norm(xyzp[0]-xyzp[8])),3))
print("atom-order note: 1=O(O1) 2,3,4=H(H3O+) 5=C11 6=C5 7=C4 8=N6 9=O7 10=C3 11-13=H(C11) 14-15=H(C5) 16=H(O7) 17-19=H(C3)")
json.dump({"donor_h_index_1based": donor, "src": src}, open(f"{base}/seed_construction.json","w"), indent=1)
