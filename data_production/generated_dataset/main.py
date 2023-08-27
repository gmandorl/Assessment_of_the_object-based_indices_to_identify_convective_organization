import numpy as np
import xarray as xr
import datetime
import argparse
import calendar
import os
import random
import math

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--month", default='01', help="month")
parser.add_argument("-y", "--year",  default=2012, type=int, help="year")
args = parser.parse_args()

path_out = 'files'


def create_circular_selection(xs, ys, center=[10,10], area=1):
    """ Create a maks of a circular region around center with a given area"""
    dist_from_center2 = (xs - center[0])**2 + (ys-center[1])**2
    index_selection   = dist_from_center2 <= area
    return index_selection



if __name__ == '__main__':
    start_time = datetime.datetime.now()

    # define year, month, day
    year  = args.year
    month = args.month
    days_in_month = calendar.monthrange(year, int(month))[1]


    # grided coordinates to use for masking
    xs, ys = np.meshgrid(np.arange(120), np.arange(120))


    for dd in range(1, days_in_month+1) :

        # create folter out
        folder_out = f'{path_out}/{args.year}/{args.year}_{month}_{dd:02d}'
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)


        # create a mock data file every 30 minutes
        for n in range(48) :
            hh = int(n/2)
            mm = 30*(n%2)


            random_binary_field = np.zeros((120,120))


            # Generate objects number and dimension
            Nobjects = int(random.expovariate(math.log(10)/30.) + random.expovariate(math.log(10)/10.) * (random.random() < 0.5))

            for object_iterator in range(Nobjects) :


                area=random.expovariate(math.log(10)/800.)
                if random.random() < 0.9 : area=random.expovariate(math.log(10)/10.)

                index_selection = create_circular_selection(xs, ys,
                                                            center=[random.randint(0, 120), random.randint(0, 120)],
                                                            area=area)
                random_binary_field[index_selection] = 1





            # save the random field in a netCDF file
            ds = xr.Dataset({'random_objects':     (('extra_dim', 'latitude','longitude'), [random_binary_field])},
                            coords= {'extra_dim': [0],
                                     'latitude' : np.linspace(0,12, 120),
                                     'longitude': np.linspace(0,12, 120)},
                            )


            ds.attrs['image_time'] = f'{year}-{month}-{dd:02d}-T{hh:02d}-{mm:02d}-00 UTC'

            ds.to_netcdf(f'{folder_out}/random_objects_data-{n:02d}.nc')


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')
