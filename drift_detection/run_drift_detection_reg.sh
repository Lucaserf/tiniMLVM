cd drift_detection

gcc -march=native -O3 -o drift_detection_reg drift_detection_reg.c -lm

cd ..

./drift_detection/drift_detection_reg 
rm ./drift_detection/drift_detection_reg 
