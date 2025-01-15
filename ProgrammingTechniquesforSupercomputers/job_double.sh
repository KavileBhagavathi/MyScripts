#!/bin/bash -l
#SBATCH --nodes=1 --time=00:30:00
#SBATCH --job-name=pical_O3_avx512
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module load intel
icx -O3 -xCORE-AVX512 -qopt-zmm-usage=high assignment1.c time.c  
echo "double precision run"
for ((i=0;i<5;i++)) do
    srun --cpu-freq=2400000-2400000 ./a.out
done 
