#!/bin/bash

martinize2 -f PE.gro -ff martini2_CNP -x PE.pdb -o topol.top -ff-dir ../forcefields/ -map-dir ../mappings/ -from uff -ignh -maxwarn 3
