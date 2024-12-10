#!/bin/bash

# we must do some preprocessing
rm -f 1UBQ_clean.pdb
sed 's/HG  SER A/HG1 SER A/g' ../1UBQ_clean.pdb >> 1UBQ_clean.pdb

# must be run interactively
# because MET is a terminal residue
# it confuses this one with a sugar residue
# thus you must set all protonation states
# and terminal residues manually
gmx pdb2gmx -f 1UBQ_clean.pdb -water none -ff charmm36-jul2022 -inter -o 1UBQ_gmx.pdb
