import math
def mode1(P, freqline_idx, n=41):
    L = open(P).read().splitlines()
    rows = []
    j = freqline_idx
    while j < len(L) and len(rows) < n:
        p = L[j].split()
        if len(p) == 11:
            try:
                idx = int(p[0]); z = int(p[1])
                v = [float(x) for x in p[2:]]
                rows.append((idx, z, v[0], v[1], v[2], j + 1))
            except ValueError:
                pass
        j += 1
    return rows

for tag, P, ln in [('ts_0016 (E3a)', '/home/ly/Cloudra-mechanism-agent/ts/ts_0016/jobs/declaration_0007/frequency/frequency.log', 1509),
                   ('ts_0011 (HI1_E3)', '/home/ly/Cloudra-mechanism-agent/ts/ts_0011/jobs/declaration_0004/frequency/frequency.log', 1510)]:
    rows = mode1(P, ln)
    mags = sorted([(math.sqrt(r[2]**2+r[3]**2+r[4]**2), r[0], r[1], r[5]) for r in rows], reverse=True)
    tot = sum(m[0]**2 for m in mags)
    print('===', tag, 'rows', len(rows), 'sum|d|^2 = %.5f' % tot)
    for m in mags[:6]:
        print('   |d|=%.4f atom %2d Z=%d L%d  share=%.3f' % (m[0], m[1], m[2], m[3], m[0]**2/tot))
    d = {r[0]: math.sqrt(r[2]**2+r[3]**2+r[4]**2) for r in rows}
    print('   key atoms: |d| C2=%d:%.4f N4=%d:%.4f O10=%d:%.4f O25=%d:%.4f H26=%d:%.4f H27=%d:%.4f O28=%d:%.4f H24=%d:%.4f' % (
       2, d.get(2,0), 4, d.get(4,0), 10, d.get(10,0), 25, d.get(25,0), 26, d.get(26,0), 27, d.get(27,0), 28, d.get(28,0), 24, d.get(24,0)))
    heavy = [m for m in mags if m[2] != 1]
    print('   heavy top3:', ['atom %d %.4f' % (m[1], m[0]) for m in heavy[:3]])
    print('   H top3:', ['atom %d %.4f' % (m[1], m[0]) for m in [x for x in mags if x[2]==1][:3]])
