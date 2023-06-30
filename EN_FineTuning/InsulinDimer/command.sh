#!/bin/bash

mkdir EN_chain
cd EN_chain
martinize2 -eunit chain -f ../3i40.pdb -o test.top -dssp dssp -p backbone -ff martini3001 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -scfix -cys auto
cd ../
mkdir EN_molecule
cd EN_molecule
martinize2 -eunit molecule -f ../3i40.pdb -o test.top -dssp dssp -p backbone -ff martini3001 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -scfix -cys auto
