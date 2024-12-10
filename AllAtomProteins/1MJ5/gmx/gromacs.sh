#!/bin/bash

rm -f ./1mj5_all_hydrogen.pdb
sed 's/HG  SER/HG1 SER/g' 1mj5_charmm_named_his.pdb >> 1mj5_all_hydrogen.pdb
sed -i 's/HB2/HB3/g' 1mj5_all_hydrogen.pdb

gmx pdb2gmx -f 1mj5_all_hydrogen.pdb -water none -ff charmm36-jul2022 -o 1mj5_gmx.pdb
