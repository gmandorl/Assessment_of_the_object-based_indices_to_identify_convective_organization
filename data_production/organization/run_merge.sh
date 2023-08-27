#!/bin/bash

dataset=$1

python merge_csv.py -c C1 -d $dataset
python merge_csv.py -c C2 -d $dataset
python merge_csv.py -c C3 -d $dataset
python merge_csv.py -c C4 -d $dataset
python merge_csv.py -c C5 -d $dataset
python merge_csv.py -c C7 -d $dataset
