import os
import sys
import inspect
import matplotlib.pyplot as plt
import datetime
import seaborn as sns


# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import process2pandas


"""
This script is useful for two things:
    1) Plotting together all hydrographs
    2) [OPTIONAL] Plotting on top of it scatter points of previously found extremums

Note the format of files that have been created...
Data handling is performed with PANDAS module
"""


def plot(df, saveName=None, extrem=None,
    axeslabel_fontsize=10., title_fontsize=20., axesvalues_fontsize=10., annotation_fontsize=10., legend_fontsize=8.):
    """
        df       - pandas.DataFrame timeseries for original hydrographs
        extrem   - list with pandas.Series with points of extremums
        saveName - None, or string with figure name to be saved
    """

    print "plotting timeseries data..."
    fig = plt.figure(tight_layout=True)
    
    ax = fig.add_subplot(111)
    df.plot(colormap="jet_r", ax=ax,  marker='x', title="Farge: Measured water level in observation wells and river Weser")


    if extrem:
        print "plotting low-high tide scatter data..."
        # if we have extrem.... we want to plot them with same color
        handles, labels = ax.get_legend_handles_labels()
        colors = list()
        for h in handles:
            colors.append(h.get_color())
        if len(colors) != len(extrem):
            raise IndexError("Number of hydrographs do not correspond to number of passed extrem. Cannot get proper colors. Do hardcode quickly")
        i = 0
        for a, c in zip(extrem, colors):
            i += 1
            print "\t>>> {0}/{1}".format(i, len(extrem))
            for item, marker in zip(a, ['o', 's']):  # a = list( hightide, lowtide)
                item.plot(x='datetime', y='y', ax=ax, marker=marker, lw=2., style='.', markeredgecolor='black', markeredgewidth=0.4, color=c, legend=False)

    #ax.set_xlim([datetime.date(2015, 1, 26), datetime.date(2015, 1, 30)])
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[0:7], labels[0:7], fontsize=legend_fontsize)
    ax.grid(True, which='major')
    ax.set_title("Measured water level in observation wells and river Weser", fontsize=title_fontsize)
    ax.set_ylabel("m AMSL", fontsize=axeslabel_fontsize)
    ax.set_xlabel("", fontsize=axeslabel_fontsize)
    ax.tick_params(axis='both', which="both", labelsize=axesvalues_fontsize)


    #figManager = plt.get_current_fig_manager()
    #figManager.window.showMaximized()

    if saveName:
        fig.savefig(saveName, dpi=300, tight_layout=True, format='pdf')
        print 'saving figure... :', saveName
    plt.show()


if __name__ == '__main__':
    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    
    file_folder       = '../data/SLICED_171020141500_130420150600/hydrographs/'
    amplitudes_folder = '../data/SLICED_171020141500_130420150600/amplitude/'
    file_name         = 'Farge-ALL_10min.all'
    
    figure_name = 'out/figure.pdf'
    ampl_fnames = ['GW_1_amplitude.all', 'GW_2_amplitude.all', 'GW_3_amplitude.all', 'GW_4_amplitude.all', 'GW_5_amplitude.all', 'GW_6_amplitude.all', 'W_1_amplitude.all']
    
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    fign = os.path.abspath(os.path.join(path, figure_name))

    # read extremum-data for all wells into pd.dataframe and save it to list...
    AMPLITUDES = list()
    for ampl_fn in ampl_fnames:
        a_fn = os.path.abspath(os.path.join(path, amplitudes_folder, ampl_fn))
        ht, lt, amp = process2pandas.read_amplitudes_into_pandas(a_fn)
        AMPLITUDES.append([ht, lt])

    
    # read hydrograph-data into pd.dataframe
    data = process2pandas.read_hydrographs_into_pandas(fname, datetime_indexes=True)
    
    # now plot figure...
    # ---------------------
    #AMPLITUDES = None
    #fign = None

    with sns.axes_style("whitegrid"):
        plot(data, saveName=fign, extrem=AMPLITUDES,
            axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.)
