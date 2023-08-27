import numpy as np
import datetime
import glob
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",   default="TOOCAN",  help="name of the dataset")
parser.add_argument("-c", "--condition", default="C1",      help="condition under study")
parser.add_argument("-s", "--split",     default=0,         help="split the input files in three groups")
parser.add_argument('--use_original',                       action='store_true')
parser.add_argument('--use_anomaly', dest='use_original',   action='store_false')
parser.set_defaults(use_original=True)
args = parser.parse_args()


var_to_exclude = ['year', 'month', 'day', 'hour', 'minute', 'day_of_year', 'number_original', 'area_original']





def compute_percentile (x, var_base) :
    """ return the percentile of the distribution of the non NAN base vector"""
    if np.isnan(x) : return np.nan
    return 100 * np.nansum((var_base<=x)) / np.sum(np.isfinite(var_base))


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    print(f'MAKE PERCENTILE {args.condition}! use_original is', args.use_original)

    # path and prefix of the names depending if anomaly is used
    path = f'../organization/output/merged/{args.dataset}/{args.condition}/'
    if not args.use_original : path = f'../anomaly/output/{args.dataset}/{args.condition}/'
    prefix = '' if args.use_original else 'anomaly___'

    # list of the files to read
    fname_base = f'{path}{prefix}{args.condition}_base.csv'
    file_names = glob.glob(f'{path}{prefix}{args.condition}*.csv')
    file_names.sort()


    # use only half of the files if needed (because they may be too many)
    if args.split=='1' : file_names = file_names[                          : int(  len(file_names)/3 ) ]
    if args.split=='2' : file_names = file_names[ int(  len(file_names)/3 ): int(2*len(file_names)/3 ) ]
    if args.split=='3' : file_names = file_names[ int(2*len(file_names)/3 ):                           ]

#    print('TEST', file_names)


    # file base to use for computing percentiles
    df_base = pd.read_csv(fname_base)
    columns = [ x for x in df_base.columns if x not in var_to_exclude]


    # loop over all the files
    for fname_extended in file_names :

        fname   = fname_extended.split('/')[-1]
        print(fname_extended)

        # read file
        df = pd.read_csv(fname_extended)



        for vs in columns :

            var_base = df_base[vs].to_numpy()
            df[vs]   = df.apply(lambda x: compute_percentile(x[vs], var_base), axis=1)


        folder_out = f'output/{args.dataset}/{args.condition}/'
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        df.to_csv(f'{folder_out}{fname}', index=False)


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')


