#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE
#SBATCH --job-name=parallelpi
unset SLURM_EXPORT_ENV

module purge
module load intel
module load likwid
icx -O3 -xAVX -qopenmp parallelpi.c time.c -o pi 
for ((j = 1 ; j < 11 ; j++)); do
    for ((i = 1 ; i < 5 ; i++)); do
        export OMP_NUM_THREADS=$i
        export OMP_PLACES=cores
        export OMP_PROC_BIND=close
        echo "Running benchmark for $i threads"
        srun --cpu-freq=2000000-2000000 ./pi $i $j --constraint=hwperf
    done
done
zip zippiompo3.zip piomp*
rm -r piomp*