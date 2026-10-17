import numpy as np, re
# scan2d_candidates_v4 : serpentine (four-neighbour) ONLY. Path-type branch removed per coordinator 22:35.
# Candidate pool = converged blocks only ("Optimization completed" incl. the 'on the basis of negligible forces' variant).
LOG="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/runs/e3b_scan2d_c2n4_o25h26.log"
L=open(LOG).read().splitlines()
N=41
rows_v=[1.4248+0.2*i for i in range(6)]
cols_v=[0.9693+0.25*j for j in range(6)]
blocks=[];i=0
while i<len(L):
    if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
        k=i+1;co=[];el=[]
        while k<len(L) and len(co)<N:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                el.append(int(p[1]));co.append([float(p[3]),float(p[4]),float(p[5])])
            k+=1
        if len(co)==N: blocks.append((i+1,np.array(co),el))
        i=k
    else: i+=1
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
opt=[i+1 for i,ln in enumerate(L) if "Optimization completed" in ln]
exh=[(i+1,L[i].strip()) for i,ln in enumerate(L) if "Number of steps exceeded" in ln or "Optimization stopped." in ln]
Z={1:"H",6:"C",7:"N",8:"O"}
def kabsch(A,B):
    Ac=A-A.mean(0); Bc=B-B.mean(0)
    U,S,Vt=np.linalg.svd(Ac.T@Bc); d=np.sign(np.linalg.det(Vt.T@U.T))
    R=Vt.T@np.diag([1,1,d])@U.T
    dev=np.linalg.norm((R@Ac.T).T-Bc,axis=1)
    return float(np.sqrt((dev**2).mean())), float(dev.max()), float(np.linalg.det(R))
def met(X,el):
    dd=lambda a,b: float(np.linalg.norm(X[a-1]-X[b-1]))
    heavy=[a for a in range(1,N+1) if el[a-1]!=1]
    nn=min(((dd(26,a),a) for a in heavy))
    return dict(r24=dd(2,4), rp=dd(25,26), r426=dd(4,26), r1027=dd(10,27), r225=dd(2,25), r226=dd(2,26), h26=(nn[0],nn[1],el[nn[1]-1]))
pts=[]
for oc in opt:
    b=[x for x in blocks if x[0]<oc][-1]; m=met(b[1],b[2]); e=[(l,en) for l,en in scf if l<oc][-1]
    pts.append(dict(n=len(pts)+1, oc=oc, hdr=b[0], X=b[1], el=b[2], m=m, E=e[1], Eln=e[0]))
print("=== scan2d_candidates_v4 (serpentine / four-neighbour only; path-type branch removed) ===")
print("log lines %d | converged grid points %d | maxstep-exhausted points %d" % (len(L), len(pts), len(exh)))
print()
print("scan# | meas R(2,4)  meas R(25,26) | E (SCF line) | OPT line | R(4,26) R(10,27) R(2,25) R(2,26) | H26 nearest")
for p in pts:
    m=p["m"]
    print("%5d | %10.4f %12.4f | %.9f (L%d) | L%d | %.4f %.4f %.4f %.4f | %s%d %.4f" % (p["n"],m["r24"],m["rp"],p["E"],p["Eln"],p["oc"],m["r426"],m["r1027"],m["r225"],m["r226"],Z[m["h26"][2]],m["h26"][1],m["h26"][0]))
print()
grid={}
warn=False
for p in pts:
    i0=int(round((p["m"]["r24"]-rows_v[0])/0.2)); j0=int(round((p["m"]["rp"]-cols_v[0])/0.25))
    p["i"],p["j"]=i0,j0; grid[(i0,j0)]=p
    if abs(p["m"]["r24"]-rows_v[i0])>0.02 or abs(p["m"]["rp"]-cols_v[j0])>0.02:
        warn=True; print("  WARNING scan#%d measured (%.4f,%.4f) deviates >0.02 A from nominal (%.4f,%.4f)" % (p["n"],p["m"]["r24"],p["m"]["rp"],rows_v[i0],cols_v[j0]))
if not warn: print("  (no measured-vs-nominal deviation >0.02 A: every cell below is anchored on measured coordinates)")
print()
print("=== per-column measured R(2,4) sequences (serpentine: direction alternates between columns) ===")
cols={}
for p in pts: cols.setdefault(round(p["m"]["rp"],2),[]).append(p)
for k in sorted(cols):
    seq=cols[k]
    line="  column R(25,26)=%.2f : " % k + " -> ".join("#%d %.4f" % (p["n"],p["m"]["r24"]) for p in seq)
    if len(seq)>=2:
        d=[b["m"]["r24"]-a["m"]["r24"] for a,b in zip(seq[:-1],seq[1:])]
        line += "   [direction: %s]" % ("increasing" if all(x>0.05 for x in d) else ("decreasing" if all(x<-0.05 for x in d) else "mixed"))
    print(line)
print("  mode: SERPENTINE (four-neighbour grid criterion, R137). path-type branch forbidden by coordinator ruling 22:35.")
print()
print("=== 6x6 table : cell = scan# + MEASURED (R(2,4), R(25,26)) + E; empty = not converged ===")
for i_ in range(6):
    cells=[]
    for j_ in range(6):
        p=grid.get((i_,j_))
        cells.append(("#%d %.6f (%.4f,%.4f)" % (p["n"],p["E"],p["m"]["r24"],p["m"]["rp"])) if p else "----")
    print("  nominal R(2,4)=%.4f | %s" % (rows_v[i_], " | ".join("%-32s"%x for x in cells)))
print()
print("=== candidate criterion (serpentine, four-neighbour) ===")
print("  one axis local maximum AND the other axis local minimum; declare which axis carries the barrier;")
print("  boundary row/column -> needs-wider-window (never a candidate); all four neighbours must be converged.")
found=0
for p in pts:
    i_,j_=p["i"],p["j"]; out=[]
    boundary=(i_ in (0,5)) or (j_ in (0,5))
    dep=[(i_-1,j_),(i_+1,j_),(i_,j_-1),(i_,j_+1)]; have=[grid.get(d) for d in dep]
    if boundary:
        out.append("boundary row/col => needs-wider-window, not a candidate")
    if any(h is None for h in have):
        out.append("neighbours missing or unconverged: " + ",".join("r%dc%d"%(d[0]+1,d[1]+1) for d,h in zip(dep,have) if h is None))
    else:
        cA_max=grid[(i_-1,j_)]["E"]<p["E"] and grid[(i_+1,j_)]["E"]<p["E"]
        cA_min=grid[(i_-1,j_)]["E"]>p["E"] and grid[(i_+1,j_)]["E"]>p["E"]
        cB_max=grid[(i_,j_-1)]["E"]<p["E"] and grid[(i_,j_+1)]["E"]<p["E"]
        cB_min=grid[(i_,j_-1)]["E"]>p["E"] and grid[(i_,j_+1)]["E"]>p["E"]
        out.append("R(2,4)axis:%s R(25,26)axis:%s" % ("max" if cA_max else ("min" if cA_min else "neither"), "max" if cB_max else ("min" if cB_min else "neither")))
        if cA_max and cB_min: out.append("CANDIDATE - barrier carried by bond-breaking axis R(2,4)"); found+=1
        elif cA_min and cB_max: out.append("CANDIDATE - barrier carried by proton axis R(25,26)"); found+=1
        elif cA_max and cB_max: out.append("ridge vertex (both max) => NOT a candidate; branch: 1D relaxed R(2,4) scan at that proton value, or reset the proton column")
        elif cA_min and cB_min: out.append("basin grid point => energy registration only")
        else: out.append("not a candidate (no max/min pair across the two axes)")
    print("  scan#%d meas(%.4f,%.4f) E=%.9f :: %s" % (p["n"],p["m"]["r24"],p["m"]["rp"],p["E"]," ; ".join(out)))
print()
print("  candidates found in this grid state: %d" % found)
if found==0:
    print("  if this holds once all 36 cells are converged, write: 'this 6x6 grid did not resolve a discrete stationary point of index 1, needs wider window or denser grid' -- never 'no TS' / 'no channel'.")
print()
print("=== adjacent-point Kabsch (fit=20 heavy, eval=20 heavy; SVD, det=+1, mirror forbidden) ===")
heavy=[i for i in range(N) if pts[0]["el"][i]!=1]
print("  synthesis self-checks first:")
rng=np.random.default_rng(11); X0=pts[0]["X"]
th=0.6; Rz=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]])
t=np.array([0.9,-1.4,2.6])
print("   (1) rigid rotation+translation : rms %.3e max %.3e det %+.1f" % kabsch(X0,(X0@Rz.T)+t))
Xm=X0.copy(); Xm[:,0]*=-1
print("   (2) mirrored copy (must be rejected): rms %.4f max %.4f det %+.1f" % kabsch(X0,Xm))
print("   (3) identical copy : rms %.3e max %.3e det %+.1f" % kabsch(X0,X0.copy()))
for n in range(len(pts)-1):
    r,m,dd=kabsch(pts[n]["X"][heavy],pts[n+1]["X"][heavy])
    flag="OK (rms<0.3, det=+1 => no branch switch)" if (r<0.3 and abs(dd-1)<1e-6) else "CHECK"
    print("  scan#%d->#%d heavy20: rms %.4f max %.4f det %+.1f  [%s]" % (n+1,n+2,r,m,dd,flag))
print()
print("=== in-progress point (not converged, excluded from pool and from neighbour tables) ===")
ls=[(i+1,L[i].strip()) for i in range(len(L)) if "on scan point" in L[i] and "Step number" in L[i]][-1]
h,bX,bEl=blocks[-1]
mm=met(bX,bEl)
print("  last step L%d : %s" % ls)
print("  last block L%d : meas (R(2,4)=%.4f, R(25,26)=%.4f) R(4,26)=%.4f R(10,27)=%.4f H26 nearest %s%d %.4f" % (h,mm["r24"],mm["rp"],mm["r426"],mm["r1027"],Z[mm["h26"][2]],mm["h26"][1],mm["h26"][0]))
if exh:
    for l,s in exh: print("  maxstep-exhausted L%d : %s" % (l,s))
else:
    print("  maxstep-exhausted points: none")
print()
print("disclaimer: constrained profile, O10-H27 frozen; candidates are TS candidates / upper bounds only; never dE-dagger; E3b result and barrier stay null.")
print("  span wording (coordinator ruling 22:35): verified-minima span 1.6086 kcal/mol (P=job 1061 -4.3383 vs 1073 -2.7297);")
print("  product-side reference uncertainty >=1.58 kcal/mol, not capped (lowest unverified reading 1071 L161621 = -5.9172 vs 1028; gap to P = 1.5789);")
print("  proton path (direct H26 transfer vs H27-relayed double shuttle) still undetermined;")
print("  instantaneous reading span ~3.1875 kcal/mol is a SNAPSHOT only (contains unverified trajectory frames, varies with 1071, not an invariant, never a denominator).")
