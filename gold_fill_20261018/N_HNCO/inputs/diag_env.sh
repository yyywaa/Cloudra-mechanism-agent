#!/bin/bash
echo "PATH=$PATH"
echo "which g16: $(command -v g16 || echo MISSING)"
ls -l /home/ly/g16/g16 2>&1 | head -2
ls -l /home/ly/g16/*.exe 2>&1 | head -3
echo "GAUSS env: ${g16root:-unset} ${GAUSS_EXEDIR:-unset}"
hostname; nproc
