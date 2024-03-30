#!/bin/bash

martinize2 -f CRE.gro -ff martini2_CNP -x CRE_cg.pdb -o topol.top -ff-dir ../forcefields/ -map-dir ../mappings/ -from uff -ignh -maxwarn 3
