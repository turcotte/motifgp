#!/bin/bash
# Executes a single timed run for MotifGP

#$ -S /bin/bash
#$ -cwd
#$ -o OUT/output
#$ -e OUT/error
#$ -q abaqus.q 
#$ -l qname=abaqus.q

echo "INPUTPATH=$1 ENGINE=$2 DATABASES=$3"
./scripts/merge_nef_and_tomtom.sh $1 $2 $3
