import os
import sys

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

'''
    Use this script to calculate gradient between
    gw-wells where hydrographs are provided, and the
    distance between them is known. Script plots a cloud
    of gradient points for each pair of wells given
    and optionally dispays a trendline

    Specify distance in function <plot()>
    See other inputs in __main__
'''


def plot(df, df_names, legendlabels=[None], saveName=None):
    """
        df           - PandasDataFrame timeseries for original hydrographs
        df_names     - list with column names
        saveName     - None, or string with figure name to be saved
        legendlabels - List of legendnames or [None]. If default ([None]) - standart names are used
    """

    distance_W_GW2   = 46.5  # this parameter has been found by regression analysis....
    distance_GW2_GW3 = 9.49  # this has been calculated through coordinates
    distance_GW3_GW4 = 13.6  # this has been calculated through coordinates
    
    print 'calculating gradient....', df_names[-1], '-', df_names[0]
    df['gradient_W_GW2'] = (df[df_names[-1]] - df[df_names[0]])/distance_W_GW2
    
    print 'calculating gradient....', df_names[0], '-', df_names[1]
    df['gradient_GW2_GW3'] = (df[df_names[0]] - df[df_names[1]])/distance_GW2_GW3
    
    print 'calculating gradient....', df_names[1], '-', df_names[2]
    df['gradient_GW3_GW4'] = (df[df_names[1]] - df[df_names[2]])/distance_GW3_GW4
    
    plot_pandas.plot_pandas_scatter(df, x=['W_1_averaging3', 'W_1_averaging3', 'W_1_averaging3'],
                y=['gradient_W_GW2', 'gradient_GW2_GW3', 'gradient_GW3_GW4'], saveName=saveName,
                xlabel='Mean river water level [m AMSL]', title='Mean Hydraulic Gradient VS. Mean River Water-Level',
                ylabel='Mean hydraulic gradient [-]', legendlabels=legendlabels,
                trendlinemode=1, ylim=[-0.015, 0.015], xlim=[-0.5, 2.5])



if __name__ == '__main__':
    # ---------------------------------------
    # user inputs
    # ---------------------------------------

    # SPECIFY INPUTS IN FUNCTION plot() !!!
    # ESPECIALLY DISTANCE BETWEEN WELLS !!!

    file_folder = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name   = 'Farge_mean_after_Serfes1991.csv'
    figure_name = 'out/figure.pdf'
    col_names   = ['GW_2_averaging3', 'GW_3_averaging3', 'GW_4_averaging3', 'W_1_averaging3']  # column names in dataframe to be loaded... see code!
    
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------


    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    fign = os.path.abspath(os.path.join(path, figure_name))

    # load data into pandas.dataframe...
    data = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal=',', na_values=['---'])

    # plotting...
    if _sns:
        with sns.axes_style("whitegrid"):
            plot(data, col_names, saveName=None)
    else:
        plot(data, col_names, saveName=None)
