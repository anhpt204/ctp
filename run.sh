#!/bin/bash

#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 8
#$ -o mctp.out
#$ -e mctp.err

#$ -t 1-72

python run_vast.py mctp input.$SGE_TASK_ID output.$SGE_TASK_ID


