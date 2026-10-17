import sys, re, numpy as np

def parse(path):
    lines=open(path, errors='ignore').read().splitlines()
    groups=[]; imag_header=None; imag_rows=[]
    i=0
    while i < len(lines):
        L=lines[i]
        if L.startswith(' Frequencies --'):
            fr=[float(x) for x in L.split('--')[1].split()]
            rm=[]; fc=[]
            j=i+1
            while j < len(lines) and j < i+8:
                if lines[j].startswith(' Red. masses --'): rm=[float(x) for x in lines[j].split('--')[1].split()]
                if lines[j].startswith(' Frc consts  --') or lines[j].startswith(' Frc consts --'): fc=[float(x) for x in lines[j].split('--')[1].split()]
                if lines[j].strip().startswith('Atom  AN'): break
                j+=1
            disp={}
            if j < len(lines) and lines[j].strip().startswith('Atom  AN'):
                k=j+1
                while k < len(lines) and lines[k].strip() and re.match(r'^\s*\d+\s+\d+', lines[k]):
                    p=lines[k].split()
                    if len(p) != 2+3*len(fr): k+=1; continue
                    an=int(p[0]); vals=[float(x) for x in p[2:2+3*len(fr)]]
                    disp[an]=np.array(vals)
                    k+=1
            groups.append({'freq':fr,'rm':rm,'fc':fc,'disp':disp,'line':i+1})
            i=j
            continue
        if 'imaginary frequencies' in L.lower() and 'negative sign' in L.lower():
            imag_header=(i+1, L.strip()); k=i+1
            while k<len(lines) and lines[k].strip() and re.match(r'^\s*\d+\s+-?\d+\.\d+', lines[k]):
                imag_rows.append((k+1, lines[k].strip())); k+=1
            i=k; continue
        i+=1
    return groups, imag_header, imag_rows

path=sys.argv[1]; target=float(sys.argv[2]) if len(sys.argv)>2 else None
g,hdr,rows=parse(path)
nmodes=sum(len(x['freq']) for x in g)
print('groups',len(g),'modes',nmodes,'imag_header',hdr)
print('imag_rows',rows)
# locate mode closest to target freq
best=None
for gi,x in enumerate(g):
    for mi,f in enumerate(x['freq']):
        if target is not None and abs(f-target)<1e-3: best=(gi,mi)
if best is None:
    neg=[(gi,mi,x['freq'][mi]) for gi,x in enumerate(g) for mi in range(len(x['freq'])) if x['freq'][mi]<0]
    print('negative modes found:',neg); 
    best=(neg[0][0],neg[0][1]) if neg else None
if best:
    gi,mi=best; x=g[gi]
    print('chosen mode freq %.4f at line %d ; red.mass %s ; frc const %s'%(x['freq'][mi],x['line'],x['rm'][mi] if x['rm'] else None,x['fc'][mi] if x['fc'] else None))
    vecs={a:v[3*mi:3*mi+3] for a,v in x['disp'].items()}
    tot=sum(float(np.linalg.norm(v)) for v in vecs.values())
    order=sorted(vecs, key=lambda a:-float(np.linalg.norm(vecs[a])))[:6]
    for a in order: print('  atom %d |d|=%.4f share=%.4f vec=%s'%(a,float(np.linalg.norm(vecs[a])),float(np.linalg.norm(vecs[a]))/tot,np.round(vecs[a],4)))
    print('sum|d| %.4f'%tot)