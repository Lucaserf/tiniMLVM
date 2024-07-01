gcc -march=native -O3 -o tflite_times tflite_times.c -L ~/tflite_build -I ~/tensorflow_src -ltensorflow-lite -lm
./tflite_times #> tflite_times.csv
rm ./tflite_times
