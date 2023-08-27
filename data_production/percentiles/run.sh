#!/bin/bash

dataset=$1




python main.py  -c C1  --use_original -d $dataset &
python main.py  -c C2  --use_original -d $dataset &

python main.py  -c C3  --use_original -d $dataset -s 1 &
python main.py  -c C3  --use_original -d $dataset -s 2 &
python main.py  -c C3  --use_original -d $dataset -s 3 &
python main.py  -c C4  --use_original -d $dataset -s 1 &
python main.py  -c C4  --use_original -d $dataset -s 2
python main.py  -c C4  --use_original -d $dataset -s 3 &

python main.py  -c C5  --use_original -d $dataset
python main.py  -c C6  --use_original -d $dataset -s 1 &
python main.py  -c C6  --use_original -d $dataset -s 2 &
python main.py  -c C6  --use_original -d $dataset -s 3 &
python main.py  -c C7  --use_original -d $dataset -s 1 &
python main.py  -c C7  --use_original -d $dataset -s 2
python main.py  -c C7  --use_original -d $dataset -s 3



