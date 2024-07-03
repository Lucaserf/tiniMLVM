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

#define INPUT_SIZE 784
#define OUTPUT_SIZE 10

struct times_data
{
    int64_t timestamp;
    int64_t run_time;
} times;

struct metadata
{
    double train_feature[INPUT_SIZE];
    double label[OUTPUT_SIZE];
};

// training from streaming data coming from dataset data.csv
int get_data(FILE *file, struct metadata *data)
{
    // line with 784 doubles separated by commas
    char line[INPUT_SIZE * 24 * 4];
    char *check = fgets(line, INPUT_SIZE * 24 * 4, file);
    if (check == NULL)
        return -1;

    char *token = strtok(line, ",");
    for (int i = 0; i < INPUT_SIZE; i++)
    {
        data->train_feature[i] = atof(token);
        token = strtok(NULL, ",");
    }

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

int main(int argc, char *argv[])
{
    uint64_t start, end;
    printf("timestamp[ns],inference_time[ns]\n");

    const char *model_path = argv[1];

    // load tflite model
    TfLiteModel *model = TfLiteModelCreateFromFile(model_path);
    TfLiteInterpreterOptions *options = TfLiteInterpreterOptionsCreate();
    // TfLiteInterpreterOptionsSetNumThreads(options, 2);

    // create interpreter
    TfLiteInterpreter *interpreter = TfLiteInterpreterCreate(model, options);
    TfLiteInterpreterAllocateTensors(interpreter);
    TfLiteTensor *input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);

    // get input tensor
    struct metadata data;
    FILE *file = fopen("./mnist_test/x_test.csv", "r");
    const int input_size = sizeof(data.train_feature);
    const int output_size = sizeof(data.label);

    for (;;)
    {
        if (get_data(file, &data) == -1)
            break;

        times.timestamp = gettimens();
        // set input as data.train_feature
        TfLiteTensorCopyFromBuffer(input_tensor, data.train_feature, input_size);
        // run inference
        TfLiteInterpreterInvoke(interpreter);
        // extract output
        const TfLiteTensor *output_tensor = TfLiteInterpreterGetOutputTensor(interpreter, 0);
        TfLiteTensorCopyToBuffer(output_tensor, data.label, output_size);
        // print data.label

        times.run_time = gettimens() - times.timestamp;

        printf("%ld,%ld\n", times.timestamp, times.run_time);
        // sleeping for 1ms minus the time taken to train the model

        // fprintf(stderr, "time elapsed: %d\n", time_elapsed_us);

        // usleep(2000000 - time_elapsed_us);
    }

    TfLiteInterpreterDelete(interpreter);
    TfLiteInterpreterOptionsDelete(options);
    TfLiteModelDelete(model);

    return 0;
}