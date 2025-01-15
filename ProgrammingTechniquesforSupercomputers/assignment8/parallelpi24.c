#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#ifdef LIKWID_PERFMON
#include <likwid-marker.h>
#else
#define LIKWID_MARKER_INIT
#define LIKWID_MARKER_THREADINIT
#define LIKWID_MARKER_SWITCH
#define LIKWID_MARKER_REGISTER(regionTag)
#define LIKWID_MARKER_START(regionTag)
#define LIKWID_MARKER_STOP(regionTag)
#define LIKWID_MARKER_CLOSE
#define LIKWID_MARKER_GET(regionTag, nevents, events, time, count)
#endif
double getTimeStamp();

int main(int argc, char** argv){
    char* cores = argv[1];
    char* bashiter = argv[2];
    char filename[32];
    snprintf(filename, sizeof(filename), "pi24_%s.txt", cores);
    FILE *fptr;
    fptr = fopen(filename,"w");
    fprintf(fptr,"#Cores,Total_WallTime,Performance,Pi\n");
    long int slices;
    double sum;
    float delta_x;
    double wcTime,wcTimeStart,wcTimeEnd;
    double x = 1.0;
    float performance;
    slices = 2*1e9;
    sum = 0.0;
    delta_x = 1.0/slices;
    
    #pragma omp parallel for
    for (int k=0; k<1000; k++)
    {
        x = x*1.0;
    }
    LIKWID_MARKER_INIT;
#pragma omp parallel
{
    LIKWID_MARKER_REGISTER("pi");
}
    wcTimeStart = getTimeStamp();
#pragma omp parallel 
{
    LIKWID_MARKER_START("pi");
    #pragma omp for reduction(+:sum) private(x)
    for (int i=0; i<slices; i++){
        double x = (i+0.5)*delta_x;
        sum = sum + 4*sqrt(1.0-x*x);
    }
    LIKWID_MARKER_STOP("pi");
}
    wcTimeEnd = getTimeStamp();
    LIKWID_MARKER_CLOSE;
    wcTime = wcTimeEnd - wcTimeStart;
    double Pi = sum * delta_x;
    performance = (7.0*slices)/(wcTimeEnd-wcTimeStart);
    fprintf(fptr,"%s,",cores);
    fprintf(fptr,"%.4lf,",wcTime);
    fprintf(fptr,"%f,",performance);
    fprintf(fptr,"%.10f\n",Pi);
    return 0;
}
