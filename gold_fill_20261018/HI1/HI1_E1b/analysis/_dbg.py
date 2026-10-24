import sys
sys.path.insert(0,'gold_fill_20261018/HI1/HI1_E1b/analysis')
import importlib.util
spec=importlib.util.spec_from_file_location("m","gold_fill_20261018/HI1/HI1_E1b/analysis/freq_mode_d1.py")
m=importlib.util.module_from_spec(spec)
sys.argv=["x","gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log"]
try: spec.loader.exec_module(m)
except SystemExit: pass
L=m.read_lines("gold_finish_20261015/HI1/E1/split/INT1_27_optfreq.log")
ob=m.orientation_blocks(L)
for st,tab in ob[-4:]:
    print(st, len(tab), "hdr:", L[st-1].strip())
    d={t[0]:(t[1],round(t[2],3),round(t[3],3),round(t[4],3)) for t in tab}
    print("  1:",d[1]," 2:",d[2]," 3:",d[3]," 4:",d[4]," 10:",d[10])
