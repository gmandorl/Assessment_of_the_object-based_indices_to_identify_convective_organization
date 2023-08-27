import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import argparse
import importlib
import os
import config

from evolution_single import evolution_single
from evolution_all    import evolution_all


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",      default="TOOCAN",       help="name of the dataset"  )
parser.add_argument("-c", "--condition",    default="C3",           help="condition to plot"    )
parser.add_argument('--use_original',                               action='store_true'         )
parser.add_argument('--use_anomaly',        dest='use_original',    action='store_false'        )
parser.add_argument('--use_values',                                 action='store_true'         )
parser.add_argument('--use_percentiles',    dest='use_values',      action='store_false'        )
parser.set_defaults(use_original=True)
parser.set_defaults(use_values=True)
args = parser.parse_args()



config = config.configs[args.condition]



if __name__ == '__main__':
    start_time = datetime.datetime.now()

    print('use_values', args.use_values, '\t use_original', args.use_original)


    # path and prefix of the name of the files to read
    fname = '' if args.use_original else 'anomaly___'
    path       = f'../../data_production/organization/output/merged/{args.dataset}/{args.condition}/'
    if not args.use_original :       path = f'../../data_production/anomaly/output/{args.dataset}/{args.condition}/'
    path_corr  = path + fname
    if not args.use_values :    path = f'../../data_production/percentiles/output/{args.dataset}/{args.condition}/'


    # read the data
    df_original = pd.read_csv( f'{path}{fname}{args.condition}_{config.fname_original}.csv')


    # select the variables to plot
    METRICS = df_original.columns
    METRICS = [m for m in METRICS if m not in ['year', 'month', 'day', 'hour', 'minute', 'day_of_year', 'ROME_delta']]

    # directory where to save the plots
    folder_out = 'original' if args.use_original else 'anomaly'
    folder_out = f'{"percentiles" if not args.use_values else "values"}/{folder_out}'
    folder_out = f'figure/{args.dataset}/{folder_out}/{args.condition}'
    if not os.path.isdir(folder_out) : os.makedirs(f'{folder_out}/evolution_single')



    # call evolution_single for each indices. It produces the boxplots
    data_mean    = dict()
    data_median  = dict()
    data_10q     = dict()
    data_90q     = dict()
    data_corr    = dict()

    for METRIC in METRICS :
        Z_stats = evolution_single( METRIC            = METRIC,
                                    path              = path,
                                    path_corr         = path_corr,
                                    Condition         = args.condition,
                                    fname             = fname,
                                    df_original       = df_original,
                                    config            = config,
                                    folder_out        = f'{folder_out}/evolution_single',
                                    use_values        = args.use_values
                                    )
        data_mean[METRIC]   = Z_stats[0]
        data_median[METRIC] = Z_stats[1]
        data_10q[METRIC]    = Z_stats[2]
        data_90q[METRIC]    = Z_stats[3]
        data_corr[METRIC]   = Z_stats[4]


    # compare all indices on the same plot
    #METRICS = [x for x in METRICS if x not in config.var_to_exclude]
    METRICS = ['number', 'Iorg','Lorg', 'MICA','ROME', 'ABCOP', 'area', 'SCAI', 'MCAI', 'OIDRA', 'COP']


    evolution_all( METRICS,
                   data_mean,
                   config,
                   figname    = 'mean',
                   ylabel     = 'Z mean' if args.use_values else '< $\Delta$p >',
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text = ''
                   )

    evolution_all( METRICS,
                   data_median,
                   config,
                   figname    = 'median',
                   ylabel     = 'Z median' if args.use_values else 'median of $\Delta$p',
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text = ''
                   )

    evolution_all( METRICS,
                   data_corr,
                   config,
                   figname    = 'correlation',
                   ylabel     = 'correlation with ref.' if args.condition!='C6' else 'auto-correlation',
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text = ''
                   )

    evolution_all( METRICS,
                   data_10q,
                   config,
                   figname    = 'quantile_10',
                   ylabel     = 'lower 10% of Z' if args.use_values else 'lower 10% of $\Delta$p',
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text = ''
                   )

    evolution_all( METRICS,
                   data_90q,
                   config,
                   figname    = 'quantile_90',
                   ylabel     = 'upper 10% of Z' if args.use_values else 'upper 10% of $\Delta$p',
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text = ''
                   )



    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

