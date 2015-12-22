#!/bin/bash

#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 8
#$ -o program.out
#$ -e program.err

python mctp.py

/home/hanu.nxhoai/pta/ctp/run.sh $@
