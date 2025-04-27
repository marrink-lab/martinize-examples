import sys
import os
import re
from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import gromacs
import vermouth
from vermouth.gmx.gro import write_gro
from vermouth.gmx.itp_read import read_itp
from vermouth.forcefield import ForceField
from vermouth.processors import MakeBonds
#from polyply import gen_params
#from polyply.src.graph_utils import find_one_ismags_match
#from polyply.src.topology import Topology

import gromacs.environment
gromacs.environment.flags['capture_output'] = True

import argparse

def _element_match(node1, node2):
     """
     Checks if the element attribute of two nodes
     is the same.

     Returns
     --------
     bool
     """
     return node1["element"] == node2["element"]

def _is_not_digit(_str):
    return not _str.isdigit()

def align_coordinates(itp_file, ref_file, outname, polymer):
    """
    Take an itp and a reference pdb file with coordinates
    corresponding to the itp_file. Figure out which coordinates
    belong to which atoms by using a subgraph isomorphism.

    Note the PDB file must have connect records. Order, atom names,
    residue names are all ignored.
    """
    print(itp_file)
    # create empty system
    ref_sys = vermouth.System()
    # load PDB and add edges to ref molecule
    vermouth.PDBInput(str(ref_file), modelidx=1).run_system(ref_sys)
    MakeBonds(allow_name=False,  allow_dist=False).run_system(ref_sys)
    ref_mol = ref_sys.molecules[0]
    print(len(ref_mol.edges))
    # load the target molecule
    top = Topology.from_gmx_topfile(itp_file, "polymer")
    target_mol = top.molecules[0].molecule
    target_mol.make_edges_from_interaction_type(type_="bonds")
    print(len(target_mol.edges))
    # assign elements to target_mol
    for node in target_mol.nodes:
        element = target_mol.nodes[node]['atomname'][0]
        target_mol.nodes[node]['element'] = element

    match = find_one_ismags_match(ref_mol, target_mol, _element_match)

    for ref_node, target_node in match.items():
        target_mol.nodes[target_node]['position'] = ref_mol.nodes[ref_node]['position']
    ref_sys.molecules[0] = target_mol
    # write out the matching coordinates
    write_gro(ref_sys, f"./{outname}.gro", box=(10.0, 10.0, 10.0), defer_writing=False)
    # convert to PDB file
    gromacs.editconf(f=f"{outname}.gro",
                     o=f"{outname}.pdb",)

def read_energies(filename):
    with open(filename, "r") as _file:
        lines = _file.readlines()
    terms = []
    record = False
    for line in lines:
        tokens = line.strip().split()
        if len(tokens) > 1 and tokens[1] == "s0":
            record = True
        if record and tokens[0] == "@":
            terms.append(" ".join(tokens[3:]))
    energies = map(float, tokens)
    return dict(zip(terms, energies))

def read_smiles(filename):
    """
    Read one or more smiles from a
    file.
    """
    smiles = []
    with open(filename) as _file:
        for line in _file.readlines():
            smile = line.strip().split()
            smiles += smile
    return smiles

def gmx_single_point(topfile, coordfile, mdpfile, prefix):
    """
    Compute GROMACS single point energy.
    """
    gromacs.editconf(f=coordfile, o=f'box_{prefix}.pdb', d=2)
    gromacs.grompp(f=mdpfile,
                   c=f'box_{prefix}.pdb',
                   p=topfile,
                   o=f"{prefix}.tpr",
                   maxwarn=4)
    gromacs.mdrun(s=f"{prefix}.tpr",
                  rerun=f"box_{prefix}.pdb",
                  deffnm=f"{prefix}")
    gromacs.energy(f=f"{prefix}.edr",
                   input="1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 9",
                   o=f"{prefix}.xvg")

def compute_molecule_energies(coordfiles, topfiles, mdpfile, polymer):
    """
    compute energies for the molecules in topfile given a single
    set of refernce coordinates
    """
    os.mkdir(f"comp_{polymer}")
    os.chdir(f"comp_{polymer}")
    # compute the energies
    energies=[]
    for topfile, coordfile, tag in zip(topfiles, coordfiles, ["mol1", "mol2"]):
        gmx_single_point(topfile, coordfile, mdpfile, prefix=tag)
        energies.append(read_energies(f"{tag}.xvg"))
    return energies

def __main__():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-p', dest='topfiles', type=str, nargs=2, help='topology files; at most 2')
    parser.add_argument('-c', dest='coordfile', type=str,  help='coordinate file', nargs=2)
    parser.add_argument('-f', dest='mdpfile', type=str,  help='mdp file')
    parser.add_argument('-mol', dest='molname', type=str, default='polymer',  help='name of molecule')

    args = parser.parse_args()

    energies = compute_molecule_energies([Path(coord).resolve() for coord in args.coordfile],
                                         [Path(top).resolve() for top in args.topfiles],
                                         Path(args.mdpfile).resolve(),
                                         args.molname)

    with open("energy_comp.dat", 'w') as _file:
        e1 = energies[0]
        e2 = energies[1]
        for term in e1:
            _file.write("{} {:3.8F} {:3.8F} {:3.8F}\n".format(term, e1[term], e2[term], e1[term]-e2[term]))
            if np.abs(e1[term]-e2[term]) > 0.1:
                print(args.molname, term, e1[term], e2[term], e1[term]-e2[term])

__main__()
