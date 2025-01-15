#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE
#SBATCH --job-name=parallelpi
#SBATCH --constraint=hwperf

unset SLURM_EXPORT_ENV
rm *.txt
module purge
module load intel
module load likwid
icx -O3 -xHost -qopenmp histo_c_scaled.c time.c -o histo_scale
#icx -O3 -xHost -qopenmp histo_c_unscaled.c time.c -o histo_unscale
for ((t = 1 ; t < 19 ; t++)); do
    echo "Running benchmark for $t threads"
    srun --cpu-freq=2000000-2000000 likwid-pin -S -c S0:0-$(( t - 1 )) ./histo_scale >> histo_parallelfor$t.txt
    #srun --cpu-freq=2000000-2000000 likwid-pin -S -c S0:0-$(( t - 1 )) ./histo_unscale >> histo_unscale$t.txt
done
