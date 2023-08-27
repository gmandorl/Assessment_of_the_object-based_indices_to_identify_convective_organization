import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import datetime
import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--condition", default='C1',     help="condition")
parser.add_argument("-d", "--dataset",   default='TOOCAN', help="dataset to use")
args = parser.parse_args()


factors = {f'reso{n}': n for n in range(2,7)}


def scale_with_dimension(df, label) :
    "this function multiply by the right factor when different resolutions are considered in condition C5"

    if label in factors.keys() :
        scale_factor = factors[label]
        for METRIC in df.columns :
            if   METRIC in ['ROME', 'ROME_delta'] or 'area' in METRIC :  df[METRIC] = df[METRIC] * scale_factor**2
            elif METRIC in ['MCAI', 'SCAI'] :                            df[METRIC] = df[METRIC] / scale_factor**2

    return df



if __name__ == '__main__':
    start_time = datetime.datetime.now()

    path = f'output/tmp/{args.dataset}/{args.condition}/'
    labels = os.listdir(path)

    for label in labels :

        # read the files and store the information in a dataframe
        file_names = glob.glob(f'{path}{label}/*' )
        df = pd.concat((pd.read_csv(f) for f in file_names), ignore_index=True)
        df = df.sort_values(by = ['year', 'month', 'day', 'hour', 'minute'], ascending = True)

        # correct scale factor: it works only for C5
        df = scale_with_dimension(df, label)


        # save the merged file
        folder_out = f'output/merged/{args.dataset}/{args.condition}/'
        fname = os.listdir(f'{path}{label}/')[0].split('___')[0]
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        df.to_csv(f'{folder_out}{fname}.csv', index=False)


    # if condition is C2: select only the perturbed images
    if args.condition=='C2' :
        import select_events_in_C2
        select_events_in_C2.select_events_in_C2(args.dataset)

    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')
