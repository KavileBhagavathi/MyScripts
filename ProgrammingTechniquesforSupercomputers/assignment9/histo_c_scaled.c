#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "timing.h"
#include <omp.h>
  int main() {
  unsigned int main_seed = 1;
  long main_hist[16], n;
  double wcstart, wcend, ct;
  n = 2 * pow(10, 9);
  
  for (int i = 0; i < 16; ++i) { // Initialize main hist
    main_hist[i] = 0;
  }

  wcstart = getTimeStamp();
  #pragma omp parallel shared(n, main_hist) reduction(+:main_hist[:16])
  {
    unsigned int thread_seed = main_seed + omp_get_thread_num(); /*need to create thread specific seeds otherwise pointless*/
    long thread_hist[16] = {0}; /*ach thread has its own local histogram*/

    #pragma omp for
    for (long j = 0; j < n; ++j) 
    {
      thread_hist[rand_r(&thread_seed) & 0xf]++;
    }
    
    #pragma omp for
    for (int i = 0; i < 16; ++i) 
    {
      main_hist[i] += thread_hist[i];
    }
    
  }
  wcend = getTimeStamp();

  for(int i=0; i<16; ++i) {
    printf("hist[%d]=%ld\n",i,main_hist[i]);
  }
  printf("Cycles: %lf cycles\n",(wcend-wcstart)*2*pow(10, 9));

  return 0;
}

