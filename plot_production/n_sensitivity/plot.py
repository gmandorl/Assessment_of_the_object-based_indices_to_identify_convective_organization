import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import os
import argparse
import configparser
import scipy
from scipy.interpolate import make_interp_spline


# label, color, and style of each index
conf_ = configparser.ConfigParser()
conf_.read('../colors.ini')
colors     = conf_['COLORS']
styles     = conf_['STYLE']
label_leg  = conf_['LEGEND']



parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",          default="TOOCAN", help="name of the dataset"        )
parser.add_argument("-c", "--condition",        default="C1",     help="condition to plot"          )
parser.add_argument("-n", "--selected_number",  default=0,        help="condition to plot", type=int)
parser.add_argument('--use_original',                                   action='store_true'  )
parser.add_argument('--use_anomaly',            dest='use_original',    action='store_false' )
parser.add_argument('--use_percentiles',                                action='store_true'  )
parser.add_argument('--use_values',             dest='use_percentiles', action='store_false' )
parser.set_defaults(use_original=True)
parser.set_defaults(use_percentiles=True)
args = parser.parse_args()




if __name__ == '__main__':
    start_time = datetime.datetime.now()

    # path of the input csv files
    folder1 = "percentiles" if args.use_percentiles else "values"
    folder2 = 'original' if args.use_original else 'anomaly'
    path_id = f'{args.dataset}/{folder1}/{folder2}/{args.condition}/'
    path = f'../two_configurations/figure/{path_id}output/'

    # make the figure where to save the plot
    folder_out = f'figure/{path_id}'
    if not os.path.isdir(folder_out) : os.makedirs(folder_out)


    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)


    # label to write in the legend
    var_to_plot = dict()
    var_to_plot['Delta_p'] = '$ <|\Delta$p|>' if args.use_percentiles else '$ <|\Delta $ Z|>'
    var_to_plot['correlation'] = 'correlation'
    var_to_plot['fraction_of_events_with_decreasing_organization'] = 'fraction of event with a decreasing'




    # read the file names and store them in a list (except for info_n0 that contains all N>2)
    filepaths = [path+f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('info_n0.csv') ]
    print([x[-6:] for x in filepaths])

    # read the csv fils
    df = pd.concat(map(pd.read_csv, filepaths))
    df = df.sort_values(by=['number_of_objects'])



    # read the organization indices
    METRICS = np.unique(df.METRIC)
    METRICS = ['number', 'Iorg','Lorg', 'MICA','ROME', 'ABCOP', 'area', 'SCAI', 'MCAI', 'OIDRA', 'COP']
    #METRICS = ['Iorg','Lorg']




    for vs in var_to_plot.keys() :
        fig, ax   = plt.subplots( figsize=(8,6) )

        for METRIC in METRICS :

            # read METRIC and number of objects
            df_ = df.query(f'METRIC=="{METRIC}"')
            metric_sensibility = df_[vs].to_numpy()
            number_of_objects  = df_.number_of_objects.to_numpy()


            # plot
            color        = colors[METRIC] if METRIC in colors else 'k'
            style        = styles[METRIC] if METRIC in styles else '-'
            METRIC_label = label_leg[METRIC] if METRIC in label_leg else METRIC


            # make a spline to plot a smoother function
            x_min = 3
            x_max = np.max(number_of_objects)
            new_x = np.linspace(x_min, x_max, (x_max-x_min)*10+1)
            spl   = make_interp_spline(number_of_objects, metric_sensibility, k=2)
            new_y = spl(new_x)

            # plot
            ax.plot(new_x, new_y, color=color, lw=3, label=METRIC_label, ls=style)
            #ax.plot(number_of_objects, metric_sensibility, color=color, lw=3, label=METRIC_label, ls=style)


        # set axis
        ax.spines[['right', 'top']].set_visible(False)
        ax.set_ylabel(var_to_plot[vs])
        ax.set_xlabel('number of objects')
        plt.grid(True, axis='y', linestyle='--')
        #plt.ylim([y_min, y_max])
        if vs == 'Delta_p' : plt.ylim([0, 30])
        plt.xlim([0, 40])

        plt.text(0.03, 0.93,  f'Perturbation ({args.condition[-1]})', weight='bold', transform = ax.transAxes, size=18)

        # legend
        leg = plt.legend(fontsize=15, ncol=2)
        plt.setp(leg.get_title(),fontweight='bold')
        leg.get_frame().set_linewidth(0.0)
        leg.get_frame().set_color('white')
        #leg.get_frame().set_alpha(1.)



        # save the plot
        plt.savefig(f'{folder_out}{vs}.png')
        plt.savefig(f'{folder_out}{vs}.pdf')

        fig.clf()


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

