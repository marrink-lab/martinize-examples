for dir in $(ls)
do

cd ${dir}
cat >> system.top << END
#include "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/charmm36-jul2022-patched.ff/forcefield.itp"
#include "molecule_0.itp"

[ system ]
protein

[ molecules ]
molecule_0 1
END
cd ../ 
done
