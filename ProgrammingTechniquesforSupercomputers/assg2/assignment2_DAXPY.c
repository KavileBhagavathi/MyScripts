#include <stdio.h>
#include <math.h>
#include <stdlib.h>
double getTimeStamp();

const double s = 1.00000000001;
int main()
{
    double wct_start,wct_end;
    float performance;
    FILE *fptr;
    fptr = fopen("daxpy_benchmarkop.txt","w");
    fprintf(fptr,"Array_Length,Total_WallTime,NIter,Performance(F/s)\n");
    for(int m=8;m<=44;m++)
    {
        int N = (int)pow((double) 1.5,m);
        //printf("%d,",N);
        double *a = malloc(N*sizeof(double));  
        double *b = malloc(N*sizeof(double));
        // double *d = malloc(N*sizeof(double));

        if ((a == NULL) || (b == NULL))
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
		        }

                int NITER=1;
                do
	       	    {
                    // time measurement
                    wct_start = getTimeStamp();

                    // repeat measurement often enough
                    for(int k=0; k<NITER; ++k) 
                    {
                        // This is the benchmark loop
                        for(int i=0; i<N; ++i) 
                        {
                            // put loop body here: a[i] = ...
                            a[i] = s*b[i] + a[i];
                        }
                        // end of benchmark loop
                    if(a[N/2]<0.) printf("%lf",a[N/2]); // prevent compiler from eliminating loop
                    }
                    wct_end = getTimeStamp();
                    NITER = NITER*2;
                } while (wct_end-wct_start<0.1); // at least 100 ms

                NITER = NITER/2;
                performance = (2.0*NITER*N)/(wct_end-wct_start);
                //printf("Total walltime: %f, NITER: %d\n",wct_end-wct_start,NITER);
                fprintf(fptr,"%d,",N);
                fprintf(fptr,"%f,",wct_end-wct_start);
                fprintf(fptr,"%d,",NITER);
                fprintf(fptr,"%f\n",performance);


            }
        free (a);
        free (b);
        
    }
    fclose(fptr);

}


