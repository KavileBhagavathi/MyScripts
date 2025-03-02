#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE
#SBATCH --job-name=raytrace

unset SLURM_EXPORT_ENV

module purge
module load intel
icx -O3 -xHost -qopenmp raytrace_c.c time.c -o raytrace100 
for ((i = 1 ; i < 73 ; i++)); do
    export OMP_NUM_THREADS=$i
    export OMP_PLACES=cores
    export OMP_PROC_BIND=close
    echo "Running benchmark for $i threads"
    srun --cpu-freq=2400000-2400000 ./raytrace100 15000 100 $i
done
zip raytrace500op.zip raytrace100_core*
rm -r raytrace500_core*