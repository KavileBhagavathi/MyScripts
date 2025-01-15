#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=05:00:00
#SBATCH --export=NONE
#SBATCH --job-name=raytrace

unset SLURM_EXPORT_ENV
rm output.txt || true
module purge
module load intel
icx -O3 -xHost -qopenmp raytrace.c time.c -o raytraceorig 

export OMP_NUM_THREADS=36
export OMP_PLACES=cores
export OMP_PROC_BIND=close
echo "Running benchmark for 36 threads"
for tiles in 1 2 3 10 12 15 30 40 50 60 75 100 120 125 150 200 250 300 375 500 600 625 750 1000 1250 1500 1875 2500 3000
do
    echo running tile size $tiles
    srun --cpu-freq=2000000-2000000 ./raytraceorig 15000 $tiles >> output.txt
done 


 
