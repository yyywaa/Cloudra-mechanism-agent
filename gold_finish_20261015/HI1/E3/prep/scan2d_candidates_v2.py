import numpy as np, re
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
def met(X,el):
    d=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
    heavy=[a for a in range(1,42) if el[a-1]!=1]
    nn=min(((d(26,a),a) for a in heavy))
    return dict(r24=d(2,4), r2526=d(25,26), r426=d(4,26), r1027=d(10,27), r225=d(2,25), r226=d(2,26), h26=(nn[0],nn[1],el[nn[1]-1]))
pts=[]
for k,oc in enumerate(opt):
    cand=[b for b in blocks if b[0] < oc]
    if not cand: continue
    b=cand[-1]; m=met(b[1],b[2]); e=float("nan"); ln=0
    for l,en in scf:
        if l < oc: e=en; ln=l
    i0=int(round((m["r24"]-rows_v[0])/0.2)); j0=int(round((m["r2526"]-cols_v[0])/0.25))
    pts.append(dict(n=k+1, oc=oc, i=i0, j=j0, m=m, E=e, scfline=ln))
cur=met(blocks[-1][1], blocks[-1][2])
print("scan# | row R(2,4)  col R(25,26) | E (SCF line) | OPT line | R(4,26) R(10,27) R(2,25) R(2,26) | H26 nearest")
grid={}
for p in pts:
    grid[(p["i"],p["j"])]=p
    print("%5d | %8.4f %8.4f | %.9f (L%d) | L%d | %.4f %.4f %.4f %.4f | %s%d %.4f" % (p["n"], rows_v[p["i"]], cols_v[p["j"]], p["E"], p["scfline"], p["oc"], p["m"]["r426"], p["m"]["r1027"], p["m"]["r225"], p["m"]["r226"], Z[p["m"]["h26"][2]], p["m"]["h26"][1], p["m"]["h26"][0]))
print()
print("scan-order note: coordinate 1 R(2,4) varies first, so the first 6 grid points cover only the bond-breaking dimension;")
print("                  the proton dimension R(25,26) starts expanding from grid point 7.")
print()
print("6x6 table (rows = R(2,4), cols = R(25,26)); cell = E and scan#:")
for i_ in range(6):
    cells=[]
    for j_ in range(6):
        p=grid.get((i_,j_))
        cells.append(("%.6f #%d" % (p["E"],p["n"])) if p else "----")
    print("  R(2,4)=%.4f | %s" % (rows_v[i_], " | ".join("%16s"%x for x in cells)))
print()
print("candidate criterion (approved symmetric version): one axis local max AND the other axis local min; declare which axis carries the barrier.")
for p in pts:
    i_,j_=p["i"],p["j"]; out=[]
    boundary = (i_ in (0,5)) or (j_ in (0,5))
    dep=[(i_-1,j_),(i_+1,j_),(i_,j_-1),(i_,j_+1)]; have=[grid.get(d) for d in dep]
    if any(h is None for h in have):
        out.append("neighbours missing or unconverged: " + ",".join("r%dc%d"%(d[0]+1,d[1]+1) for d,h in zip(dep,have) if h is None))
    else:
        cA_max = grid[(i_-1,j_)]["E"] < p["E"] and grid[(i_+1,j_)]["E"] < p["E"]
        cA_min = grid[(i_-1,j_)]["E"] > p["E"] and grid[(i_+1,j_)]["E"] > p["E"]
        cB_max = grid[(i_,j_-1)]["E"] < p["E"] and grid[(i_,j_+1)]["E"] > p["E"]
        cB_max = grid[(i_,j_-1)]["E"] < p["E"] and grid[(i_,j_+1)]["E"] < p["E"]
        cB_min = grid[(i_,j_-1)]["E"] > p["E"] and grid[(i_,j_+1)]["E"] > p["E"]
        tag="R(2,4)axis:%s  R(25,26)axis:%s" % ("max" if cA_max else ("min" if cA_min else "neither"), "max" if cB_max else ("min" if cB_min else "neither"))
        out.append(tag)
        if cA_max and cB_min: out.append("CANDIDATE - barrier carried by bond-breaking axis R(2,4)")
        elif cA_min and cB_max: out.append("CANDIDATE - barrier carried by proton axis R(25,26)")
        elif cA_max and cB_max: out.append("ridge vertex (both max) => NOT a candidate; branch: at that proton value run a 1D relaxed R(2,4) scan, or reset the proton column")
        elif cA_min and cB_min: out.append("basin grid point => energy registration only")
        else: out.append("not a candidate (no max/min pair across the two axes)")
    if boundary: out.append("boundary row/col => record needs-wider-window, not a candidate")
    print("  scan#%d row%d col%d E=%.9f :: %s" % (p["n"],i_+1,j_+1,p["E"]," ; ".join(out)))
print()
print("if no grid point satisfies the criterion, write: this 6x6 grid did not resolve a discrete stationary point of index 1, needs wider window or denser grid -- never no-TS / no-channel.")
print()
print("in-progress grid point (not converged, excluded from table):")
print("  last block L%d: R(2,4)=%.4f R(25,26)=%.4f R(10,27)=%.4f H26 nearest %s%d %.4f" % (blocks[-1][0], cur["r24"], cur["r2526"], cur["r1027"], Z[cur["h26"][2]], cur["h26"][1], cur["h26"][0]))
print()
print("disclaimer: constrained profile O10-H27 frozen; candidates are TS candidates / upper bounds only; no dE-double-dagger; E3b result and barrier stay null;")
print("            any single-value barrier must be quoted with product-side stationary-point span 2.0160 kcal/mol (1028 reference; P -4.3383 / 1073 -2.7297 / 1069 -4.7458) and P = job 1061.")