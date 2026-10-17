import sys, math
def xyz(path):
    L=open(path).read().splitlines(); n=int(L[0]); at=[]
    for l in L[2:2+n]:
        p=l.split(); at.append((p[0], float(p[1]), float(p[2]), float(p[3])))
    return L[1], at
for path in sys.argv[1:]:
    com, at = xyz(path)
    d=lambda i,j: math.dist(at[i-1][1:], at[j-1][1:])
    print(path)
    print("  comment:", com[:110])
    print("  C1...C29=%.4f  C1...C35=%.4f  O28...H24=%.4f  C29-O28=%.4f  C2-N4=%.4f" % (d(1,29), d(1,35), d(28,24), d(29,28), d(2,4)))
