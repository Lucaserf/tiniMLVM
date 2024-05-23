#include "genann.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define EPOCHS 100
#define TRAINING_BATCH 1000
#define TESTING_BATCH 100
#define INPUT_SIZE 10
#define TEST_SIZE_PRINT 5

double synthetic_function(double *x)
{
    for (int k = 0; k < INPUT_SIZE; k++)
    {
        x[k] = (double)rand() / RAND_MAX;
    }

    return pow(x[0], 2) + 4 * pow(x[1], 2) + pow(x[2], 2) + pow(x[3], 6) + pow(x[4], 2) + pow(x[5], 3) + pow(x[6], 2) + pow(x[7], 3) + 6 * pow(x[8], 2) + pow(x[9], 2);
}

struct times_data times;

int main()
{
    times.timestamp = time(NULL);
    times.train_time = 0;
    times.run_time = 0;

    printf("timestamp,train_time,train_inference_time\n");
    printf("%ld,%lf,%lf\n", times.timestamp, times.train_time, times.run_time);
    genann *ann = genann_init(INPUT_SIZE, 2, 64, 1);
    float learning_rate = 0.001;
    double train_feature[INPUT_SIZE];
    double train_label[1];
    for (int i = 0; i < EPOCHS; i++)
    {
        train_label[0] = synthetic_function(train_feature);
        times.timestamp = time(NULL);
        genann_train(ann, train_feature, train_label, learning_rate);
        printf("%ld,%lf,%lf\n", times.timestamp, times.train_time,
               times.run_time);
    }

    genann_free(ann);
    return 0;
}