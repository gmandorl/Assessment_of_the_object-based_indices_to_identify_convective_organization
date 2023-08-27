import numpy as np
import matplotlib.pyplot as plt
import configparser


# label, color, and style of each index
conf_ = configparser.ConfigParser()
conf_.read('../colors.ini')
colors     = conf_['COLORS']
styles     = conf_['STYLE']
label_leg  = conf_['LEGEND']


def evolution_all( METRICS,
                   data,
                   config,
                   figname = 'data',
                   ylabel     = 'Z',
                   folder_out = f'figure',
                   use_values = True,
                   extra_text = ''
                   ) :



    data = dict( (k, data[k])   for k in METRICS )

    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)


    fig, ax = plt.subplots(figsize =(8, 6))

    # plot each index
    for METRIC in METRICS :
        color        = colors[METRIC] if METRIC in colors else 'k'
        style        = styles[METRIC] if METRIC in styles else '-'
        METRIC_label = label_leg[METRIC] if METRIC in label_leg else METRIC
        ax.plot(data[METRIC], marker='o', label=METRIC_label, color=color, ls=style)


    # set axes style
    ax.spines[['right', 'top', 'bottom']].set_visible(False)
    ax.spines[['right', 'top', 'bottom']].set_visible(False)

    # grid and horizontal line
    ax.axhline(0, color='lightgrey', linewidth=2, linestyle='--')



    # x axis label
    xlabels = config.labels
    xticks  = np.arange(len(xlabels))
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
    ax.set_ylabel(ylabel)
    ax.set_xlabel(config.xlabel)

    # legend
    leg = plt.legend(ncol=2, fontsize=15)#loc = (0.8, 0.7)
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_color('white')
    #leg.get_frame().set_alpha(0.)

    # save the plot
    fig.subplots_adjust(left=0.15)
    fig.savefig(f'{folder_out}/evolution_{figname}.png', dpi=300)
    fig.savefig(f'{folder_out}/evolution_{figname}.pdf', dpi=300)

    plt.close()




