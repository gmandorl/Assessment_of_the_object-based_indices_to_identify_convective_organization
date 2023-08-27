#!/bin/bash

dataset=$1


for x in use_original
do
for y in use_values use_percentiles
do


python plot.py -c C1 --$x --$y -d $dataset
python plot.py -c C2 --$x --$y -d $dataset
python plot.py -c C3 --$x --$y -d $dataset
python plot.py -c C4 --$x --$y -d $dataset
python plot.py -c C5 --$x --$y -d $dataset
python plot.py -c C6 --$x --$y -d $dataset
python plot.py -c C7 --$x --$y -d $dataset


done
done



