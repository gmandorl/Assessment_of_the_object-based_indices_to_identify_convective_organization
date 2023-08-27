import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
from datetime import timezone
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", default='TOOCAN', help="dataset to use")
args = parser.parse_args()


def compute_day_of_year (year, month, day, hour, minute) :
    """Return the date in datetime format"""
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=timezone.utc)


def time_diff(t1, t2) :
    return t1==t2




if __name__ == '__main__':
    start_time = datetime.datetime.now()



    for time_shift in list(np.arange(1,30, dtype=int)*30) + list(np.arange(1,4, dtype=int)*60*24) + [131400] :
        time_shift = int(time_shift)
        n = int( time_shift / 30. )
        print(n, time_shift)

        path = f'../organization/output/merged/{args.dataset}/'

        df   = pd.read_csv(f'{path}C1/C1_base.csv')

        df['date'] = df.apply(lambda x: compute_day_of_year(x['year'],
                                                            x['month'],
                                                            x['day'],
                                                            x['hour'],
                                                            x['minute']), axis=1)

        # create df2: the shift df1 of time_shift
        df1  = df
        df2  = df.iloc[n:  , :]

        df2_end = pd.DataFrame(columns=df1.columns, index=list(range(n)) )
        df2_end['year']   = 3000
        df2_end['month']  = 1
        df2_end['day']    = 1
        df2_end['hour']   = 0
        df2_end['minute'] = 0
        df2  = pd.concat( (df2, df2_end) )


        # shift the two dataframe ( "to_numpy" is crucial to perform the shift! )
        df1['date_shifted'] = df2['date'].to_numpy() - datetime.timedelta(minutes=time_shift)
        df1['to_select'] = df1.apply(lambda x: time_diff(x['date'], x['date_shifted']), axis=1)
        df2['to_select'] = df1['to_select'].to_numpy()


        # perform the selection
        columns_to_nan = [x for x in df2.columns if x not in ['year', 'month', 'day', 'hour', 'minute']]
        df2[columns_to_nan][df2['to_select']==False] = np.nan


        # remove new used columns
        del df1['date_shifted']
        del df1['to_select']
        del df2['to_select']
        del df1['date']
        del df2['date']


        # save the new data
        folder_out = f'{path}/C6/'
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        df1.to_csv(f'{folder_out}C6_base.csv',           index=False)
        df2.to_csv(f'{folder_out}C6_{time_shift}min_later.csv',    index=False)


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

