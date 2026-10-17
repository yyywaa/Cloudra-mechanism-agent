import sys, math
rad = {"H":0.31,"C":0.76,"N":0.71,"O":0.66,"S":1.05}
def xyz(path):
    L = open(path).read().splitlines(); n = int(L[0]); at=[]
    for l in L[2:2+n]:
        p=l.split(); at.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return at
at = xyz(sys.argv[1]); n=len(at)
par=list(range(n))
def find(a):
    while par[a]!=a: par[a]=par[par[a]]; a=par[a]
    return a
def uni(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: par[ra]=rb
for i in range(n):
    for j in range(i+1,n):
        if math.dist(at[i][1:],at[j][1:]) < 1.3*(rad[at[i][0]]+rad[at[j][0]]): uni(i,j)
comp={}
for i in range(n): comp.setdefault(find(i),[]).append(i+1)
cid={}
for k,(root,mem) in enumerate(sorted(comp.items(), key=lambda kv:-len(kv[1]))):
    for m in mem: cid[m]=k
print("frag sizes", [len(v) for v in comp.values()])
best=[]
for i in range(1,n+1):
    for j in range(i+1,n+1):
        if cid[i]!=cid[j] and at[i-1][0]=="C" and at[j-1][0]=="C":
            best.append((math.dist(at[i-1][1:],at[j-1][1:]), i, j, cid[i], cid[j]))
best.sort()
print("cross-fragment C...C:", [(round(d,3),i,j,ci,cj) for d,i,j,ci,cj in best[:6]])
bestX=[]
for i in range(1,n+1):
    for j in range(i+1,n+1):
        if cid[i]!=cid[j] and (at[i-1][0]=="C" or at[j-1][0]=="C") and (at[i-1][0] in "NO" or at[j-1][0] in "NO"):
            bestX.append((math.dist(at[i-1][1:],at[j-1][1:]), at[i-1][0]+str(i), at[j-1][0]+str(j)))
bestX.sort()
print("cross-fragment C/X:", [(round(d,3),a,b) for d,a,b in bestX[:6]])
