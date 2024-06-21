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
icx -qopenmp -O1 -no-vec parallelpi.c time.c -o pi 
for ((i = 1 ; i < 37 ; i++)); do
    export OMP_NUM_THREADS=$i
    export OMP_PLACES=cores
    export OMP_PROC_BIND=close
    echo "Running benchmark for $i threads"
    srun --cpu-freq=2400000-2400000 ./pi $i
done
zip zippiomp.zip piomp*
rm -r piomp*