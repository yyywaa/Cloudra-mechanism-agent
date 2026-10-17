import numpy as np, json
BASE="/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/HI1/E3/"
def blocks(path):
    L=open(path).read().splitlines(); out=[]; i=0
    while i < len(L):
        if "Input orientation:" in L[i] or "Standard orientation:" in L[i]:
            k=i+1; co=[]; el=[]
            while k < len(L) and len(co) < 41:
                p=L[k].split()
                if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                    el.append(int(p[1])); co.append([float(p[3]),float(p[4]),float(p[5])])
                k+=1
            if len(co)==41: out.append((i+1,np.array(co),el))
            i=k
        else: i+=1
    return out
B=blocks(BASE+"runs/build_seed_product_optfreq.log")
b=[x for x in B if x[0] < 49775][-1]
X=b[1]; el=b[2]
print("block L%d, elements (first 12):"%b[0], el[:12])
print("element histogram:", {z:el.count(z) for z in set(el)})
def r(a,b_): return float(np.linalg.norm(X[a-1]-X[b_-1]))
print("RAW (no mapping) key distances, 1-based:")
for nm,(i,j) in {"R(2,4)":(2,4),"R(2,25)":(2,25),"R(4,26)":(4,26),"R(25,26)":(25,26),"R(10,27)":(10,27),"R(2,26)":(2,26)}.items():
    print("  %-10s %.4f  (elements %d-%d)" % (nm, r(i,j), el[i-1], el[j-1]))
# N atom and its neighbours
n=[i+1 for i,z in enumerate(el) if z==7]
print("N atoms at (1-based):", n)
for a in n:
    ds=sorted(((float(np.linalg.norm(X[a-1]-X[k])),k+1,el[k]) for k in range(41) if k+1!=a))[:4]
    print("  N%d neighbours:" % a, ", ".join("%d(%d) %.4f"%(k,z,d) for d,k,z in ds))
o=[i+1 for i,z in enumerate(el) if z==8]
for a in o:
    ds=sorted(((float(np.linalg.norm(X[a-1]-X[k])),k+1,el[k]) for k in range(41) if k+1!=a))[:4]
    print("  O%d neighbours:" % a, ", ".join("%d(%d) %.4f"%(k,z,d) for d,k,z in ds))
