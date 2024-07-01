#define _GNU_SOURCE
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>

// include tensorflow lite
#include "tensorflow/lite/c/c_api.h"

#define INPUT_SIZE 10

struct times_data
{
    long long timestamp;
    int run_time;
} times;

struct metadata
{
    double train_feature[INPUT_SIZE];
    double label[1];
};

// training from streaming data coming from dataset data.csv
int get_data(FILE *file, struct metadata *data)
{
    char line[1024];
    char *check = fgets(line, 1024, file);
    if (check == NULL)
        return -1;

    char *token = strtok(line, ",");
    for (int i = 0; i < INPUT_SIZE; i++)
    {
        data->train_feature[i] = atof(token);
        token = strtok(NULL, ",");
    }

    data->label[0] = atof(token);

    return 0;
}

#define NSEC_PER_SEC 1000000000LL

long long
ts2timestamp(struct timespec *tv)
{
    return tv->tv_sec * NSEC_PER_SEC + tv->tv_nsec;
}

int main()
{
    uint64_t start, end;

    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);

    times.timestamp = ts2timestamp(&ts);
    times.run_time = 0;

    printf("timestamp[ns],train_time[ns],train_inference_time[ns]\n");

    // load tflite model

    // get input tensor
    struct metadata data;
    FILE *file = fopen("./../data.csv", "r");
    // skip header
    char line[1024];
    char *check = fgets(line, 1024, file);

    for (;;)
    {
        clock_gettime(CLOCK_MONOTONIC, &ts);

        if (get_data(file, &data) == -1)
            break;
        times.timestamp = ts2timestamp(&ts);
        // set input as data.train_feature

        times.run_time = (int)(ts2timestamp(&ts) - times.timestamp) / 1000;

        printf("%lld,%d\n", times.timestamp, times.run_time);
        // sleeping for 1ms minus the time taken to train the model
        clock_gettime(CLOCK_MONOTONIC, &ts);

        // fprintf(stderr, "time elapsed: %d\n", time_elapsed_us);

        // usleep(2000000 - time_elapsed_us);
    }

    return 0;
}