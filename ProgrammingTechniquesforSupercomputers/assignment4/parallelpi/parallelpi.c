#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
double getTimeStamp();

int main(int argc, char** argv){
    char* cores = argv[1];
    char filename[32];
    snprintf(filename, sizeof(filename), "piompperf%s.txt", cores);
    FILE *fptr;
    fptr = fopen(filename,"w");
    fprintf(fptr,"#Cores,Total_WallTime,Pi\n");
    long int slices;
    double sum;
    float delta_x;
    double wcTime,wcTimeStart,wcTimeEnd;
    double x = 1.0;
    slices = 2*1e9;
    sum = 0.0;
    delta_x = 1.0/slices;
    
    #pragma omp parallel for
    for (int k=0; k<1000; k++)
    {
        x = x*1.0;
    }

    wcTimeStart = getTimeStamp();
    #pragma omp parallel for reduction(+:sum)
    for (int i=0; i<slices; i++){
        double x = (i+0.5)*delta_x;
        sum = sum + 4*sqrt(1.0-x*x);
    }
    wcTimeEnd = getTimeStamp();
    wcTime = wcTimeEnd - wcTimeStart;
    double Pi = sum * delta_x;
    fprintf(fptr,"%s,",cores);
    fprintf(fptr,"%.4lf,",wcTime);
    fprintf(fptr,"%.10f\n",Pi);
    return 0;
}
