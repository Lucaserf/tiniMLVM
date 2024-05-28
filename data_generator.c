#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define INPUT_SIZE 10
#define DATASET_SIZE 50

double synthetic_function(double *x)
{
    for (int k = 0; k < INPUT_SIZE; k++)
    {
        x[k] = (double)rand() / RAND_MAX;
    }

    return pow(x[0], 2) + 4 * pow(x[1], 2) + pow(x[2], 2) + pow(x[3], 6) + pow(x[4], 2) + pow(x[5], 3) + pow(x[6], 2) + pow(x[7], 3) + 6 * pow(x[8], 2) + pow(x[9], 2);
}

int main()
{
    double train_feature[INPUT_SIZE];
    double train_label;
    printf("x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,y\n");
    for (int i = 0; i < DATASET_SIZE; i++)
    {
        train_label = synthetic_function(train_feature);
        printf("%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf\n", train_feature[0], train_feature[1], train_feature[2], train_feature[3], train_feature[4], train_feature[5], train_feature[6], train_feature[7], train_feature[8], train_feature[9], train_label);
    }
    return 0;
}
