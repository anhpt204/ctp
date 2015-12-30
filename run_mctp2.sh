#!/bin/bash

#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 8
#$ -o mctp2.out
#$ -e mctp2.err

#$ -t 1-96

python run_vast.py mctp2 input.$SGE_TASK_ID output.$SGE_TASK_ID


