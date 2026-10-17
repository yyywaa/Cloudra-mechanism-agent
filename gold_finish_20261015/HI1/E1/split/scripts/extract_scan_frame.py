
import re, math, sys
log, k, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = open(log, errors='replace').read().splitlines()
opL = [i for i,L in enumerate(lines,1) if 'Optimization completed' in L]
print('optimization-completed lines:', len(opL), '->', opL)
target = opL[k-1]
blocks = []
i = 0
while i < len(lines):
    L = lines[i]
    if ('Standard orientation:' in L) or ('Input orientation:' in L):
        j = i+1; dashes = 0
        while j < len(lines) and dashes < 2:
            if lines[j].strip().startswith('---'): dashes += 1
            j += 1
        atoms = []
        while j < len(lines):
            p = lines[j].split()
            if len(p)==6 and p[0].isdigit() and p[1].isdigit():
                atoms.append((int(p[1]), float(p[3]), float(p[4]), float(p[5]))); j += 1
            else: break
        if atoms: blocks.append((j, i+1, atoms))
        i = j; continue
    i += 1
cand = [b for b in blocks if b[0] < target]
endL, startL, atoms = cand[-1]
sym = {1:'H',6:'C',7:'N',8:'O'}
print('frame: orientation block start line', startL, 'end line', endL, 'natoms', len(atoms))
def d(a,b): return math.dist(atoms[a-1][1:], atoms[b-1][1:])
ms = sorted((d(a,b),a,b) for a in range(1,len(atoms)+1) for b in range(a+1,len(atoms)+1))
print('R(2,18)=%.4f R(2,3)=%.4f R(18,27)=%.4f R(3,27)=%.4f R(2,4)=%.4f' % (d(2,18), d(2,3), d(18,27), d(3,27), d(2,4)))
print('minsep %.4f (%d-%d); next', ms[0])
for m in ms[1:5]: print('   %.4f %d-%d' % m)
assert len(atoms)==27, 'atom count'
with open(outp,'w') as f:
    f.write('%d\n' % len(atoms))
    f.write('E1a constrained-relaxation scan job1070 point %d converged frame (R(2,18) fixed) | post-freeze asset, non-delivery | logLine %d\n' % (k, target))
    for z,x,y,zz in atoms:
        f.write('%s %.8f %.8f %.8f\n' % (sym[z], x, y, zz))
print('wrote', outp)
