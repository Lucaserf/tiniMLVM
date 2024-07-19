#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>

#define INPUT_SIZE 10
#define DATASET_SIZE (int)1e5

struct metadata
{
    double train_feature[INPUT_SIZE];
    double label[1];
};

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

// get all data from the file

int get_all_data(FILE *file, struct metadata *data, int size)
{
    for (int i = 0; i < size; i++)
    {
        if (get_data(file, &data[i]) == -1)
        {
            return i;
        }
    }
    return size;
}

int main()
{
    struct metadata reference_data[DATASET_SIZE];
    FILE *reference_file = fopen("./regression_test/reference.csv", "r");
    if (reference_file == NULL)
    {
        printf("Error opening file\n");
        return 1;
    }

    get_all_data(reference_file, reference_data, DATASET_SIZE);
    fclose(reference_file);

    struct metadata data[DATASET_SIZE];
    FILE *datafile = fopen("./regression_test/data.csv", "r");
    if (datafile == NULL)
    {
        printf("Error opening file\n");
        return 1;
    }
    get_all_data(datafile, data, DATASET_SIZE);
    fclose(datafile);

    // measure the drift
    double drift = 0;
    for (int i = 0; i < DATASET_SIZE; i++)
    {
        for (int j = 0; j < INPUT_SIZE; j++)
        {
            drift += pow(data[i].train_feature[j] - reference_data[i].train_feature[j], 2);
        }
    }

    drift = sqrt(drift);
    printf("Drift: %lf\n", drift);

    return 0;
}
