#!/bin/bash

dataset=$1


# compute the organization indices and store them in csv files
cd data_production/organization/
source run_all.sh $dataset


# compute the percentiles
echo 'running percentiles'
cd ../percentiles/
source run.sh $dataset
cd ../..




# produce the plots
echo 'running plots'
cd plot_production/two_configurations/
source run.sh $dataset
cd ../n_sensitivity/
source run.sh $dataset
cd ../many_configurations/
source run.sh $dataset
cd ../..


