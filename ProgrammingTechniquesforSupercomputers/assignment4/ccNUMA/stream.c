#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <omp.h>
double getTimeStamp();
const double s = 1.00000000001;
int main(int argc, char** argv)
{   
    char* threads = argv[1];
    double wct_start,wct_end;
    float performance;
    char filename[32];
    snprintf(filename, sizeof(filename), "streamnuma%s.txt", threads);
    FILE *fptr;
    fptr = fopen(filename,"w");
    fprintf(fptr,"Loop_length,Threads,Total_WallTime,NIter,Performance(F/s)\n");
    int N;
    do
    {
        N = 10*1e8;
        //printf("%d,",N);
        double *a = malloc(N*sizeof(double));  
        double *b = malloc(N*sizeof(double));
        double *c = malloc(N*sizeof(double));

        if ((a == NULL) || (b == NULL) || (c == NULL))
            {
                printf("Memory not allocated.\n");
                exit(0);
            }
        else
            {   
                for (int i=0; i<N; i++)
                {
                    a[i] = 1.0;
                    b[i] = 1.0;
                    c[i] = 1.0;
                }
                #pragma omp parallel for
                for(int x=0; x<N; ++x) 
                {
                    x = x*1;
                }
                int NITER=1;
                do {
                    // time measurement
                    wct_start = getTimeStamp();

                    // repeat measurement often enough
                    for(int k=0; k<NITER; ++k) 
                    {
                        // This is the benchmark loop
                        #pragma omp parallel for
                        for(int i=0; i<N; ++i) 
                        {
                            // put loop body here: a[i] = ...
                            a[i] = b[i] + s * c[i];
                        }
                        // end of benchmark loop
                    if(a[N/2]<0.) printf("%lf",a[N/2]); // prevent compiler from eliminating loop
                    }
                    wct_end = getTimeStamp();
                    NITER = NITER*2;
                } while (wct_end-wct_start<0.2); // at least 100 ms

                NITER = NITER/2;
                performance = (2.0*NITER*N)/(wct_end-wct_start);
                //printf("Total walltime: %f, NITER: %d\n",wct_end-wct_start,NITER);
                fprintf(fptr,"%d,",N);
                fprintf(fptr,"%s,",threads);
                fprintf(fptr,"%f,",wct_end-wct_start);
                fprintf(fptr,"%d,",NITER);
                fprintf(fptr,"%f\n",performance);


            }
        free (a);
        free (b);
        free (c);
        N = N + 1000;
        
    } while (N < 100000000);
    fclose(fptr);

}


