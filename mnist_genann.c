#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include "mnist.h"
#include "genann.h"

float evaluate_model(genann *ann)
{
    int correct = 0;
    for (int i = 0; i < NUM_TEST; i++)
    {
        const double *guess = genann_run(ann, test_image[i]);
        int max = 0;
        // argmax
        for (int j = 1; j < 10; j++)
        {
            if (guess[j] > guess[max])
            {
                max = j;
            }
        }
        if (max == test_label[i])
        {
            correct++;
        }
    }
    double accuracy = (double)correct / NUM_TEST;
    return accuracy;
}

int main()
{
    load_mnist();

    printf("initializing the neural network\n");

    genann *ann = genann_init(784, 2, 64, 1);

    float learning_rate = 0.01;

    printf("label: %d\n", train_label[0]);

    for (int i = 0; i < 5; i++)
    {
        genann_train(ann, (const double *)train_image, (const double *)train_label, learning_rate);
        printf("epoch: %d ", i);
        float accuracy = evaluate_model(ann);
        printf("accuracy: %lf\n", accuracy);
    }
    print_mnist_pixel(test_image, 1);
    const double *guess = genann_run(ann, test_image[1]);

    printf("%lf\n", guess[0]);

    genann_free(ann);
    return 0;
}