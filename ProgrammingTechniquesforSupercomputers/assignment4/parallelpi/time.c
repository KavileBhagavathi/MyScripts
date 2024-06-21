#include "timing.h"

double getTimeStamp()
{
  struct timespec ts;
  clock_gettime(CLOCK_MONOTONIC, &ts);
  return (double)ts.tv_sec + (double)ts.tv_nsec * 1.e-9;
}

double getTimeResolution()
{
  struct timespec ts;
  clock_getres(CLOCK_MONOTONIC, &ts);
  return (double)ts.tv_sec + (double)ts.tv_nsec * 1.e-9;
}

double getTimeStamp_()
{
  return getTimeStamp();
}

double gettimestamp_()
{
  return getTimeStamp();
}



/* old-style timing function (outdated) 
void timing(double* wcTime, double* cpuTime)
{
   struct timeval tp;
   struct rusage ruse;

   gettimeofday(&tp, NULL);
   *wcTime=(double) (tp.tv_sec + tp.tv_usec/1000000.0); 
  
   getrusage(RUSAGE_SELF, &ruse);
   *cpuTime=(double)(ruse.ru_utime.tv_sec+ruse.ru_utime.tv_usec / 1000000.0);
}

void timing_(double* wcTime, double* cpuTime) {
   timing(wcTime, cpuTime);
}

*/
