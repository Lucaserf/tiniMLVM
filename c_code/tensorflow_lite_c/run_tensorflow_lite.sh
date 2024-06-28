gcc -march=native -O3 -o tflite_times tflite_times.c -ltensorflow
./tflite_times #> tflite_times.csv
rm ./tflite_times
