import sys
seed = [l.split() for l in open(sys.argv[1]).read().splitlines()[2:] if l.strip()]
gjf  = [l.split() for l in open(sys.argv[2]).read().splitlines()[7:] if l.strip()]
print("seed atoms", len(seed), "gjf atoms", len(gjf))
same_el = all(a[0] == b[0] for a, b in zip(seed, gjf))
mx = max(abs(float(a[i]) - float(b[i])) for a, b in zip(seed, gjf) for i in (1, 2, 3))
print("element_sequence_identical", same_el)
print("max_abs_coord_dev_angstrom", round(mx, 6))
print("first3", seed[:3])
print("gjf_first3", gjf[:3])
