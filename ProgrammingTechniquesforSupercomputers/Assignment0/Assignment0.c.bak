#include <stdio.h>
#include <math.h>

float slices;
double sum;
float delta_x;

int main(){
    slices = 1000000000.0;
    sum = 0;
    delta_x = 1.0/slices;

    for (int i=0; i<slices; i++){
        double x = (i+0.5)*delta_x;
        sum = sum + 4*sqrt(1.0-x*x);
    }
    double Pi = sum * delta_x;
    printf("The value of delta_x is %.9f\n",delta_x);
    printf("The value of pi is %f\n",Pi);
}
