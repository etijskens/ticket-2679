#!/bin/bash
#
#SBATCH --ntasks=1 --cpus-per-task=64 --mem-per-cpu=1g
#SBATCH --time=00:05:00


module purge
module load calcua/2020a
module load Python


python Run_Parallel_Test.py

sleep 10
