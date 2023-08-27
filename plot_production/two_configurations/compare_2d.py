import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import os
import warnings


def draw_and_save ( METRIC,
                    H2,
                    axis_label_original,
                    axis_label_modified,
                    folder_out = "figure/2d_comparison/",
                    set_log = False
                    ) :

    fig, ax   = plt.subplots( figsize=(8,6) )

    # take care of when H2 is a delta function
    bin_width = H2[1][1] - H2[1][0]
    if bin_width<1e-20 : return
    if np.sum(H2[0])<1e-20 : return

    # transform the histogram into density
    SF         =  100 / np.sum(H2[0]) / bin_width**2
    h2_to_plot =  H2[0]
    h2_to_plot =  h2_to_plot * SF


    # x-y limits
    xedges  = ( H2[1][:-1] + H2[1][1:] ) / 2.
    yedges  = ( H2[2][:-1] + H2[2][1:] ) / 2.

    # z limits
    levels  = np.linspace (SF, h2_to_plot.max() if not set_log else np.log(h2_to_plot.max()), 11)
    ticks   = np.array([levels[0], levels[2], levels[4], levels[6], levels[8], levels[10]])
    ticks_round = np.around(ticks, 1)

    # z limits for the log scale
    if set_log :
        levels  = np.linspace ( -4, 0, 9)
        ticks   = np.array([levels[0], levels[2], levels[4], levels[6], levels[8]])
        ticks_round = np.around((10**ticks), 4)
        if 'percentile' in folder_out : ticks_round = ['10$^{-6}$', '10$^{-5}$', '10$^{-4}$', '10$^{-3}$', '10$^{-2}$']
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            h2_to_plot  = np.log10(h2_to_plot)


    # plot the density
    h2_to_plot = np.where(h2_to_plot>levels[0], h2_to_plot, np.nan)
    contourf_  = plt.contourf(xedges, yedges, h2_to_plot, levels=levels, cmap='Blues')

    # plot the diagonal
    range_min = xedges[1]
    range_max = xedges[-2]
    plt.plot( (range_min,range_max),(range_min,range_max), color='r', linestyle='--', linewidth=2)

    # add colorbar
    fig.subplots_adjust(left=0.15, right=0.82)  # add a new axix to the right
    cbar_ax = fig.add_axes([0.84, 0.2, 0.01, 0.6])
    cbar = fig.colorbar(contourf_, cax=cbar_ax, ticks=ticks)
    cbar.ax.set_yticklabels(ticks_round)


    # axis label
    ax.set_xlabel(axis_label_original)
    ax.set_ylabel(axis_label_modified)
    plt.text(1.04, 0.97, 'Density', weight='bold', transform = ax.transAxes)

    # save the plot
    plt.savefig(f'{folder_out}/{METRIC}.png')
    plt.savefig(f'{folder_out}/{METRIC}.pdf')
    plt.close()






def compare_2d( METRIC,
                df_original,
                df_modified,
                axis_label_original,
                axis_label_modified,
                nbins      = 50,
                folder_out = "figure/2d_comparison/",
                use_values = True
                ) :

    original = df_original[METRIC]
    modified = df_modified[METRIC]


    # select where there are non NAN values
    non_NAN = np.logical_and( np.isfinite(original),
                              np.isfinite(modified))

    original = original[non_NAN].to_numpy()
    modified = modified[non_NAN].to_numpy()


    # numpy to plot
    up_limit   =  np.quantile(original, q=0.99)
    lo_limit   =  np.quantile(original, q=0.01)
    set_log    = False
    if not use_values :
        up_limit   =  100.
        lo_limit   =  0.
        set_log    =  True

    # make the histogram
    plot_range =  [[lo_limit, up_limit], [lo_limit, up_limit]]
    H2 = np.histogram2d(modified, original, bins=nbins, range=plot_range)



    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)


    draw_and_save( METRIC, H2, axis_label_original, axis_label_modified, folder_out, set_log = set_log)






