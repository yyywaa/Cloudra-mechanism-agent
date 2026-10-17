import math
L=open("ts/ts_0019/jobs/declaration_0001/ts_opt/refine.log").read().splitlines()
blocks=[]
i=0
while i<len(L):
    if "Input orientation:" in L[i]:
        k=i+1; co=[]
        while k<len(L) and len(co)<41:
            p=L[k].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit(): co.append((float(p[3]),float(p[4]),float(p[5])))
            k+=1
        if len(co)==41: blocks.append((i+1,co))
        i=k
    else: i+=1
print("blocks:",len(blocks),"last block header line:",blocks[-1][0])
X=blocks[-1][1]
g=lambda a: X[a-1]
d=lambda a,b: math.dist(g(a),g(b))
for nm,a,b in [("C2-N4",2,4),("C2-O25",2,25),("N4-H26",4,26),("O25-H26",25,26),("O10-H27",10,27),("C2...H26",2,26),("C9-O10",9,10),("C9-O11",9,11)]:
    print("  %-9s %.4f" % (nm, d(a,b)))
heavy=[a for a in range(1,42) if a!=26 and L[blocks[-1][0]+5+ (a-1)].split()[1] not in ("1",)]
# nearest heavy to H26 using element info from header rows
els={}
k=blocks[-1][0]
while k<len(L) and len(els)<41:
    p=L[k].split()
    if len(p)==6 and p[0].isdigit() and p[1].isdigit(): els[int(p[0])]=int(p[1])
    k+=1
Z={1:"H",6:"C",7:"N",8:"O"}
nn=sorted((math.dist(g(26),g(a)),a,Z[els[a]]) for a in range(1,42) if els[a]!=1 and a!=26)[:2]
print("H26 nearest heavy:",[(round(x[0],4),x[1],x[2]) for x in nn])
print("--- last convergence table (L222261-222267) ---")
for k in range(222260,222268): print("  L%d %s" % (k+1, L[k]))