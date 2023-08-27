import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import argparse
import config
import os
import configparser

from compare_2d    import compare_2d
from variation_all import variation_all



parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",          default="TOOCAN",      help="name of the dataset"          )
parser.add_argument("-c", "--condition",        default="C1",          help="condition to plot"            )
parser.add_argument("-n", "--selected_number",  default=0,             help="number of objects",   type=int)
parser.add_argument('--use_original',                                  action='store_true' )
parser.add_argument('--use_anomaly',            dest='use_original',   action='store_false')
parser.add_argument('--use_values',                                    action='store_true' )
parser.add_argument('--use_percentiles',        dest='use_values',     action='store_false')
parser.set_defaults(use_original=True)
parser.set_defaults(use_values=True)
args = parser.parse_args()


config=config.configs[args.condition]

conf_ = configparser.ConfigParser()
conf_.read('../colors.ini')
label_leg  = conf_['LEGEND']




if __name__ == '__main__':
    start_time = datetime.datetime.now()

    print('condition:', args.condition, ' \t use_values:', args.use_values, '\t use_original:', args.use_original)

    # path and prefix of the name of the files to read
    fname = '' if args.use_original else 'anomaly___'
    path  = f'../../data_production/organization/output/merged/{args.dataset}/{args.condition}/'
    if not args.use_original :       path = f'../../data_production/anomaly/output/{args.dataset}/{args.condition}/'
    if not args.use_values :     path = f'../../data_production/percentiles/output/{args.dataset}/{args.condition}/'


    # read the data
    df_original = pd.read_csv( f'{path}{fname}{args.condition}_{config.fname_original}.csv')
    df_modified = pd.read_csv( f'{path}{fname}{args.condition}_{config.fname_modified}.csv')

    # select the variables to plot
    METRICS = df_original.columns
    METRICS = [m for m in METRICS if m not in ['year', 'month', 'day', 'hour', 'minute', 'day_of_year']]



    # directory where to save the plots
    folder_out = 'original' if args.use_original else 'anomaly'
    folder_out = f'{"percentiles" if not args.use_values else "values"}/{folder_out}'
    folder_out = f'figure/{args.dataset}/{folder_out}/{args.condition}'
    if not os.path.isdir(f'{folder_out}/2d_comparison') : os.makedirs(f'{folder_out}/2d_comparison')


    ############## possible selection on N ################
    if args.selected_number > 0 :
        idx_to_select = np.abs( df_original['number_original'] - args.selected_number ) < 2
        df_original   = df_original[idx_to_select]
        df_modified   = df_modified[idx_to_select]
    print('LEN', len(df_original))
    #######################################################




    # loop over all variables to produce the 2d distribution to compare the two cases
    for METRIC in METRICS :

        # set the label of the axes
        METRIC_label = label_leg[METRIC] if METRIC in label_leg else METRIC
        axis_label = METRIC_label if args.use_values else f'p({METRIC_label})'

        compare_2d( METRIC              = METRIC,
                    df_original         = df_original,
                    df_modified         = df_modified,
                    axis_label_original = axis_label,
                    axis_label_modified = f'{axis_label} {config.axis_label_modified}',
                    folder_out          = f'{folder_out}/2d_comparison',
                    use_values          = args.use_values
                    )


    # select the variables to compare in a single plot
    #METRICS = [x for x in METRICS if x not in config.var_to_exclude]
    METRICS = ['number', 'Iorg','Lorg', 'MICA','ROME', 'ABCOP', 'area', 'SCAI', 'MCAI', 'OIDRA', 'COP']


    # compare all indices on the same plot
    variation_all( METRICS,
                   df_original,
                   df_modified,
                   selected_number = args.selected_number,
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text =''
                   )



    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

