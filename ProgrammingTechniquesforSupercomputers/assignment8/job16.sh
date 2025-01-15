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
icx -O3 -xHost -qopenmp -DLIKWID_PERFMON $LIKWID_INC parallelpi16.c time.c $LIKWID_LIB -llikwid -o parallelpi16
for ((t = 1 ; t < 37 ; t++)); do
    echo "Running benchmark for $t threads"
    srun --cpu-freq=1600000-1600000 likwid-perfctr -C S0:0-$(( t - 1 )) -g ENERGY -m ./parallelpi16 $t
done
for ((t = 37 ; t < 73 ; t++)); do
    echo "Running benchmark for $t threads"
    srun --cpu-freq=1600000-1600000 likwid-perfctr -C S0:0-35@S1:0-$(( t - 37 )) -g ENERGY -m ./parallelpi16 $t
done
zip pi16.zip pi16_*
rm pi16_*