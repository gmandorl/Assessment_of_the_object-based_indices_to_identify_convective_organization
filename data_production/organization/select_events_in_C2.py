import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import glob
import os



def select_events_in_C2(dataset) :

    path = f'output/merged/{dataset}/'
    folder_all = f'{path}C2_original/'
    folder_sel = f'{path}C2/'

    df_base      = pd.read_csv(f'{folder_sel}C2_base.csv')
    df_mergedObj = pd.read_csv(f'{folder_sel}C2_mergedObj.csv')


    # save the original version in another folder
    if not os.path.isdir(folder_all) :
        os.makedirs(folder_all)

    df_base.to_csv(f'{folder_all}C2_base.csv',           index=False)
    df_mergedObj.to_csv(f'{folder_all}C2_mergedObj.csv', index=False)


    # calculate Delta N and perform the selection
    delta_N       = df_base['number'] - df_mergedObj['number']

    df_base     ['delta_N']  = delta_N
    df_mergedObj['delta_N']  = delta_N


    # select only the events where there are two objects that merged
    df_base      = df_base.query('delta_N==1')
    df_mergedObj = df_mergedObj.query('delta_N==1')
    del df_base['delta_N']
    del df_mergedObj['delta_N']

    # save the selected file
    df_base.to_csv(f'{folder_sel}C2_base.csv',           index=False)
    df_mergedObj.to_csv(f'{folder_sel}C2_mergedObj.csv', index=False)

