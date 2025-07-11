#define _GNU_SOURCE
#include "genann.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <sys/time.h>

#define INPUT_SIZE 10

struct times_data times;

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
gettimens()
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * NSEC_PER_SEC + ts.tv_nsec;
}

int main()
{
    uint64_t start, end;

    times.timestamp = gettimens();
    times.train_time = 0;
    times.run_time = 0;

    printf("timestamp[ns],train_time[ns],train_inference_time[ns]\n");
    genann *ann = genann_init(INPUT_SIZE, 2, 64, 1);
    float learning_rate = 0.001;

    struct metadata data;
    FILE *file = fopen("./../data.csv", "r");
    // skip header
    char line[1024];
    char *check = fgets(line, 1024, file);

    for (;;)
    {
        if (get_data(file, &data) == -1)
            break;
        times.timestamp = gettimens();
        genann_train(ann, data.train_feature, data.label, learning_rate);
        printf("%ld,%ld,%ld\n", times.timestamp, times.train_time,
               times.run_time);
        // sleeping for 1ms minus the time taken to train the model
        int time_elapsed_us = (int)(gettimens() - times.timestamp);
        // fprintf(stderr, "time elapsed: %d\n", time_elapsed_us);

        // usleep(2000000 - time_elapsed_us);
    }

    genann_free(ann);
    return 0;
}