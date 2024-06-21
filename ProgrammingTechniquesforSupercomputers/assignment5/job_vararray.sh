#!/bin/bash -l
#
#SBATCH --gres=gpu:a100:1
#SBATCH --time=1:00:00
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module purge
module load nvhpc
rm cuda_vararraybenchmark || true
rm cudavararrop.txt || true
nvcc cuda_variablearray.cu time.c -o cuda_vararraybenchmark

value=1

# Start the while loop
while (( $(echo "$value <= 1000000000" | bc -l) ))
do
  # Print the current value
  
  # Multiply the value by 1.5
  value=$(echo "$value * 1.2" | bc -l)
  srun ./cuda_vararraybenchmark $value 24 3456 256
done

