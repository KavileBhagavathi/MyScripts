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
icx -O3 -xHost -qopenmp -DLIKWID_PERFMON $LIKWID_INC parallelpi24.c time.c $LIKWID_LIB -llikwid -o parallelpi24
for ((t = 1 ; t < 37 ; t++)); do
    echo "Running benchmark for $t threads"
    srun --cpu-freq=2400000-2400000 likwid-perfctr -C S0:0-$(( t - 1 )) -g ENERGY -m ./parallelpi24 $t
done
for ((t = 37 ; t < 73 ; t++)); do
    echo "Running benchmark for $t threads"
    srun --cpu-freq=2400000-2400000 likwid-perfctr -C S0:0-35@S1:0-$(( t - 37 )) -g ENERGY -m ./parallelpi24 $t
done
zip pi24.zip pi24_*
rm pi24_*