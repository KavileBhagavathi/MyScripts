#!/bin/bash -l
#
#SBATCH --gres=gpu:a100:1
#SBATCH --time=1:00:00
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module purge
module load nvhpc
rm cuda_varthreadsbenchmark || true
rm cudavarthreadsop.txt || true
nvcc cuda_variablethreads.cu time.c -o cuda_varthreadsbenchmark
for threads in {1..1024} 
do
    srun ./cuda_benchmark 32000000 16 864 $threads
done 
