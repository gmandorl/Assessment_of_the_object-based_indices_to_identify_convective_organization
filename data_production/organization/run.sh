#!/bin/bash



CONDITION=$1
dataset=$2

for yy in {2012..2016}
do
python main.py -y $yy -m 1  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 2  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 3  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 4  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 5  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 6  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 7  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 8  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 9  -c $CONDITION -d $dataset  &
python main.py -y $yy -m 10 -c $CONDITION -d $dataset  &
python main.py -y $yy -m 11 -c $CONDITION -d $dataset  &
python main.py -y $yy -m 12 -c $CONDITION -d $dataset
sleep 40
done

