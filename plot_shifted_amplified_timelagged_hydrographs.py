''' Plot signal for each well separately and compare on one canvas:
        - original hydrograph
        - amplified hydrograph (apply E)
        - shifted and amplified hydrograph (apply tlag + E)
'''
import os
import sys

import pandas as pd
import datetime
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


def plot(df1, df2, name1, name2, saveName=None, mode='min', river_df=None):
    """
        df   - PandasDataFrame timeseries for original hydrographs
        amplitudes - list with pandas.Series with points of amplitudes
    """
    print "plotting timeseries data..."
    fig = plt.figure(tight_layout=True)
    
    ax = fig.add_subplot(111)
    df1[name1].plot(ax=ax, legend=True, title="Filtered (shifted, amplified and timelagged) piezometric records for observation wells", lw=1.2)  # river
    df2[name2].plot(ax=ax, legend=True, color="r", lw=1.2)  # filtered

    if mode == 'max':
        shortname = name2[-4:]
        df1[name2].plot(ax=ax, legend=True, color='k', lw=0.5)  # shifter and amplified
        df1[shortname].plot(ax=ax, legend=True, color="g", lw=0.8)  # original

        """
        print 'making erskine'
        df1['erskine'] = df1[shortname]
        for time_index, value_h in df1[shortname].iteritems():
            timelag_datetime = datetime.timedelta(minutes=25)
            T = river_df.loc[(time_index-timelag_datetime)][0]
            df1.ix[time_index, 'erskine'] = value_h - 0.25218*(T-df1[name1].mean())
        

        df1['erskine'].plot(ax=ax, legend=True, color="y", lw=1.2)  # erskine
        n5 = '{0}: '.format(shortname+':  shifted, amplified, lagged ERSKINE')

        print 'finished erskine'
        """
        handles, labels = ax.get_legend_handles_labels()
        n1 = '{0}: mean = {1:.2f}'.format(name1, df1[name1].mean())
        n2 = '{0}: mean = {1:.2f}'.format(shortname+': shifted, amplified, lagged', df2[name2].mean())
        n3 = '{0}: mean = {1:.2f}'.format(shortname+': shifted, amplified', df1[name2].mean())
        n4 = '{0}: mean = {1:.2f}'.format(shortname+': original', df1[shortname].mean())

        labels = [n1, n2, n3, n4, ]  # n5]
        ax.legend(handles, labels)



    ax.grid(True, which='minor')
    ax.set_ylabel("m AMSL")
    ax.set_xlabel("Datetime")
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    #py.iplot_mpl(fig, filename='test')

    if saveName:
        fig.savefig(saveName, dpi=300, tight_layout=True)#, format='pdf')
        print 'saving figure... :', saveName
    plt.show()


if __name__ == '__main__':
    # --------------------------------------------------------------------------------------
    # user inputs
    # --------------------------------------------------------------------------------------
    file_folder = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name   = 'Farge-ALL_10min.all'
    river_name  = 'Farge-W1_1min.all'
    figure_path = 'out/'

    E_GW_1 = 0.25218  #  Tidal Efficiency [-]
    E_GW_2 = 0.31209  #  Tidal Efficiency [-]
    E_GW_3 = 0.24625  #  Tidal Efficiency [-]
    E_GW_4 = 0.17867  #  Tidal Efficiency [-]
    E_GW_5 = 0.33024  #  Tidal Efficiency [-]
    E_GW_6 = 0.36874  #  Tidal Efficiency [-]

    t_lag_GW_1 = 25  # in minutes
    t_lag_GW_2 = 12  # in minutes
    t_lag_GW_3 = 16  # in minutes
    t_lag_GW_4 = 25  # in minutes
    t_lag_GW_5 = 12  # in minutes
    t_lag_GW_6 = 35  # in minutes
    # --------------------------------------------------------------------------------------
    # END user inputs END
    # --------------------------------------------------------------------------------------

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    RIVER_fname = os.path.abspath(os.path.join(path, file_folder, river_name) )

    # loading data from text file
    RIVER_data = process2pandas.read_mean_hydrographs_into_pandas(RIVER_fname, datetime_indexes=True, decimal='.',  skiprows=4)
    data = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal='.',  skiprows=1)

    # amplifying
    data['filtered_GW_1'] = data['W_1'].mean() + (data['GW_1'] - data['GW_1'].mean()) / E_GW_1
    data['filtered_GW_2'] = data['W_1'].mean() + (data['GW_2'] - data['GW_2'].mean()) / E_GW_2
    data['filtered_GW_3'] = data['W_1'].mean() + (data['GW_3'] - data['GW_3'].mean()) / E_GW_3
    data['filtered_GW_4'] = data['W_1'].mean() + (data['GW_4'] - data['GW_4'].mean()) / E_GW_4
    data['filtered_GW_5'] = data['W_1'].mean() + (data['GW_5'] - data['GW_5'].mean()) / E_GW_5
    data['filtered_GW_6'] = data['W_1'].mean() + (data['GW_6'] - data['GW_6'].mean()) / E_GW_6


 
    for n1, t_lag in zip(['GW_1',     'GW_2',     'GW_3',    'GW_4',      'GW_5',     'GW_6'],
                         [t_lag_GW_1, t_lag_GW_2, t_lag_GW_3, t_lag_GW_4, t_lag_GW_5, t_lag_GW_6]):
        
        figname = os.path.abspath(os.path.join(path, figure_path, 'hydrograph_filtered___'+n1+'.png'))
        figname = None
        print n1

        timelag_datetime = datetime.timedelta(minutes=t_lag)
        data_timelagged = data.set_index(pd.DatetimeIndex(data['filtered_'+n1].index - timelag_datetime))  # applying timelag
        
        plot(data, data_timelagged, 'W_1', 'filtered_'+n1, saveName=figname, mode='max', river_df=RIVER_data)
        print '-'*50

