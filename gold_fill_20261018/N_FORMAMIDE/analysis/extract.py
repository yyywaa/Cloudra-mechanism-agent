#!/usr/bin/env python3
"""Extract G16 evidence: normal termination, last SCF Done (value+line), frequencies,
imaginary modes, optimization convergence flags, sha256. Read-only on logs."""
import sys, re, hashlib, os
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda: f.read(1<<20), b''): h.update(b)
    return h.hexdigest()
def analyze(p):
    lines=open(p, errors='replace').read().split('\n')
    scf=[(i+1,l) for i,l in enumerate(lines) if 'SCF Done' in l]
    imag=[(i+1,l) for i,l in enumerate(lines) if 'imaginary frequencies' in l.lower() or 'imaginary frequenc' in l.lower()]
    freqs=[(i+1,l) for i,l in enumerate(lines) if re.search(r'Frequencies --', l)]
    term=[(i+1,l) for i,l in enumerate(lines) if 'Normal termination' in l or 'Error termination' in l]
    stat=[(i+1,l) for i,l in enumerate(lines) if 'Stationary point found' in l or 'Optimization completed' in l]
    negs=[]
    for i,l in freqs:
        for v in re.findall(r'-\d+\.\d+', l): negs.append((i, float(v)))
    print('FILE', os.path.abspath(p))
    print('SHA256', sha(p))
    print('SCF_LAST', scf[-1] if scf else None, ' N_SCF', len(scf))
    print('FREQ_LINES', [i for i,_ in freqs])
    print('NEG_FREQS', negs)
    print('TERMINATION', term[-1] if term else None)
    print('STATIONARY', stat)
    for i,l in imag: print('IMAG_LINE', i, l.strip())
if __name__=='__main__':
    for p in sys.argv[1:]: analyze(p); print('-'*60)
