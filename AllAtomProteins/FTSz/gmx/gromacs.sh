#!/bin/bash

rm -f FTSz_clean.pdb
sed 's/HG  SER A/HG1 SER A/g' ../result/out_with_h.pdb >> FTSz_clean.pdb
sed -i 's/HG  CYS A/HG1 CYS A/g' FTSz_clean.pdb

time gmx pdb2gmx -f FTSz_clean.pdb -water none -ff charmm36-jul2022 -o FTSz_gmx.pdb
