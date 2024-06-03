#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double getTimeStamp();
int main()
{
    double wct_start,wct_end;
    float performance;
    FILE *fptr;
    for(int filenum=1;filenum<6;filenum++) //Loop to run multiple benchmark runs and generate individual op files
    {
        char filename[sizeof "vectorupdate_benchmark00.txt"];
        sprintf(filename, "vectorupdate_benchmark%02d.txt", filenum);
        fptr = fopen(filename,"w");
        fprintf(fptr,"Array_Length,Stride,Total_WallTime,NIter,Performance(F/s)\n"); 
        int N = (int)pow(10,8); //Size of vector
        double s = 0.0;
        int M = 8;
        for (int n=0; M<=(int)pow(10,6); n++) //M is the stride size
        {   
            M = (int)8*pow((double) 1.2,n);
            double *a = malloc(N*sizeof(double));
            if (a==NULL)
            {
                printf("Memory not allocated.\n");
                exit(0);
            }
            else
            {
                for (int j=0; j<N; j++)
                {
                    a[j] = 1.0;
                }
                int NITER=1;
                do {
                    // time measurement
                    wct_start = getTimeStamp();

                    // repeat measurement often enough
                    for(int k=0; k<NITER; ++k) 
                    {
                        // This is the benchmark loop
                        for(int i=0; i<N; i+=M) 
                        {
                            // put loop body here: a[i] = ...
                            a[i] = s * a[i];
                        }
                        // end of benchmark loop
                    if(a[N/2]<0.) printf("%lf",a[N/2]); // prevent compiler from eliminating loop
                    }
                    wct_end = getTimeStamp();
                    NITER = NITER*2;
                } while (wct_end-wct_start<0.1); // at least 100 ms
                NITER = NITER/2;
                int stride_multiplier = (int)(N/M);
                performance = (1.0*NITER*stride_multiplier)/(wct_end-wct_start);
                //printf("Total walltime: %f, NITER: %d\n",wct_end-wct_start,NITER);
                fprintf(fptr,"%d,",N);
                fprintf(fptr,"%d,",M);
                fprintf(fptr,"%f,",wct_end-wct_start);
                fprintf(fptr,"%d,",NITER);
                fprintf(fptr,"%f\n",performance);
            }
            free(a);

        }
        fclose(fptr);
    }

}


