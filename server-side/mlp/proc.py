

f = open("log.log","r")

pci = []
for l in f:
    line = l.strip().split()
    try:
        pci.append(float(line[1]))
    except:
        pass
import numpy as np

pci = np.array(pci)

print("avg",np.average(pci))
print("max",np.max(pci))
print("min",np.min(pci))
print("std",np.std(pci))
