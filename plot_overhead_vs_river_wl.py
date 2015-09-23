''' Scripts reads data from excel file:
    - extremum points of river hydrograph (high/low tide)
    - overhead in the gw wells at the time of river high/low tide
    
    and plots one againt another as a scatter plot

    Can also calculate and plot trendlines(!!!) in three
    different modes ( see docstring of plot_pandas_scatter_special1() function)
'''

import os
import sys
import inspect

try:
    import seaborn as sns
    _sns = True
except:
    _sns = False


# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas
import plot_pandas



if __name__ == '__main__':
    # --------------------------------------------------------------------------------------
    # user inputs
    # --------------------------------------------------------------------------------------
    file_folder       = '../data/SLICED_171020141500_130420150600/'
    file_name         = 'output_tidal_efficiency_with_E.xls'
    

    HYDR_VALS = dict()
    HYDR_VALS['MThw']   =  2.28
    HYDR_VALS['MTnw']   = -1.57
    HYDR_VALS['NNTnw']  = -3.42
    HYDR_VALS['HThw']   =  4.99
    HYDR_VALS['MspTnw'] = -1.87

    X_name1 = 'Low Tide [m AMSL]'   # pointers to excel table colums with river data
    X_name2 = 'High Tide [m AMSL]'  # pointers to excel table colums with river data
    
    # column names in excel file , which represent overhead at low-tide
    overhead_names1 = list(
        ['Overhead_gw1_at_W_low[m]',
        'Overhead_gw2_at_W_low[m]',
        'Overhead_gw3_at_W_low[m]',
        'Overhead_gw4_at_W_low[m]',
        'Overhead_gw5_at_W_low[m]',
        'Overhead_gw6_at_W_low[m]']
    )
    # column names in excel file , which represent overhead at high-tide
    overhead_names2 = list(
        ['Overhead_gw1_at_W_high[m]',
        'Overhead_gw2_at_W_high[m]',
        'Overhead_gw3_at_W_high[m]',
        'Overhead_gw4_at_W_high[m]',
        'Overhead_gw5_at_W_high[m]',
        'Overhead_gw6_at_W_high[m]']
    )
    # --------------------------------------------------------------------------------------
    # END user inputs END
    # --------------------------------------------------------------------------------------

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    
    mode = 'XLS'
    if mode == 'XLS':
        # load data into pandas.dataframe
        data = process2pandas.read_xlx_into_pandas(fname, sheetname=0)

        for Y_name1, Y_name2 in zip(overhead_names1, overhead_names2):
            if _sns:
                with sns.axes_style("whitegrid"):
                    plot_pandas.plot_pandas_scatter_special1(data, x=[X_name1, X_name2], y=[Y_name1, Y_name2], saveName=None, HYDR_VALS=HYDR_VALS,
                        xlabel='River water level [m AMSL]', title='OVERHEAD IN OBSERVATION WELL VS RIVER WATERLEVEL', ylabel='Overhead [m]',
                        trendlinemode=3, xlim=[-4., 3.5])
            else:
                    plot_pandas.plot_pandas_scatter_special1(data, x=[X_name1, X_name2], y=[Y_name1, Y_name2], saveName=None, HYDR_VALS=HYDR_VALS,
                        xlabel='River water level [m AMSL]', title='OVERHEAD IN OBSERVATION WELL VS RIVER WATERLEVEL', ylabel='Overhead [m]',
                        trendlinemode=3, xlim=[-4., 3.5])
