#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE
#SBATCH --job-name=parallelpi
#SBATCH --constraint=hwperf
unset SLURM_EXPORT_ENV
module purge
module load intel
module load likwid
icx -O1 -no-vec -qopenmp parallelpi.c time.c -o pi 
srun --cpu-freq=2000000-2000000 likwid-perfctr -g DATA -C 0 ./pi
zip zippiompo3.zip piomp*
rm -r piomp*