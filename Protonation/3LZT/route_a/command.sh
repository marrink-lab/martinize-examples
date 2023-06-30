#!/bin/bash

mkdir output
cd output
martinize2 -resid input -f ../3lzt_charmm_named.pdb -x cg.pdb -o sys.top -dssp -ff martini3001 -scfix -from charmm -maxwarn 1 -bonds-fudge 1 >& command.log
