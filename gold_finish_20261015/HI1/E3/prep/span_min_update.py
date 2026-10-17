import re, sys, subprocess
T="/home/ly/Cloudra-mechanism-agent/ts/ts_0020/jobs/declaration_0001/ts_opt/refine.log"
k=627.5095; ref=-939.312626605; P=-939.319540184; MAXver=-939.316976731  # 1073 (verified minimum, highest of the two)
L=open(T).read().splitlines()
scf=[(i+1,float(re.search(r"E\(RB3LYP\) =\s*(-?\d+\.\d+)",ln).group(1))) for i,ln in enumerate(L) if "SCF Done" in ln]
mn=min(scf,key=lambda x:x[1])
print("log lines: %d | SCF lines: %d" % (len(L),len(scf)))
print("GLOBAL MIN (min over all SCF lines, NOT the last line):")
print("  L%d = %.9f  =>  %+.4f kcal/mol vs 1028 ; %+.4f vs P(job 1061)" % (mn[0],mn[1],(mn[1]-ref)*k,(mn[1]-P)*k))
print("last SCF : L%d = %.9f => %+.4f vs 1028" % (scf[-1][0],scf[-1][1],(scf[-1][1]-ref)*k))
print("lowest 4 : " + " | ".join("L%d %+.4f" % (l,(e-ref)*k) for l,e in sorted(scf,key=lambda x:x[1])[:4]))
unc=abs((mn[1]-P)*k)
import datetime
now=datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
print()
import math
_floor=math.floor(unc*100.0)/100.0   # lower bounds are rounded DOWN, never up (coordinator 23:09)
term=[(i+1,ln.strip()) for i,ln in enumerate(L) if ln.startswith(" Normal termination of Gaussian 16")]
if term:
    # job finished: the "not capped" wording applies ONLY to a still-running job (coordinator ruling 23:58)
    print("sentence (job FINISHED -- 'not capped' must NOT be used):")
    print("  product-side reference uncertainty = |lowest unverified frame - P|; as of %s  >= %.2f kcal/mol, and THIS JOB NO LONGER REFRESHES (lowest frame L%d = %.9f; %+.4f vs 1028 / %+.4f vs P; %s; the stationary point's frequencies are unverified, so a lower species cannot be excluded)  [bound floored from %.4f]" % (term[-1][1].split(" at ")[-1],_floor,mn[0],mn[1],(mn[1]-ref)*k,(mn[1]-P)*k,term[-1][1],unc))
else:
    print("sentence (job STILL RUNNING -- 'not capped, will refresh' applies):")
    print("  product-side reference uncertainty = |lowest unverified frame - P|; as of %s  >= %.2f kcal/mol, not capped  [bound floored from %.4f]" % (now,_floor,unc))
print("  (value = |%.4f - (%.4f)| = %.4f)" % ((mn[1]-ref)*k,-4.3383,unc))
print("  P (job 1061) is a frequency-verified product-side minimum but NOT the lowest known stationary point: another gradient-converged stationary point lies 2.1093 kcal/mol BELOW it (1071 final frame, frequencies unverified).")
print("instantaneous reading span (snapshot only, never a denominator) = max(1073 %.4f) - min(%.4f) = %.4f" % ((MAXver-ref)*k,(mn[1]-ref)*k,(MAXver-ref)*k-(mn[1]-ref)*k))
