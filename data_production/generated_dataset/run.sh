#!/bin/bash


for yy in {2012..2016}
do
for mm in {01..12}
do


python main.py -m $mm -y $yy &
done
sleep 20
done

