#!/bin/bash

mkdir output
cd output
martinize2 -resid input -f ../1mj5_all_hydrogen.pdb -x cg.pdb -o sys.top -dssp -ff martini3001 -scfix -from amber -maxwarn 1 >& command.log
