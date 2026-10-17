import numpy as np, re, sys
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
rows_v=[1.4248+0.2*i for i in range(6)]
cols_v=[0.9693+0.25*j for j in range(6)]
blocks=[]; i=0
while i < len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1; co=[]; el=[]
        while k < len(L) and len(co)<41:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==41: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
opt=[i+1 for i,ln in enumerate(L) if "Optimization completed." in ln]
Z={1:"H",6:"C",7:"N",8:"O"}
def metrics(X,el):
    d=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
    heavy=[a for a in range(1,42) if el[a-1]!=1]
    nn=min(((d(26,a),a) for a in heavy))
    return dict(r24=d(2,4), r2526=d(25,26), r426=d(4,26), r1027=d(10,27), r225=d(2,25), r226=d(2,26), h26=(nn[0],nn[1],el[nn[1]-1]))
pts=[]
for oc in opt:
    cand=[b for b in blocks if b[0] < oc]
    if not cand: continue
    b=cand[-1]; m=metrics(b[1],b[2])
    e=float("nan"); ln=0
    for l,en in scf:
        if l < oc: e=en; ln=l
    i0=int(round((m["r24"]-rows_v[0])/0.2)); j0=int(round((m["r2526"]-cols_v[0])/0.25))
    pts.append(dict(oc=oc, blk=b[0], i=i0, j=j0, m=m, E=e, scfline=ln))
cur=metrics(blocks[-1][1], blocks[-1][2])
print("== converged grid points: %d (Optimization completed at %s) ==" % (len(pts), opt))
grid={}
for p in pts:
    grid[(p["i"],p["j"])]=p
    print("  row %d (R(2,4)=%.4f) col %d (R(25,26)=%.4f) | E=%.9f (SCF L%d) | R(4,26)=%.4f R(10,27)=%.4f R(2,25)=%.4f R(2,26)=%.4f | H26 nearest %s%d %.4f | OPT completed L%d" % (p["i"]+1, rows_v[p["i"]], p["j"]+1, cols_v[p["j"]], p["E"], p["scfline"], p["m"]["r426"], p["m"]["r1027"], p["m"]["r225"], p["m"]["r226"], Z[p["m"]["h26"][2]], p["m"]["h26"][1], p["m"]["h26"][0], p["oc"]))
print()
print("== 6x6 table (row = R(2,4), col = R(25,26)); * = Optimization completed ==")
for i_ in range(6):
    cells=[]
    for j_ in range(6):
        p=grid.get((i_,j_))
        cells.append(("%.6f*" % p["E"]) if p else "----")
    print("  R(2,4)=%.4f | %s" % (rows_v[i_], " ".join("%14s"%x for x in cells)))
print()
print("== grid-value consistency ==")
for p in pts:
    print("  point(oc L%d): |R(2,4)-%.4f|=%.5f |R(25,26)-%.4f|=%.5f" % (p["oc"], rows_v[p["i"]], abs(p["m"]["r24"]-rows_v[p["i"]]), cols_v[p["j"]], abs(p["m"]["r2526"]-cols_v[p["j"]])))
print()
print("== candidate criterion: (1) local max along R(2,4) within a proton column, (2) local min along R(25,26) within a row, (3) self+used neighbours all converged, (4) first/last row and column excluded ==")
if not pts: print("  no converged point yet")
for p in pts:
    i_,j_=p["i"],p["j"]; notes=[]
    if i_ in (0,5) or j_ in (0,5): notes.append("(4) boundary row%d/col%d => only record needs-wider-window" % (i_+1,j_+1))
    dep=[(i_-1,j_),(i_+1,j_),(i_,j_-1),(i_,j_+1)]; have=[grid.get(d) for d in dep]
    if any(h is None for h in have):
        notes.append("(3) missing neighbours: " + ",".join("(%d,%d)"%(d[0]+1,d[1]+1) for d,h in zip(dep,have) if h is None))
    else:
        c1 = grid[(i_-1,j_)]["E"] < p["E"] and grid[(i_+1,j_)]["E"] < p["E"]
        c2 = grid[(i_,j_-1)]["E"] > p["E"] and grid[(i_,j_+1)]["E"] > p["E"]
        notes.append("(1) along R(2,4): %s | (2) along R(25,26): %s" % ("local max" if c1 else "not max", "local min" if c2 else "not min"))
        if c1 and c2: notes.append("=> candidate (still only TS candidate / upper bound; no dE-double-dagger)")
        elif c1 and not c2: notes.append("=> NOT a candidate; branch per ruling: at that proton value run a 1D relaxed R(2,4) scan, or reset the proton column")
    print("  point row%d col%d E=%.9f :: %s" % (i_+1,j_+1,p["E"]," ; ".join(notes)))
print()
print("== in-progress grid point (not converged, not tabulated) ==")
print("  last block L%d: R(2,4)=%.4f R(25,26)=%.4f R(10,27)=%.4f H26 nearest %s%d %.4f" % (blocks[-1][0], cur["r24"], cur["r2526"], cur["r1027"], Z[cur["h26"][2]], cur["h26"][1], cur["h26"][0]))
print()
print("== disclaimer: constrained profile (O10-H27 frozen); peak = TS candidate/upper bound only; no dE-double-dagger; E3b barrier stays null; any single-value barrier must be quoted together with product-side stationary-point span 2.0160 kcal/mol (1028 reference) and P = job 1061 ==")
