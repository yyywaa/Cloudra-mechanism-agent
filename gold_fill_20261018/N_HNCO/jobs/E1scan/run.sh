#!/bin/bash
set -x
cd "$(dirname "$0")" || exit 1
export g16root=/home/ly
export GAUSS_EXEDIR=/home/ly/g16
export GAUSS_SCRDIR="$PWD/scratch"
mkdir -p "$GAUSS_SCRDIR"
export PATH="/home/ly/g16:$PATH"
unset GAUSS_PDEF GAUSS_MDEF
/home/ly/g16/g16 E1_scan_manual.gjf E1_scan_manual.log
echo "G16 exit: $?"
grep -c "SCF Done" E1_scan_manual.log
tail -3 E1_scan_manual.log
