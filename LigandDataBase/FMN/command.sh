#!/bin/bash
set -e
mkdir run
cd run

martinize2 -f ../protein_clean_plus.pdb -x cg.pdb -from gromos -o test.top -dssp dssp -p backbone -ff martini22 -resid input -cys auto -maxwarn 4 -ignh -elastic -eunit molecule >& command.log
cat >> system.top << END
#include "../martini_PEO_PS_CNP.itp"
#include "molecule_0.itp"
#include "molecule_1.itp"
#include "molecule_2.itp"
#include "molecule_3.itp"
#include "molecule_4.itp"
[ system ]
protein 

[ molecules ]
molecule_0    1
molecule_1    1
molecule_2    1
molecule_1    1
molecule_3    2
molecule_4    1
END

gmx solvate -cp cg.pdb  -cs ../W.gro   -o start.gro -radius 0.21 -box 10 10 10  >& solv.out
nsol=$(grep "1 atoms" solv.out | awk '{print $5}')

echo "W ${nsol}" >> system.top

echo -e "keep 1 \n name 0 SOLU \n r W | r NA | r CL | r FMN | r NAD \n name 1 SOLV \n q \n" | gmx make_ndx -f start.gro

gmx grompp -f ../min.mdp -c start.gro -p system.top -maxwarn 1 -o min.tpr -r start.gro
gmx mdrun -v -deffnm min -nsteps 2000

gmx grompp -f ../pre_NpT_posre.mdp -c min.gro -p system.top -r start.gro -o posre.tpr -n index.ndx
gmx mdrun -pin on -v -deffnm posre -s posre.tpr

gmx grompp -f ../pre_NpT.mdp -c posre.gro -p system.top -o eq.tpr -n index.ndx
gmx mdrun -pin on -v -deffnm eq -s eq.tpr
