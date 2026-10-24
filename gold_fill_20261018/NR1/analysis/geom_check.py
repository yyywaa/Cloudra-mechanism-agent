import sys, math
sys.path.insert(0, '/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/NR1/analysis')
from e2_scan_torsion import dih
p = sys.argv[1]
L = open(p).read().splitlines()
n = int(L[0].split()[0])
at = []
for i in range(2, 2 + n):
    s = L[i].split()
    at.append((s[0], float(s[1]), float(s[2]), float(s[3])))
def d(i, j):
    return math.dist(at[i-1][1:], at[j-1][1:])
print(p, 'natoms', n)
print('d(5,7)=%.4f d(5,11)=%.4f d(7,11)=%.4f d(5,1)=%.4f d(1,11)=%.4f' % (d(5,7), d(5,11), d(7,11), d(5,1), d(1,11)))
print('dih(7-5-8-11)=%+.1f  dih(7-5-8-9)=%+.1f' % (dih(at[6][1:], at[4][1:], at[7][1:], at[10][1:]), dih(at[6][1:], at[4][1:], at[7][1:], at[8][1:])))
