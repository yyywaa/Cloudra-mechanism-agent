import math
P = '/home/ly/Cloudra-mechanism-agent/ts/ts_0016/jobs/declaration_0007/frequency/frequency.log'
L = open(P).read().splitlines()
print('total lines', len(L))
freqs = [(i+1, l.strip()) for i, l in enumerate(L) if 'Frequencies --' in l]
print('Frequencies lines', len(freqs), 'first', freqs[0])
print('imaginary head lines', [i+1 for i, l in enumerate(L) if 'imaginary' in l.lower()][:3])
# displacement block after first Frequencies line
i0 = freqs[0][0]
# find the atom displacement table rows: lines with 5 columns, first two ints
rows = []
j = i0
while j < len(L) and len(rows) < 41:
    p = L[j].split()
    if len(p) == 5:
        try:
            idx = int(p[0]); z = int(p[1]); dx, dy, dz = float(p[2]), float(p[3]), float(p[4])
            rows.append((idx, z, dx, dy, dz, j+1))
        except ValueError:
            pass
    j += 1
print('parsed atom rows', len(rows))
if rows:
    mags = [(math.sqrt(r[2]**2 + r[3]**2 + r[4]**2), r[0], r[1], r[5]) for r in rows]
    mags.sort(reverse=True)
    print('top 8 |d|: (|d|, atom, Z, line)')
    for m in mags[:8]:
        print('   %.4f  atom %2d Z=%d L%d' % m)
    tot = sum(m[0]**2 for m in mags)
    print('sum |d|^2 = %.5f' % tot)
    top3 = mags[:3]
    print('top3 share of sum|d|^2 = %.3f' % (sum(m[0]**2 for m in top3)/tot))
    heavy = [m for m in mags if m[2] != 1]
    print('heavy top3:', ['atom %d |d|=%.4f' % (m[1], m[0]) for m in heavy[:3]])
    print('all non-top atoms |d| max = %.4f' % mags[3][0])
