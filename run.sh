#!/bin/bash

#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 48
#$ -o mctp1.out
#$ -e mctp1.err

#$ -t 1-48

python run_vast.py mctp1 input.$SGE_TASK_ID output.$SGE_TASK_ID


