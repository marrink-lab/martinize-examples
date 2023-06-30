#!/bin/bash

mkdir EN_region
cd EN_region
martinize2 -f ../AF-A0A7Y6D765-F1-model_v3.pdb -o test.top -dssp dssp -p backbone -ff martini3001 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -scfix -cys auto -ignore HOH -eunit 20:320
cd ../
mkdir EN_all
cd EN_all
martinize2 -f ../AF-A0A7Y6D765-F1-model_v3.pdb -o test.top -dssp dssp -p backbone -ff martini3001 -elastic -resid input -ef 700.0 -el 0.5 -eu 0.9 -ea 0 -ep 0 -scfix -cys auto -ignore HOH 
