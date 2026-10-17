
import re, math, sys
log = sys.argv[1]
lines = open(log, errors='replace').read().splitlines()
blocks = []   # (endline_index0, atoms)
i = 0
while i < len(lines):
    L = lines[i]
    if ('Standard orientation:' in L) or ('Input orientation:' in L):
        j = i + 1
        dashes = 0
        while j < len(lines) and dashes < 2:
            if lines[j].strip().startswith('---'):
                dashes += 1
            j += 1
        atoms = []
        while j < len(lines):
            parts = lines[j].split()
            if len(parts) == 6 and parts[0].isdigit() and parts[1].isdigit():
                atoms.append((int(parts[1]), float(parts[3]), float(parts[4]), float(parts[5])))
                j += 1
            else:
                break
        if atoms:
            blocks.append((j, atoms))
        i = j
        continue
    i += 1
pt = 0; scfE = None; scfL = None; records = []
for i, L in enumerate(lines, 1):
    m = re.search(r'on scan point\s+(\d+) out of\s+(\d+)', L)
    if m: pt = int(m.group(1))
    if 'SCF Done:' in L:
        mm = re.search(r'E\(RB3LYP\)\s*=\s*(-?\d+\.\d+)', L)
        if mm: scfE = float(mm.group(1)); scfL = i
    if 'Optimization completed.' in L:
        records.append((pt, i, scfE, scfL))
def d(a,b,A): return math.dist(A[a-1][1:], A[b-1][1:])
print('blocks:', len(blocks), 'records:', len(records))
print('%2s %6s %7s %16s %7s %7s %8s %8s %7s %8s %s' % ('pt','opL','scfL','E(RB3LYP)','R2-18','R2-3','R18-27','R3-27','minsep','atoms','tightest4'))
for k,(pt,opL,scfE,scfL) in enumerate(records,1):
    cand = [b for b in blocks if b[0] < opL]
    endL, atoms = cand[-1]
    ms = sorted(((d(a,b,atoms),a,b) for a in range(1,len(atoms)+1) for b in range(a+1,len(atoms)+1)))
    print('%2d %6d %7d %16.9f %7.4f %7.4f %8.4f %8.4f %7.4f %8d %s' % (k, opL, scfL, scfE,
        d(2,18,atoms), d(2,3,atoms), d(18,27,atoms), d(3,27,atoms), ms[0][0], len(atoms),
        ' | '.join('%.4f %d-%d'%(m[0],m[1],m[2]) for m in ms[:4])))
