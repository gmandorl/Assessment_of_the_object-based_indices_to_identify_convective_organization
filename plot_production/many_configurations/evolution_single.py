import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cbook as cbook
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl
import configparser

# label of each index
conf_ = configparser.ConfigParser()
conf_.read('../colors.ini')
label_leg  = conf_['LEGEND']



def evolution_single( METRIC,
                      path,
                      path_corr,
                      Condition,
                      fname,
                      df_original,
                      config,
                      folder_out        = f'figure',
                      use_values        = True
                      ) :

    Z_mean      = []
    Z_median    = []
    Z_10q       = []
    Z_90q       = []
    stats_inner = []
    stats_outer = []
    corrcoef = []

    # loop over all the perturbed cases
    for fname_modified in config.cases :

        # read the data
        df_modified  = pd.read_csv( f'{path}{fname}{Condition}_{fname_modified}.csv')
        modified = df_modified[METRIC].to_numpy()
        original = df_original[METRIC].to_numpy()


        # select where there are non NAN values
        non_NAN = np.logical_and( np.isfinite(original),
                                  np.isfinite(modified))
        original = original[non_NAN]
        modified = modified[non_NAN]

        # compute correlation using values
        df_modified_corr  = pd.read_csv( f'{path_corr}{Condition}_{fname_modified}.csv')
        df_original_corr  = pd.read_csv( f'{path_corr}{Condition}_base.csv')
        modified_corr     = df_modified_corr[METRIC].to_numpy()[non_NAN]
        original_corr     = df_original_corr[METRIC].to_numpy()[non_NAN]


        # compute Z
        std      = np.nanstd(original) if use_values else 1.
        Z_metric = ( modified - original ) / std


        # save data and statistics
        Z_mean.append( np.mean(Z_metric) )
        Z_median.append( np.median(Z_metric) )
        Z_10q.append( np.quantile(Z_metric, q=0.1) )
        Z_90q.append( np.quantile(Z_metric, q=0.9) )
        corrcoef.append( np.corrcoef(original_corr, modified_corr)[0][1] )
        box_inner =  cbook.boxplot_stats(Z_metric, whis=0)[0]
        box_outer =  cbook.boxplot_stats(Z_metric, whis=[10, 90])[0]
        box_inner['q1'], box_inner['q3'] = np.percentile(Z_metric, [30, 70])
        box_outer['q1'], box_outer['q3'] = np.percentile(Z_metric, [20, 80])

        stats_inner.append(box_inner)
        stats_outer.append(box_outer)


    # statistics to draw
    boxprops        = dict(linestyle='-', linewidth=1)
    medianprops     = dict(linewidth=2.5, color='k')
    meanpointprops  = dict(marker='D', markeredgecolor='black', markerfacecolor='#984e4f', markersize=8)


    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)


    fig, ax = plt.subplots(figsize =(8, 6))

    # Creating axes instance
    bp_outer = ax.bxp(stats_outer, patch_artist = True, widths=0.2, showcaps=False, showfliers=False, boxprops=boxprops)
    bp_inner = ax.bxp(stats_inner, patch_artist = True, widths=0.4, showcaps=False, showfliers=False,
                      medianprops=medianprops, boxprops=boxprops, meanprops=meanpointprops, showmeans=True)


    # correlation colors
    cmap = plt.cm.turbo
    cmin = 0.2 # also used later
    colors = [cmap( max(0,1-(1-c)/(1-cmin)) ) for c in corrcoef]


    for patch, color in zip(bp_outer['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('k')

    for patch in bp_inner['boxes']:
        patch.set_color('#dddddd')
        patch.set_edgecolor('k')


    # set axes style
    ax.spines[['right', 'top', 'bottom']].set_visible(False)
    ax.spines[['right', 'top', 'bottom']].set_visible(False)
    fig.subplots_adjust(left=0.15)  # add a new axix to the right

    # grid and horizontal line
    ax.axhline(0, color='lightgrey', linewidth=2, linestyle='--')



    # x axis label
    xlabels = config.labels
    xticks  = np.arange(len(xlabels))+1 # this +1 is needed to place correctly the labels
    if len(xlabels) > 15 :
        xlabels = xlabels[1::4] # select one event out of 4
        xticks  = xticks [1::4]
    if len(xlabels) > 30 :
        xlabels = xlabels[1::8] # select one event out of 8
        xticks  = xticks [1::8]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.tick_params(axis='x', colors='darkgrey')
    plt.tick_params(axis='x', bottom=False)

    # axis title
    METRIC_label = label_leg[METRIC] if METRIC in label_leg else METRIC
    ax.set_ylabel(f'Z({METRIC_label})' if use_values else f'$\Delta$p({METRIC_label})')
    ax.set_xlabel(config.xlabel)




    # set legend
    legend_elements = [ Line2D([0], [0], color='k', lw=2, label='median'),
                        Line2D([0], [0], marker='D', color='k', label='mean', lw=0, markerfacecolor='#984e4f', markersize=8),
                        Patch(facecolor='#dddddd', edgecolor='k', label='30%-70%'),
                        Patch(facecolor=cmap(0.8), edgecolor='k', label='20%-80%'),
                        Line2D([], [], marker='|', color='k', linestyle='None', label='10%-90%')]

    leg = plt.legend(handles=legend_elements, fontsize=13)#loc = (0.8, 0.7)
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_color('white')
    handles = leg.legendHandles


    # add color palette for the correlation
    axins = inset_axes(
        ax,
        width="40%",  # width: 5% of parent_bbox width
        height="3%",  # height: 50%
        loc="lower left",
        bbox_to_anchor=( 0.5, 0.98, 1, 1),
        bbox_transform=ax.transAxes,
    )

    # correlation colors
    norm = mpl.colors.Normalize(vmin=cmin, vmax=1)
    bounds = np.linspace(cmin,1,18+1)
    ticks  = np.linspace(cmin,1,4+1)
    cb2 = mpl.colorbar.ColorbarBase(axins, cmap=cmap,
                                norm=norm,
                                boundaries=bounds,
                                #fontsize=13,
                                #extend='both',
                                ticks=ticks,
                                ticklocation='top',
                                spacing='proportional',
                                orientation='horizontal')
    cb2.ax.tick_params(labelsize=13)
    plt.text(0.3, 1.01, 'Correlation\n with ref.', fontsize=13, weight='bold', transform = ax.transAxes)


    # save the plot
    plt.savefig(f'{folder_out}/{METRIC}.png', dpi=300)
    plt.savefig(f'{folder_out}/{METRIC}.pdf', dpi=300)
    plt.close()

    return Z_mean, Z_median, Z_10q, Z_90q, corrcoef


