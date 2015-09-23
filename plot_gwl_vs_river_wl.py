''' Scripts reads data from excel file:
    - hydrograph of gw wells
    - hydrograph of River
    and plots one againt another as a scatter plot

    Can also calculate and plot trendlines(!!!) in three
    different modes ( see docstring of plot_pandas_scatter() function)
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

    # SPECIFY PARANS TO FUNCTION plot_pandas_scatter() !!!
    file_folder       = '../data/SLICED_171020141500_130420150600/'
    file_name         = 'output_tidal_efficiency_with_E.xls'
    
    figure_name = 'out/figure.pdf'
    save_fnames = ['GW_1', 'GW_2', 'GW_3', 'GW_4', 'GW_5', 'GW_6']
    
    mode = 'XLS'  # requires module <xlrd>, possible to extend to work with CSV
    trendlinemode = 2  # see doc-string to function <plot_pandas_scatter()>


    X_name1 = 'Low Tide [m AMSL]'   # pointers to excel table colums with river data
    X_name2 = 'High Tide [m AMSL]'  # pointers to excel table colums with river data

    # column names in excel file , which represent overhead at low-tide
    overhead_names1 = list(
        ['H_gw1_at_W_low[m AMSL]',
        'H_gw2_at_W_low[m AMSL]',
        'H_gw3_at_W_low[m AMSL]',
        'H_gw4_at_W_low[m AMSL]',
        'H_gw5_at_W_low[m AMSL]',
        'H_gw6_at_W_low[m AMSL]']
    )
    # column names in excel file , which represent overhead at high-tide
    overhead_names2 = list(
        ['H_gw1_at_W_high[m AMSL]',
        'H_gw2_at_W_high[m AMSL]',
        'H_gw3_at_W_high[m AMSL]',
        'H_gw4_at_W_high[m AMSL]',
        'H_gw5_at_W_high[m AMSL]',
        'H_gw6_at_W_high[m AMSL]']
    )
    figure_savename = list([
        'GW_1_vs_W_1.png',
        'GW_2_vs_W_1.png',
        'GW_3_vs_W_1.png',
        'GW_4_vs_W_1.png',
        'GW_5_vs_W_1.png',
        'GW_6_vs_W_1.png']
    )
    # --------------------------------------------------------------------------------------
    # END user inputs END
    # --------------------------------------------------------------------------------------

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    fign = os.path.abspath(os.path.join(path, figure_name))

    if mode == 'XLS':  #  WORKING WITH EXCEL SHEET
        # read excel file into pandas dataframe
        data = process2pandas.read_xlx_into_pandas(fname, sheetname=0)

        for Y_name1, Y_name2, sn in zip(overhead_names1, overhead_names2, figure_savename):
            sn = os.path.abspath(os.path.join(path, 'out/', sn))
            plot_pandas.plot_pandas_scatter(data, x=[X_name1, X_name2], y=[Y_name1, Y_name2], saveName=None, trendlinemode=trendlinemode,
                xlabel='River water level [m AMSL]', title='WATER LEVEL IN OBSERVATION WELL VS RIVER WATERLEVEL', ylabel='Well water level [m AMSL]')
                
