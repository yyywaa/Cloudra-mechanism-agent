
import numpy as np, json, itertools
base="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HL1/ts_run/prep"
src=f"{base}/csearch_RC2/guided_assembly/assembly/complex_candidate_000.xyz"
lines=open(src).read().split("\n"); n=int(lines[0])
rows=[l.split() for l in lines[2:2+n]]
sym=[r[0] for r in rows]; X=np.array([[float(x) for x in r[1:4]] for r in rows])

# hydronium internal geometry (atoms 1..4) taken from the tool-built component; oxime (5..19) kept as built
O1, H2, H3, H4 = X[0], X[1], X[2], X[3]
N6, O7, H16 = X[7], X[8], X[15]

def unit(v):
    return v/np.linalg.norm(v)

# rotation mapping current hydronium frame -> target frame
a1 = unit(H2-O1)
tmp = H3-O1
a2 = unit(tmp - a1*np.dot(tmp,a1))
a3 = np.cross(a1,a2)
A = np.column_stack([a1,a2,a3])

uN = unit(N6-O7); uH = unit(H16-O7)
w  = -unit(uN+uH)                       # O7 -> O1: in-plane lone-pair (anti) direction
b1 = -w                                 # O1 -> H2 (points at O7)
ref = N6-O7
b2 = ref - b1*np.dot(ref,b1); b2 = unit(b2)
b3 = np.cross(b1,b2)
B = np.column_stack([b1,b2,b3])
R = B @ A.T
d_OO = 2.60
best=None
for az in range(0,360,10):
    th=np.radians(az)
    c,s=np.cos(th),np.sin(th)
    Rz = np.array([[c,-s,0],[s,c,0],[0,0,1]])
    Rt = B @ Rz @ B.T @ R
    hyd_rot = (Rt @ (X[:4]-O1).T).T
    newO1 = O7 + d_OO*w
    hyd = hyd_rot + newO1
    # clash check against oxime heavy atoms + H16
    heavy = X[4:]
    dmin = min(np.linalg.norm(h-e) for h in hyd for e in heavy)
    if best is None or dmin>best[0]: best=(dmin, az, Rt)
    
dmin, az, Rt = best
hyd = (Rt @ (X[:4]-O1).T).T + (O7 + d_OO*w)
Y = X.copy(); Y[:4]=hyd
print("best azimuth", az, "min hydronium..oxime-atom distance", round(dmin,3))
def d(i,j): return float(np.linalg.norm(Y[i-1]-Y[j-1]))
print("after placement: O1-O7", round(d(1,9),3), "H2-O7", round(d(2,9),3), "H2-N6", round(d(2,8),3),
      "O1-N6", round(d(1,8),3), "H3-O7", round(d(3,9),3), "H4-O7", round(d(4,9),3))
print("angle O1-H2...O7 (deg)", round(float(np.degrees(np.arccos(np.dot(unit(O7-Y[1]),unit(Y[1]-Y[0]))))),1) if False else "")

def write_xyz(path, comment, coords, symbols):
    with open(path,"w") as f:
        f.write(f"{len(symbols)}\n{comment}\n")
        for s,c in zip(symbols,coords):
            f.write(f"{s:2s} {c[0]:14.8f} {c[1]:14.8f} {c[2]:14.8f}\n")

write_xyz(f"{base}/RC_seedB.xyz",
  "smiles: [OH3+].CC/C(=N/O)/C ; HL1_E1 RC ion-dipole complex, O-specific pose: H3O+ H2 points at oxime O7 along the in-plane lone-pair direction (anti to N6); d(O1-O7)=2.60 A",
  Y, sym)
# product seed B: H2 moved to O7 (0.98 A), water left in place -> same atom order
Z = Y.copy()
Z[1] = Y[8] + 0.98*unit(Y[1]-Y[8])
write_xyz(f"{base}/PC_seedB.xyz",
  "smiles: O.CC/C(C)=N/[OH2+] ; HL1_E1 product complex (H2O + O-protonated (E)-butanone oxime); same atom order as RC_seedB, H2 moved onto O7",
  Z, sym)
print("PC_seedB: d(H2-O7)=", round(float(np.linalg.norm(Z[1]-Z[8])),3), " d(O1-H2)=", round(float(np.linalg.norm(Z[0]-Z[1])),3), " d(O1-O7)=", round(float(np.linalg.norm(Z[0]-Z[8])),3))
json.dump({"d_OO":d_OO,"azimuth_deg":az,"order":"1=O1 2=H2 3=H9 4=H10 5=C11 6=C5 7=C4 8=N6 9=O7 10=C3 11-13=H(C11) 14-15=H(C5) 16=H8 17-19=H(C3)"},
          open(f"{base}/seed_constructionB.json","w"), indent=1)
