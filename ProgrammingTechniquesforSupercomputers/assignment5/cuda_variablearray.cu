#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <time.h>
double getTimeStamp()
    {
        struct timespec ts;
        clock_gettime(CLOCK_MONOTONIC, &ts);
        return (double)ts.tv_sec + (double)ts.tv_nsec * 1.e-9;
    }

void initoncpu(double *a_src, size_t size)
    {
        for(size_t i=0; i<size; i++){
           a_src[i] = 1.0;
        }
    }

void checkOnCPU(double *a_dest, size_t numberofelements) 
    {
        for (size_t i = 0; i < numberofelements; ++i)
        {
        assert(2.0 == a_dest[i]);
        }
        printf("Assertion success!\n");
    }

__global__ void cudakernel(double *d_src, double *d_dest, size_t numberofelements)
    {
        size_t start = blockIdx.x * blockDim.x + threadIdx.x;
        size_t stride = gridDim.x * blockDim.x;
        for (size_t i = start; i < numberofelements; i=i+stride)
        {
            d_dest[i] = d_src[i] + 1.0;
        }
    }

__global__ void cudakernelwarmup(double *d_src, double *d_dest, size_t numberofelements)
    {
        size_t start = blockIdx.x * blockDim.x + threadIdx.x;
        size_t stride = gridDim.x * blockDim.x;
        for (size_t i = start; i < numberofelements; i=i+stride)
        {
            d_dest[i] = 1.0;
        }
    }

int main(int argc, char **argv0)
    {
    double kernel_wct_start,kernel_wct_end,hosttodev_start,hosttodev_end,devtohost_start,devtohost_end;
    size_t numberofelements = atoi(argv0[1]);
    size_t kernel_reps = atoi(argv0[2]);
    size_t cuda_blocks = atoi(argv0[3]);
    size_t cuda_threads_per_block = atoi(argv0[4]);
    FILE *fptr;
    fptr = fopen("cudavararrop.txt","a");
    if(cuda_threads_per_block==1)
    {
        fprintf(fptr,"Number_of_elements,Kernel_reps,Cuda_blocks,Threads_per_block,T_hosttodev,T_exec,T_devtohost,Bw_HosttoDev,Bw_DevtoHost,Bw_execution\n");
    }
    size_t size = sizeof(double)*numberofelements;
    //allocate host arrays
    double *a_src, *a_dest;
    if (cudaMallocHost(&a_src, size) != cudaSuccess || cudaMallocHost(&a_dest, size) != cudaSuccess) 
        {
            printf("Failed to allocate host memory.\n");
            return 1;
        }
    else
        {
            printf("Allocated host memory.\n");
        }
    // allocate _device_ arrays
    double *d_src, *d_dest;
    if (cudaMalloc(&d_src, size) != cudaSuccess || cudaMalloc(&d_dest, size) != cudaSuccess) 
        {
            printf("Failed to allocate device memory.\n");
            return 1;
        }
    else
        {
            printf("Allocated device memory.\n");
        }
    //initialize data on CPU
    initoncpu(a_src,numberofelements);
    hosttodev_start = getTimeStamp();
    cudaMemcpy(d_src, a_src, size, cudaMemcpyHostToDevice);
    hosttodev_end = getTimeStamp();
        
    auto numBlocks = atoi(argv0[3]);
    auto numThreadsPerBlock = atoi(argv0[4]);
    
    cudakernelwarmup<<<numBlocks, numThreadsPerBlock>>>(d_src, d_dest, numberofelements);

    cudaDeviceSynchronize();
    kernel_wct_start = getTimeStamp();
    for (int k=0;k<kernel_reps;k++)
    {
    cudakernel<<<numBlocks, numThreadsPerBlock>>>(d_src, d_dest, numberofelements);
    }
    cudaDeviceSynchronize();
    kernel_wct_end = getTimeStamp();

    devtohost_start = getTimeStamp();
    cudaMemcpy(a_dest, d_dest, size, cudaMemcpyDeviceToHost);
    devtohost_end = getTimeStamp();

    checkOnCPU(a_dest, numberofelements);
    cudaFree(a_src);
    cudaFree(a_dest);
    cudaFreeHost(d_src);
    cudaFreeHost(d_dest);
    /*
    printf("Execution time: %f seconds\n", kernel_wct_end - kernel_wct_start);
    printf("Host to device time: %f seconds\n", hosttodev_end - hosttodev_start);
    printf("Device to host time: %f seconds\n", devtohost_end - devtohost_start);
    */
    double Bw_HosttoDev = size/(hosttodev_end - hosttodev_start);
    double Bw_DevtoHost = size/(devtohost_end - devtohost_start);
    double Bw_execution = (size*2*16)/(kernel_wct_end - kernel_wct_start);
    fprintf(fptr,"%d,",numberofelements);
    fprintf(fptr,"%d,",kernel_reps);
    fprintf(fptr,"%d,",cuda_blocks);
    fprintf(fptr,"%d,",cuda_threads_per_block);
    fprintf(fptr,"%f,",hosttodev_end - hosttodev_start);
    fprintf(fptr,"%f,",kernel_wct_end - kernel_wct_start);
    fprintf(fptr,"%f,",devtohost_end - devtohost_start);
    fprintf(fptr,"%f,",Bw_HosttoDev);
    fprintf(fptr,"%f,",Bw_DevtoHost);
    fprintf(fptr,"%f\n",Bw_execution);
    return 0;
    }
