import math
def parse(path):
    L = open(path).read().splitlines()
    conv = [i+1 for i,l in enumerate(L) if 'Optimization completed' in l]
    blocks = []
    for i,l in enumerate(L):
        if 'Standard orientation' in l:
            at=[]; j=i+5
            while j < len(L) and not L[j].strip().startswith('-----'):
                p=L[j].split()
                if len(p)==6: at.append((int(p[0]),int(p[1]),float(p[3]),float(p[4]),float(p[5])))
                j+=1
            blocks.append((i+1,at))
    scf=[(i+1,float(l.split('=')[1].split()[0])) for i,l in enumerate(L) if 'SCF Done' in l]
    fr=[]
    for c in conv:
        g=[b for b in blocks if b[0]<c][-1]; s=[x for x in scf if x[0]<c][-1]
        assert len(g[1])==41 and g[1][0][0]==1
        fr.append((g,s,c))
    return L, fr
base='HI1/E2/scan_1d/build/'
for name in ['E2_1D_scan.log','E2_1D_scan_cont1.log']:
    L,fr = parse(base+name)
    print('==', name, 'lines', len(L), 'frames', len(fr), 'conv lines', [f[2] for f in fr])
    for k,(g,s,c) in enumerate(fr,1):
        D={x[0]:x for x in g[1]}
        print('  pt%d hdr L%d SCF L%d E=%.9f R(28,24)=%.4f R(11,24)=%.4f R(1,29)=%.4f' % (
            k,g[0],s[0],s[1], math.dist(D[28][2:],D[24][2:]), math.dist(D[11][2:],D[24][2:]), math.dist(D[1][2:],D[29][2:])))
