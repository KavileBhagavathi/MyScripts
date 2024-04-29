#include <stdio.h>
#include <math.h>
#include "timing.h"

double getTimeStamp()
{
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (double)ts.tv_sec + (double)ts.tv_nsec * 1.e-9;
}


int main(){
    float slices;
    double sum;
    float delta_x;
    double wcTime,wcTimeStart,wcTimeEnd;
    
    slices = 1000000000.0;
    sum = 0;
    delta_x = 1.0/slices;
    wcTimeStart = getTimeStamp();
    for (int i=0; i<slices; i++){
        double x = (i+0.5)*delta_x;
        sum = sum + 4*sqrt(1.0-x*x);
    }
    wcTimeEnd = getTimeStamp();
    wcTime = wcTimeEnd - wcTimeStart;
    double Pi = sum * delta_x;
    /*printf("Pi is %f\n",Pi);*/
    printf("Walltime: %.3lf s\n",wcTime);
    return 0;
}
