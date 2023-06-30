#!/bin/bash

for i in {0..5}
do
mkdir run$i
cd run$i
cp -f ../system.top ./

martinize2 -f ../aa.gro -x cg.pdb -o temp.top -dssp dssp -p backbone -ff martini3001 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -scfix -cys auto
polyply gen_coords -p system.top -c cg.pdb -res W NA CL -o start.gro -dens 1000 -name protein

echo -e "keep 1 \n name 0 SOLU \n r W | r NA | r CL | r BENZ \n name 1 SOLV \n q \n" | gmx make_ndx -f start.gro

gmx grompp -f ../min.mdp -c start.gro -p system.top -maxwarn 1 -o min.tpr -r start.gro
gmx mdrun -v -deffnm min -nsteps 2000

gmx grompp -f ../pre_NpT_posre.mdp -c min.gro -p system.top -r start.gro -o posre.tpr -n index.ndx
gmx mdrun -pin on -v -deffnm posre -s posre.tpr

gmx grompp -f ../pre_NpT.mdp -c posre.gro -p system.top -o eq.tpr -n index.ndx
gmx mdrun -pin on -v -deffnm eq -s eq.tpr
cd ../
done
