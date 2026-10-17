import re, sys
def parse(path):
    d = open(path, errors='ignore').read()
    i = d.rfind('HF=-463')
    seg = d[i:].split('RMSD')[0].replace('\n', '')
    nums = [float(x) for x in re.findall(r'-?\d+\.\d+', seg)]
    return nums
for p in sys.argv[1:]:
    v = parse(p)
    print('###', p, 'n=', len(v))
    lab = {0:'R-side d(O8-H4) 1.4976->2.30 (job903)', 1:'P-side d(O8-H4) 1.4976->1.00 (job906)'}
    ref = v[0]
    for k, e in enumerate(v):
        print(' pt%02d  %.7f  dE=%+7.2f kcal' % (k+1, e, (e-ref)*627.509474))
