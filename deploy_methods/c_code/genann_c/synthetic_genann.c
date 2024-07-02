#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include "genann.h"

#define EPOCHS 200
#define TRAINING_BATCH 1000
#define TESTING_BATCH 100
#define INPUT_SIZE 10
#define TEST_SIZE_PRINT 5

double synthetic_function(const double *x){
    return pow(x[0], 2) + 4*pow(x[1], 2) + pow(x[2], 2) + pow(x[3], 6) + pow(x[4], 2) + pow(x[5], 3) + pow(x[6], 2) + pow(x[7], 3) + 6*pow(x[8], 2) + pow(x[9], 2);
}

double mean_squared_error(double *x,double *y, int n){
    double error = 0;
    for (int i = 0; i < n; i++){
        error += pow(x[i] - y[i], 2);
    }
    return error / n;

}

int main(){

    // printf("initializing the neural network\n");

    genann *ann = genann_init(INPUT_SIZE, 2, 32, 1);

    float learning_rate = 0.001;

    printf("training the neural network\n");
    for (int i = 0; i < EPOCHS; i++){
        double train_feature[INPUT_SIZE];
        double train_label[1];
        for (int j = 0; j < TRAINING_BATCH; j++){
            for (int k = 0; k < INPUT_SIZE; k++){
                train_feature[k] = (double) rand() / RAND_MAX;
                // printf("train_feature[%d]: %lf\n", k, train_feature[k]);
            }
            train_label[0] = synthetic_function(train_feature);
            // printf("train_label: %lf\n", train_label[0]);
            genann_train(ann, train_feature, train_label , learning_rate);
        }
        printf("epoch: %d \n", i);

        double input[TESTING_BATCH];
        double labels[TESTING_BATCH];
        for (int j = 0; j < TESTING_BATCH; j++){
            double testing_feature[INPUT_SIZE];
            double testing_label[1];
            for (int k = 0; k < INPUT_SIZE; k++){
                testing_feature[k] = (double) rand() / RAND_MAX;
                // printf("testing_feature[%d]: %lf\n", k, testing_feature[k]);
            }
            testing_label[0] = synthetic_function(testing_feature);
            // printf("testing_label: %lf\n", testing_label[0]);
            double const *out = genann_run(ann, testing_feature);
            // printf("output: %lf\n", out[0]);
            input[j] = out[0];
            labels[j] = testing_label[0];
        }

        printf("mean squared error: %lf\n", mean_squared_error(input, labels, TESTING_BATCH));
    }

    for (int j = 0; j < TEST_SIZE_PRINT; j++){
        double testing_feature[INPUT_SIZE];
        double testing_label[1];
        for (int k = 0; k < INPUT_SIZE; k++){
            testing_feature[k] = (double) rand() / RAND_MAX;
            printf("testing_feature[%d]: %lf\n", k, testing_feature[k]);
        }
        testing_label[0] = synthetic_function(testing_feature);
        printf("testing_label: %lf\n", testing_label[0]);
        double const *out = genann_run(ann, testing_feature);
        printf("output: %lf\n", out[0]);
    }



    genann_free(ann);
    return 0;
}