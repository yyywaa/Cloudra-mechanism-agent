import math, hashlib, sys
LOG="/home/ly/Cloudra-mechanism-agent/ts/ts_0022/jobs/declaration_0004/irc/irc.log"
raw=open(LOG,'rb').read(); h=hashlib.sha256(raw).hexdigest()
L=raw.decode().splitlines()
def frame_at(hdr_line, tag):
    # hdr_line: 1-based line of "Input orientation:" ; atoms start +5
    co=[]
    k=hdr_line+4
    while not L[k].strip().startswith("-----"):
        f=L[k].split()
        if len(f)>=6: co.append((f[0], int(f[1]), float(f[3]), float(f[4]), float(f[5])))
        k+=1
    assert len(co)==19, len(co)
    return co
def d(co,i,j): return math.dist(co[i-1][2:], co[j-1][2:])
def report(co,tag,out):
    q={ 'O1H2':d(co,1,2),'H2O9':d(co,2,9),'H4N8':d(co,4,8),'O1H4':d(co,1,4),'O1H3':d(co,1,3),
        'H2N8':d(co,2,8),'O9H16':d(co,9,16),'O1O9':d(co,1,9)}
    qp=q['H2O9']-q['O1H2']
    tot=hashlib.sha256(open(out,'rb').read()).hexdigest()
    print(f"{tag}: elements="+"".join({8:'O',1:'H',6:'C',7:'N'}[c[1]] for c in co))
    print(f"{tag}: O1H2={q['O1H2']:.4f} H2O9={q['H2O9']:.4f} q'={qp:+.4f} O1O9={q['O1O9']:.4f} H4N8={q['H4N8']:.4f} O1H4={q['O1H4']:.4f} O1H3={q['O1H3']:.4f} H2N8={q['H2N8']:.4f} O9H16={q['O9H16']:.4f}")
    print(f"{tag}: xyz={out} sha256={tot}")
# REVERSE outermost: path 2, point 10 -> 'Input orientation' block at L8672
co=frame_at(8672,'rev')
hdr=f"rev_outer seed: TS IRC path2 (REVERSE) point 10 outermost frame | src {LOG} | log sha256 {h} | frame at line 8672 (Input orientation) | extracted programmatically, not retyped"
with open("/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HL1/HL1_E1/irc_endpoints/rev_outer/start.xyz","w") as f:
    f.write(f"19\n{hdr}\n")
    for c in co: f.write(f"{ {8:'O',1:'H',6:'C',7:'N'}[c[1]] }  {c[2]:.8f}  {c[3]:.8f}  {c[4]:.8f}\n")
report(co,'rev','/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HL1/HL1_E1/irc_endpoints/rev_outer/start.xyz')
# also verify the forward copy kept from format_converter
co2=frame_at(4538,'fwd')
report(co2,'fwd(expected)','/home/ly/Cloudra-mechanism-agent/gold_fill_20261018/HL1/HL1_E1/irc_endpoints/fwd_outer/start.xyz')
