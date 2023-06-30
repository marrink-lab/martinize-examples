#!/bin/bash
set -e 
for i in {0..5}
do
mkdir run$i
cd run$i

cat >> system.top << END
; Include forcefield parameters
#include "../martini_v3.0.0.itp"
#include "../martini_v3.0.0_ions_v1.itp"
#include "../martini_v3.0.0_solvents_v1.itp"
#include "molecule_0.itp"

[ moleculetype ]
molecule_1 1

[ atoms ]
1 TC5 165 BENZ R1 1 0.0 
2 TC5 165 BENZ R2 2 0.0 
3 TC5 165 BENZ R3 3 0.0 

[ constraints ]
3 1 1 0.290
1 2 1 0.290
3 2 1 0.290

#ifdef DPOSRES
[ position_restraints ]
1 1 1000 1000 1000
2 1 1000 1000 1000
3 1 1000 1000 1000
#endif

[ system ]
; Name
Title

[ molecules ]
; Compound	#mols
molecule_0  	   1
molecule_1  	   1
END

martinize2 -f ../aa.gro -x cg.pdb -o temp.top -dssp dssp -p backbone -ff martini3001 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -scfix -cys auto

gmx solvate -cp cg.pdb  -cs ../W.gro   -o start.gro -radius 0.21 -box 10 10 10  >& solv.out
nsol=$(grep "1 atoms" solv.out | awk '{print $5}')
echo "W ${nsol}" >> system.top


gmx grompp -f ../min.mdp -c start.gro -p system.top -maxwarn 1 -o ion.tpr -r start.gro

echo "W" | gmx genion -s ion.tpr -p system.top -conc 0.150 -neutral -o ion.gro

echo -e "keep 1 \n name 0 SOLU \n r W | r NA | r CL | r BENZ \n name 1 SOLV \n q \n" | gmx make_ndx -f ion.gro

gmx grompp -f ../min.mdp -c ion.gro -p system.top -maxwarn 1 -o min.tpr -r start.gro
gmx mdrun -v -deffnm min -nsteps 2000

gmx grompp -f ../pre_NpT_posre.mdp -c min.gro -p system.top -r start.gro -o posre.tpr -n index.ndx
gmx mdrun -pin on -v -deffnm posre -s posre.tpr

gmx grompp -f ../pre_NpT.mdp -c posre.gro -p system.top -o eq.tpr -n index.ndx
gmx mdrun -pin on -v -deffnm eq -s eq.tpr
cd ../
done
