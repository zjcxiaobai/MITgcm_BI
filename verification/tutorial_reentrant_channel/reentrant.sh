#!/bin/bash -l
#SBATCH --mail-type=ALL
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=160
#SBATCH -t 12:00:00
#SBATCH -J reentrant
cd $SLURM_SUBMIT_DIR

module load StdEnv/2023 intel/2023.2.1 intelmpi/2021.9.0

cd run/

mpirun -np 1600 ./mitgcmuv

