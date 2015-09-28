import os
import sys

import matplotlib.pyplot as plt
import seaborn as sns


# use this if you want to include modules from a subfolder
import inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas


"""
This script is useful for:
    1) Plotting hydrograph and showing on top the time-averaged line (averaged afer Serfes 1991)

Data handling is performed with PANDAS
"""


def plot(df, name1, name2, saveName=None, ylim=None,
        axeslabel_fontsize=10., title_fontsize=20., axesvalues_fontsize=10., annotation_fontsize=10., legend_fontsize=8.):
    """

        df       - pandas.DataFrame timeseries for original hydrographs
        name1    - name of the column (in passed <df> pandas.dataframe), where data for measured water level is stored
        name2    - name of the column (in passed <df> pandas.dataframe), where data for time-averaged water level is stored
        saveName - None, or string with figure name to be saved
        ylim     - None, or list for y-limits [ymin, ymax] of the plot. (i.e. ylim=[0., 1.])
    """
    print "plotting timeseries data..."
    fig = plt.figure(tight_layout=True, figsize=(8.27, 5.83))
    ax = fig.add_subplot(111)
    
    df[name1].plot(ax=ax, legend=True, title="Measured water level")
    df[name2].plot(ax=ax, legend=True, title="Farge: Measured water level and averaging after Serfes(1991)", color="k")

    handles, labels = ax.get_legend_handles_labels()
    labels[1] = labels[0]+' averaged after Serfes(1991)'
    ax.legend(handles, labels, fontsize=legend_fontsize)

    ax.grid(True, which='major')
    ax.set_title("Measured water level and averaging after Serfes(1991)", fontsize=title_fontsize)
    ax.set_ylabel("m AMSL", fontsize=axeslabel_fontsize)
    ax.set_xlabel("", fontsize=axeslabel_fontsize)
    ax.tick_params(axis='both', labelsize=axesvalues_fontsize)
    if ylim: ax.set_ylim(ylim)


    

    #figManager = plt.get_current_fig_manager()
    #figManager.window.showMaximized()

    #py.iplot_mpl(fig, filename='test')

    if saveName:
        fig.savefig(saveName, dpi=300, tight_layout=True)#, format='pdf')
        print 'saving figure... :', saveName
    plt.show()


if __name__ == '__main__':
    # ---------------------------------------
    # user inputs
    # ---------------------------------------

    file_folder = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name   = 'Farge_mean_after_Serfes1991.csv'
    figure_path = 'out/'

    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------

    
    path  = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )

    # loading data into pandas dataframe
    data = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal=',', na_values=['---'])

    # plotting
    for n1 in ['GW_1', 'GW_2', 'GW_3', 'GW_4', 'GW_5', 'GW_6', 'W_1']:
        figname = os.path.abspath(os.path.join(path, figure_path, 'hydrograph_+mean_'+n1+'.pdf'))
        #figname = None
        with sns.axes_style("whitegrid"):
            plot(data, n1, n1+'_averaging3', saveName=figname, ylim=[-3., 5.],
                axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.)


