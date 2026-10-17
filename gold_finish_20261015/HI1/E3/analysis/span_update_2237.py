K=627.5095; REF=-939.312626605; P=-939.319540184
def d(E): return (E-REF)*K
for n,E in [("L164410 (step161)",-939.322318474),("L165348 (step162)",-939.322199299)]:
    print("%-20s %.9f -> %+0.4f vs 1028 ; %+0.4f vs P" % (n,E,d(E),d(E)-d(P)))
lo=-939.322318474
print("lowest so far -> uncertainty floor = %.4f ; instant spread vs 1073(-2.7297) = %.4f" % (d(P)-d(lo), (-2.7297)-d(lo)))
