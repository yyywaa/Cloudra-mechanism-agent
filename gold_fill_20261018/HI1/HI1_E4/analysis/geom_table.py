import numpy as np, sys, re

def read_xyz(p):
    L=open(p).read().splitlines(); n=int(L[0]); a=[l.split() for l in L[2:2+n]]
    return [x[0] for x in a], np.array([[float(v) for v in x[1:4]] for x in a])

def read_gauss_last_frame(p):
    L=open(p).read().splitlines()
    idx=[i for i,l in enumerate(L) if 'Input orientation:' in l]
    i0=idx[-1]; els=[];X=[]
    for l in L[i0+5:]:
        s=l.split()
        if len(s)==6 and s[0].isdigit():
            els.append({1:'H',6:'C',7:'N',8:'O'}[int(s[1])]); X.append([float(x) for x in s[3:6]])
        elif els: break
    return els, np.array(X)

PAIRS=[(2,25),(2,4),(10,27),(25,27),(28,24),(25,24),(25,26),(10,11)]
def table(el,X,label):
    out={'label':label}
    for a,b in PAIRS:
        out[(a,b)]=float(np.linalg.norm(X[a-1]-X[b-1]))
    return out

frames=[]
B='/home/ly/Cloudra-mechanism-agent/'
frames.append(table(*read_gauss_last_frame(B+'ts/ts_0016/jobs/declaration_0007/frequency/frequency.log'),'TS_old_decl0007_freqL219'))
frames.append(table(*read_xyz(B+'ts/ts_0016/path/input_0007/provided.xyz'),'guess_provided.xyz'))
frames.append(table(*read_xyz(B+'gold_finish_20261015/HI1/E3/runs/I2_optfreq/I2_min_v5.xyz'),'I2_min_job961'))
frames.append(table(*read_xyz(B+'gold_finish_20261015/HI1/E3/prep/hemiaminal_1028_lastframe.xyz'),'P_hemiaminal_job1028'))
hdr='frame'.ljust(30)+''.join(('R(%d,%d)'%(a,b)).rjust(11) for a,b in PAIRS)
print(hdr)
for f in frames:
    print(f['label'].ljust(30)+''.join(('%10.3f '%f[p]) for p in PAIRS))
