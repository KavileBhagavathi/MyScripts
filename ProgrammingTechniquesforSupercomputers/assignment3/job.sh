#!/bin/bash -l
#SBATCH --nodes=1 --time=01:00:00
#SBATCH --job-name=schonauer_benchmarking
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module purge
module load intel
rm -rf benchop512 || true
mkdir benchop512 
rm -rf benchop256 || true
mkdir benchop256 
rm -rf benchopSSE || true
mkdir benchopSSE

icx -O3 -xCORE-AVX512 -qopt-zmm-usage=high assignment3.c time.c -o schonauertriadavx512
echo "Compiling AVX512 successful"
icx -O3 -xCORE-AVX2 assignment3.c time.c -o schonauertriadavx256
echo "Compiling AVX256 successful"
icx -O3 -xSSE4.2 assignment3.c time.c -o schonauertriadSSE
echo "Compiling SSE successful"
echo "Running benchmarks"
#for ((i=0;i<3;i++)) do
#    srun --cpu-freq=2400000-2400000 ./a.out
#done 
srun --cpu-freq=2100000-2100000 ./schonauertriadavx512
scp *.txt benchop512/
cd benchop512
rm benchop512.zip || true
zip benchop512.zip *.txt
cd ..

srun --cpu-freq=2100000-2100000 ./schonauertriadavx256
scp *.txt benchop256/
cd benchop256
rm benchop256.zip || true
zip benchop256.zip *.txt
cd ..

srun --cpu-freq=2100000-2100000 ./schonauertriadSSE
scp *.txt benchopSSE/
cd benchopSSE
rm benchopSSE.zip || true
zip benchopSSE.zip *.txt
cd ..