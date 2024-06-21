#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE
#SBATCH --job-name=streamtriadomp

unset SLURM_EXPORT_ENV

module purge
module load intel
module load likwid
icx -qopenmp -O3 -xHost -fno-alias stream.c time.c -o streamnuma
for threads in {0..17}
do
    #export OMP_NUM_THREADS=$threads 
    #export OMP_PLACES=cores
    #export OMP_PROC_BIND=close
    echo "Running omp benchmark for $threads threads"
    srun --cpu-freq=2000000-2000000 likwid-pin -c M0:0-$ ./cstreamnuma $threads
done
zip zstreamnuma.zip streamnuma*
