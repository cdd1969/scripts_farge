''' Read CSV data into pandas dataframe and then plot
    two subplots:
        1) mean water water-level
        2) gradient between those wells (used in punkt 1 )
'''

import os
import sys

import matplotlib.pyplot as plt
try:
    import seaborn as sns
    _sns = True
except:
    _sns = False


# use this if you want to include modules from a subfolder
import inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas
import plot_pandas


def plot(df, df_names, legend_names, saveName=None):
    """
        df   - PandasDataFrame timeseries for original hydrographs
        names - list with column names
        legend_names - list with strings
    """
    print "plotting timeseries data..."
    fig = plt.figure(tight_layout=False, figsize=(11.69, 8.27))
    
    # ---------------------------
    # SUBPLOT 1
    # ---------------------------
    ax1 = fig.add_subplot(211)
    plot_pandas.plot_mean_waterlevel(df, df_names, legend_names, saveName=saveName, ax=ax1)
    
    # ---------------------------
    # SUBPLOT 2
    # ---------------------------

    ax2 = fig.add_subplot(212)
    distance_W_GW2   = 46.5  # this parameter has been found by regression analysis....
    distance_GW2_GW3 = 9.49  # this has been calculated through coordinates
    distance_GW3_GW4 = 13.6  # this has been calculated through coordinates
    
    print 'calculating gradient....', df_names[-1], '-', df_names[0]
    df['gradient_W_GW2'] = (df[df_names[-1]] - df[df_names[0]])/distance_W_GW2
    
    print 'calculating gradient....', df_names[0], '-', df_names[1]
    df['gradient_GW2_GW3'] = (df[df_names[0]] - df[df_names[1]])/distance_GW2_GW3
    
    print 'calculating gradient....', df_names[1], '-', df_names[2]
    df['gradient_GW3_GW4'] = (df[df_names[1]] - df[df_names[2]])/distance_GW3_GW4
    
    df['gradient_W_GW2'].plot(  ax=ax2, legend=True, title="Farge: Mean hydraulic gradients", lw=0.8)
    df['gradient_GW2_GW3'].plot(ax=ax2, legend=True, title="Farge: Mean hydraulic gradients", lw=0.8)
    df['gradient_GW3_GW4'].plot(ax=ax2, legend=True, title="Farge: Mean hydraulic gradients", lw=0.8)

    handles, labels = ax2.get_legend_handles_labels()
    for i, l_name, dist in zip([0, 1, 2], labels, [distance_W_GW2, distance_GW2_GW3, distance_GW3_GW4]):
        labels[i] = l_name+': distance = {0} m'.format(dist)
    ax2.legend(handles, labels)

    ax2.grid(True, which='major')
    ax2.set_ylabel("Mean hydraulic gradient [-]")
    ax2.set_xlabel("Datetime")
    ax2.set_ylim([-0.015, 0.015])
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()


    if saveName:
        fig.savefig(saveName, dpi=300, tight_layout=True)#, format='pdf')
        print 'saving figure... :', saveName
    plt.show()


if __name__ == '__main__':
    # --------------------------------------------------------------------------------------
    # user inputs
    # --------------------------------------------------------------------------------------
    file_folder  = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name    = 'Farge_mean_after_Serfes1991.csv'
    
    col_names    = ['GW_2_averaging3', 'GW_3_averaging3', 'GW_4_averaging3', 'W_1_averaging3']
    legend_names = ['GW_2 mean water-level', 'GW_3 mean water-level', 'GW_4 mean water-level', 'W_1 mean water-level']
    # --------------------------------------------------------------------------------------
    # END user inputs END
    # --------------------------------------------------------------------------------------


    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )

    data = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal=',', na_values=['---'])

    if _sns:
        with sns.axes_style("whitegrid"):
            plot(data, col_names, legend_names , saveName=None)
    else:
        plot(data, col_names, legend_names , saveName=None)
