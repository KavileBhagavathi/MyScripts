#!/bin/bash -l
#SBATCH --partition=spr1tb
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE
#SBATCH --job-name=streamtriadomp

unset SLURM_EXPORT_ENV

module purge
module load intel 
module load likwid
icx -O3 -xHost -fno-alias DAXPY.c time.c -o DAXPY
for m in `seq 0 7`; do
    for c in `seq 0 7`; do
        echo -n $c " " $m " "; \
        srun --cpu-freq=2000000-2000000 numactl --membind=$m likwid-pin -c N:$((c*1))-$(((c+1)*1-1)) ./DAXPY
    done
done