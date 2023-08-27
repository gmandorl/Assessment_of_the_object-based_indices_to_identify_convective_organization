#!/bin/bash

dataset=$1


source run.sh C1      $dataset;     sleep 300
source run.sh C2      $dataset;     sleep 300
source run.sh C3      $dataset;     sleep 300
source run.sh C3_bis  $dataset;     sleep 300
source run.sh C4      $dataset;     sleep 300
source run.sh C5      $dataset;     sleep 300
source run.sh C7      $dataset;     sleep 300




source run_merge.sh   $dataset

python compute_C6.py -d $dataset
sleep 300
