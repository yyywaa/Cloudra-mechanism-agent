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
    pts.append(dict(n=k+1, oc=oc, hdr=b[0], m=m, E=e, scfline=ln))
# maxstep-exhausted scan points (not converged)
exh=[i+1 for i,ln in enumerate(L) if "Number of steps exceeded" in ln or "Optimization stopped." in ln]
print("=== scan2d_candidates_v3 : measured-coordinate table (no row/col inference) ===")
print("log lines: %d | converged grid points (Optimization completed): %d | maxstep-exhausted points: %d" % (len(L), len(pts), len(exh)))
print()
print("scan# | meas R(2,4)  meas R(25,26) | E (SCF line) | OPT line | R(4,26) R(10,27) R(2,25) R(2,26) | H26 nearest")
for p in pts:
    m=p["m"]
    print("%5d | %10.4f %12.4f | %.9f (L%d) | L%d | %.4f %.4f %.4f %.4f | %s%d %.4f" % (p["n"], m["r24"], m["r2526"], p["E"], p["scfline"], p["oc"], m["r426"], m["r1027"], m["r225"], m["r226"], Z[m["h26"][2]], m["h26"][1], m["h26"][0]))
print()
# order detection from measured coordinates
mode="undetermined"
if len(pts)>=2:
    kinds=[]
    for a,b in zip(pts[:-1],pts[1:]):
        dr24=abs(b["m"]["r24"]-a["m"]["r24"]); drp=abs(b["m"]["r2526"]-a["m"]["r2526"])
        kinds.append("row-advance" if dr24>0.05 else ("path-advance" if drp>0.02 else "no-change"))
    print("consecutive measured deltas: " + ", ".join("%d->%d:%s" % (a["n"],b["n"],k) for a,b,k in zip(pts[:-1],pts[1:],kinds)))
    if all(k=="path-advance" or k=="no-change" for k in kinds) and any(k=="path-advance" for k in kinds):
        mode="path-type (continuation: first dim stays at its end value)"
    elif any(k=="row-advance" for k in kinds):
        mode="row-major / serpentine (first dim resets or steps per column)"
print("detected traversal mode: %s" % mode)
print()
print("6x6 cells: each cell = scan# + MEASURED (R(2,4), R(25,26)); rows/cols are nominal design values only")
grid={}
for p in pts:
    i0=int(round((p["m"]["r24"]-rows_v[0])/0.2)); j0=int(round((p["m"]["r2526"]-cols_v[0])/0.25))
    p["i"],p["j"]=i0,j0; grid[(i0,j0)]=p
    if abs(p["m"]["r24"]-rows_v[i0])>0.02 or abs(p["m"]["r2526"]-cols_v[j0])>0.02:
        print("  WARNING scan#%d measured (%.4f,%.4f) deviates from nominal (%.4f,%.4f) by >0.02 A" % (p["n"],p["m"]["r24"],p["m"]["r2526"],rows_v[i0],cols_v[j0]))
for i_ in range(6):
    cells=[]
    for j_ in range(6):
        p=grid.get((i_,j_))
        cells.append(("#%d E=%.6f (%.4f,%.4f)" % (p["n"],p["E"],p["m"]["r24"],p["m"]["r2526"])) if p else "----")
    print("  nominal R(2,4)=%.4f | %s" % (rows_v[i_], " | ".join("%-34s"%x for x in cells)))
print()
print("=== candidate criteria ===")
if mode.startswith("path"):
    print("PATH-TYPE criterion: neighbours = previous and next CONVERGED point along the scan path.")
    print("  candidate requires: (a) local maximum along the path; (b) energy descending on BOTH sides; (c) BOTH sides converged.")
    print("  any side missing/unconverged => 'candidate pending confirmation', never enters ts_prepare.")
    print("  a maxstep-exhausted (unconverged) point is neither a candidate nor a usable neighbour (no false candidate between two unconverged points).")
    for i,p in enumerate(pts):
        prev=pts[i-1] if i>0 else None; nxt=pts[i+1] if i+1<len(pts) else None
        tag="scan#%d (%.4f,%.4f) E=%.9f :: " % (p["n"],p["m"]["r24"],p["m"]["r2526"],p["E"])
        if prev is None or nxt is None:
            print(tag + "candidate pending confirmation: path end (missing %s)" % ("previous" if prev is None else "next"))
            continue
        up_l = p["E"] > prev["E"]; up_r = p["E"] > nxt["E"]
        if up_l and up_r:
            print(tag + "CANDIDATE - path local maximum, both sides converged and descending (prev scan#%d, next scan#%d)" % (prev["n"],nxt["n"]))
        elif up_l or up_r:
            print(tag + "not a candidate (one-sided rise only)")
        else:
            print(tag + "not a candidate (path monotone here)")
else:
    print("GRID criterion (four-neighbour, serpentine): one axis local max AND the other axis local min; declare which axis carries the barrier.")
    for p in pts:
        i_,j_=p["i"],p["j"]; out=[]
        boundary=(i_ in (0,5)) or (j_ in (0,5))
        dep=[(i_-1,j_),(i_+1,j_),(i_,j_-1),(i_,j_+1)]; have=[grid.get(d) for d in dep]
        if any(h is None for h in have):
            out.append("neighbours missing or unconverged: " + ",".join("r%dc%d"%(d[0]+1,d[1]+1) for d,h in zip(dep,have) if h is None))
        else:
            cA_max = grid[(i_-1,j_)]["E"] < p["E"] and grid[(i_+1,j_)]["E"] < p["E"]
            cA_min = grid[(i_-1,j_)]["E"] > p["E"] and grid[(i_+1,j_)]["E"] > p["E"]
            cB_max = grid[(i_,j_-1)]["E"] < p["E"] and grid[(i_,j_+1)]["E"] < p["E"]
            cB_min = grid[(i_,j_-1)]["E"] > p["E"] and grid[(i_,j_+1)]["E"] > p["E"]
            out.append("R(2,4)axis:%s  R(25,26)axis:%s" % ("max" if cA_max else ("min" if cA_min else "neither"), "max" if cB_max else ("min" if cB_min else "neither")))
            if cA_max and cB_min: out.append("CANDIDATE - barrier carried by bond-breaking axis R(2,4)")
            elif cA_min and cB_max: out.append("CANDIDATE - barrier carried by proton axis R(25,26)")
            elif cA_max and cB_max: out.append("ridge vertex (both max) => NOT a candidate; branch: 1D relaxed R(2,4) scan at that proton value, or reset the proton column")
            elif cA_min and cB_min: out.append("basin grid point => energy registration only")
            else: out.append("not a candidate (no max/min pair across the two axes)")
        if boundary: out.append("boundary row/col => needs-wider-window, not a candidate")
        print("  scan#%d measured(%.4f,%.4f) E=%.9f :: %s" % (p["n"],p["m"]["r24"],p["m"]["r2526"],p["E"]," ; ".join(out)))
print()
print("if no point satisfies the criterion: 'this grid did not resolve a discrete stationary point of index 1, needs wider window or denser grid' -- never no-TS / no-channel.")
print()
cur=met(blocks[-1][1], blocks[-1][2])
print("in-progress point (no Optimization completed yet, excluded): last block L%d meas (%.4f, %.4f) R(4,26)=%.4f R(10,27)=%.4f H26 nearest %s%d %.4f" % (blocks[-1][0], cur["r24"], cur["r2526"], cur["r426"], cur["r1027"], Z[cur["h26"][2]], cur["h26"][1], cur["h26"][0]))
last_step=[ (i+1,L[i].strip()) for i in range(len(L)) if "on scan point" in L[i] and "Step number" in L[i] ]
print("last step line L%d: %s" % last_step[-1])
print("last SCF line L%d: %s" % scf[-1])
print()
print("disclaimer: constrained profile O10-H27 frozen; candidates are TS candidates / upper bounds only; never dE-dagger; E3b result and barrier stay null.")
print("  span wording (coordinator ruling 22:05/22:09/22:10): main caliber 1.6086 kcal/mol (frequency-verified product minima P=job 1061 -4.3383 vs 1073 -2.7297);")
print("  product-side reference uncertainty >=1.6 kcal/mol, not capped (1069 last frame -4.7458, 1071 instantaneous min -5.3443); proton path still undetermined;")
print("  instantaneous reading span ~2.6145 kcal/mol (contains unverified trajectory frames, varies with 1071, not an invariant).")
