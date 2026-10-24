import re, math, hashlib, sys
p="/home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0004/irc/irc.log"
raw=open(p,'rb').read(); h=hashlib.sha256(raw).hexdigest()
L=raw.decode('utf-8','replace').splitlines()
print("sha256",h,"lines",len(L))
def dists(co):
    d=lambda i,j: math.dist(co[i],co[j])
    return dict(O1H2=d(1,2), H2O9=d(2,9), H4N8=d(4,8), O1H4=d(1,4), O1H3=d(1,3),
                H2N8=d(2,8), O9H16=d(9,16), O1O9=d(1,9))
frames=[]; i=0
while i < len(L):
    if "Input orientation:" in L[i]:
        # look back up to 12 lines for Point Number / Path Number
        pt=path=None
        for k in range(i-1, max(-1,i-16), -1):
            m=re.search(r"Point Number:\s*(\d+)\s*Path Number:\s*(\d+)", L[k])
            if m: pt,path=int(m.group(1)),int(m.group(2)); break
        co={}; k=i+5
        while k < len(L) and not L[k].strip().startswith("-----"):
            f=L[k].split()
            if len(f)>=6:
                try: co[int(f[0])]=tuple(float(x) for x in f[3:6])
                except: pass
            k+=1
        # energy: nearest following SCF Done
        e=None
        for k in range(i, min(len(L), i+400)):
            m=re.search(r"SCF Done:\s+E\(\S+\)\s*=\s*(-?\d+\.\d+)", L[k])
            if m: e=float(m.group(1)); break
        if len(co)==19: frames.append(dict(line=i+1, pt=pt, path=path, co=co, e=e))
        i=k
    i+=1
print("frames", len(frames))
for f in frames:
    dd=dists(f["co"])
    q=dd["O1H2"]-dd["H2O9"]; qp=-q
    print(f"L{f['line']} pt={f['pt']} path={f['path']} E={f['e']} O1H2={dd['O1H2']:.4f} H2O9={dd['H2O9']:.4f} q={q:+.4f} q'={qp:+.4f} O1O9={dd['O1O9']:.4f} H4N8={dd['H4N8']:.4f} O1H4={dd['O1H4']:.4f} O1H3={dd['O1H3']:.4f} H2N8={dd['H2N8']:.4f} O9H16={dd['O9H16']:.4f}")
