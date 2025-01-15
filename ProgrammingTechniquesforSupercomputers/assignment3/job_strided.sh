#!/bin/bash -l
#SBATCH --nodes=1 --time=01:00:00
#SBATCH --job-name=vectorupdate_benchmarking
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module purge
module load intel
rm -rf vectorstride || true
mkdir vectorstride 
icx -O3 -xHost -fno-alias assignment3strided.c time.c -o vectorstrided
echo "Compiling successful"
echo "Running benchmarks"
#for ((i=0;i<3;i++)) do
#    srun --cpu-freq=2400000-2400000 ./a.out
#done 
srun --cpu-freq=2100000-2100000 ./vectorstrided
scp vectorupdate_benchmark* vectorstride/
cd vectorstride
rm vectorupdate.zip || true
zip vectorupdate.zip *.txt
cd ..
rm vectorupdate_benchmark*