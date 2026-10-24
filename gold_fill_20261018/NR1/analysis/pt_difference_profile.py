#!/usr/bin/env python3
"""Composite true PT difference coordinate from jobs 903 + 906 (E1 lane numbering).
dR = r(O1-H4) - r(H4-O8); duplicated shared starting point removed."""
import sys, math
sys.path.insert(0, '/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/NR1/analysis')
from scan_table import parse, d
B='/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/NR1/E1/'
rows=[]
for tag,p in [('903',B+'scan/pt_scan_R_01.log'),('906',B+'scan_P/pt_scan_P_01.log')]:
    pts=parse(p)
    for n,pt in enumerate(pts,1):
        at=pt['geom'][1]; e=pt['scf'][1]
        rows.append({'job':tag,'pt':n,'E':e,'scf_line':pt['scf'][0],
                     'O1H4':d(at,1,4),'H4O8':d(at,4,8),'OO':d(at,1,8),'CO':d(at,6,8)})
# de-duplicate the identical starting point
dedup=[]; seen=set()
for r in rows:
    key=(round(r['E'],9), round(r['O1H4'],6), round(r['H4O8'],6))
    if key in seen: continue
    seen.add(key); dedup.append(r)
for r in dedup: r['dR']=r['O1H4']-r['H4O8']
dedup.sort(key=lambda r: r['dR'])
emin=min(dedup,key=lambda r:r['E'])
print('n_unique_points', len(dedup), ' min point: job %s pt%d dR=%+.4f E=%.9f (L%d)'%(emin['job'],emin['pt'],emin['dR'],emin['E'],emin['scf_line']))
print(' max dR = %+.4f (job %s pt%d, E=%.9f)'%(max(dedup,key=lambda r:r['dR'])['dR'], max(dedup,key=lambda r:r['dR'])['job'], max(dedup,key=lambda r:r['dR'])['pt'], max(dedup,key=lambda r:r['dR'])['E']))
prev=None; peak=0
print('dR(A)    E(Ha)              rel(kcal)  job/pt  scf_line  r(O1-H4) r(H4-O8) O1..O8  C6-O8')
for r in dedup:
    rel=(r['E']-emin['E'])*627.5095
    print('%+7.4f  %.9f  %+8.3f   %s/pt%-2d  L%-6d  %7.4f %8.4f %7.4f %7.4f'%(r['dR'],r['E'],rel,r['job'],r['pt'],r['scf_line'],r['O1H4'],r['H4O8'],r['OO'],r['CO']))
