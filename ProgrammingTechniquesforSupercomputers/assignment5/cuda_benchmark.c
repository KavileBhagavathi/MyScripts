#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
double getTimeStamp()
{
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (double)ts.tv_sec + (double)ts.tv_nsec * 1.e-9;
}

void initoncpu(double *a_src, size_t size)
    {
        for(int i=0; i<size; i++){
            a_src[i] = 1.0;
        }
    }
void checkOnCPU(double *a_dest, size_t numberofelements) {
        for (size_t i = 0; i < numberofelements; ++i)
        assert(2.0 == a_dest[i]);
    }
__global__ void cudakernel(double *d_src, double *d_dest, size_t numberofelements)
    {
        size_t start = blockIdx.x * blockDim.x + threadIdx.x;
        size_t stride = gridDim.x * blockDim.x;
        if (size_t i = start; i < elements; i=i+stride )
        {
            d_dest[i] = d_src[i] + 1.0;
        }
    }


int main(int argc, char **argv0){
    if (argc < 2)
    {
        printf("No arguments passed. Try again!\n");
        return 1;
    }
    else
    {
        size_t numberofelements = atoi(argv0[1]);
        size_t kernel_reps = atoi(argv0[2]);
        size_t cuda_blocks = atoi(argv0[3]);
        size_t cuda_threads_per_block = atoi(argv0[4]);
        printf("number of elements: %d\n",numberofelements);
        printf("kernel_reps: %d\n",kernel_reps);
        printf("cuda_blocks: %d\n",cuda_blocks);
        printf("cuda_threads: %d\n",cuda_threads_per_block);
        size_t size = sizeof(double)*numberofelements;
        //allocate host arrays
        double *a_src, *a_dest;
        cudaMallocHost(&a_src, size);
        cudaMallocHost(&a_dest, size);
        // allocate _device_ arrays
        double *d_src, *d_dest;
        cudaMalloc(&d_src, size);
        cudaMalloc(&d_dest, size);

        //initialiye data on CPU
        initoncpu(a_src,size);
        cudaMemcpy(d_src, a_src, size, cudaMemcpyHostToDevice);

        auto numBlocks = atoi(argv0[3]);
        auto numThreadsPerBlock = atoi(argv0[4]);
        copyOnGPU<<<numBlocks, numThreadsPerBlock>>>(d_src, d_dest, numberofelements);
        cudaDeviceSynchronize();
        cudaMemcpy(a_dest, d_dest, size, cudaMemcpyDeviceToHost);
        checkOnCPU(a_dest, numberofelements);

        cudaFree(d_src);
        cudaFree(d_src);
        cudaFreeHost(a_src);
        cudaFreeHost(a_dest);
    }


    return 0;
}