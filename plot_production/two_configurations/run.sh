#!/bin/bash

dataset=$1

for n in $(seq 3 1 40;seq 0 1 0)
do
for x in use_original
do
for y in use_values use_percentiles
do


python plot.py -c C1 --$x --$y -d $dataset -n $n &
python plot.py -c C2 --$x --$y -d $dataset -n $n &
python plot.py -c C3 --$x --$y -d $dataset -n $n &
python plot.py -c C4 --$x --$y -d $dataset -n $n &
python plot.py -c C5 --$x --$y -d $dataset -n $n &
python plot.py -c C6 --$x --$y -d $dataset -n $n
python plot.py -c C7 --$x --$y -d $dataset -n $n


done
done
done


