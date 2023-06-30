#!/bin/bash

mkdir output
cd output

martinize2 -f ../2GS2_WT_model.pdb -x cg.pdb -o test.top -dssp -ff martini22 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -cys auto -maxwarn 2 -ignh >& command.log
