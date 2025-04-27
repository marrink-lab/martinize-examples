import sys
import vermouth
from vermouth.forcefield import ForceField
from vermouth.gmx.itp_read import read_itp
import networkx as nx
from collections import defaultdict

file = sys.argv[1]

with open(file, "r") as _file:
    lines = _file.readlines()

ff = ForceField("test")
read_itp(lines, ff)

mol = ff.blocks[sys.argv[2]]
print("atoms", len(mol.nodes))
for inter_type in ["bonds", "angles", "pairs"]:
    print(inter_type, len(mol.interactions[inter_type]))

counts =  {}
for inter in mol.interactions["dihedrals"]:
    fdx = inter.parameters[0]
    count = counts.get(fdx, 0)
    counts[fdx] = count + 1

print(counts)
print("Dihedals")
for idx, n in counts.items():
    print(idx, n)
print("---")
total=0
for resid in range(1, 6):
    cg=0
    for node in mol.nodes:
        if mol.nodes[node]['resid'] == resid:
            cg+= float(mol.nodes[node]['charge'])
            total += float(mol.nodes[node]['charge'])
    print(resid, cg)
print("tot", total)

di = defaultdict(list)
for node in mol.nodes:
    aname = mol.nodes[node]['atype']
    cg = mol.nodes[node]['charge']
    di[aname].append(cg)

#for name, values in di.items():
#    print(name, set(values))
