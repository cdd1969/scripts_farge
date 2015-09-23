''' Plots all time-averaged hydrographs together.
'''

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


if __name__ == '__main__':
    # --------------------------------------------------------------------------------------
    # user inputs
    # --------------------------------------------------------------------------------------
    file_folder  = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name    = 'Farge_mean_after_Serfes1991.csv'
    
    col_names    = ['GW_1_averaging3', 'GW_2_averaging3', 'GW_3_averaging3', 'GW_4_averaging3', 'GW_5_averaging3', 'GW_6_averaging3', 'W_1_averaging3']
    legend_names = ['GW_1 mean water-level', 'GW_2 mean water-level', 'GW_3 mean water-level', 'GW_4 mean water-level', 'GW_5 mean water-level', 'GW_6 mean water-level', 'W_1 mean water-level']
    # --------------------------------------------------------------------------------------
    # END user inputs END
    # --------------------------------------------------------------------------------------

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )

    data = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal=',', na_values=['---'])

    if _sns:
        with sns.axes_style("whitegrid"):
            plot_pandas.plot_mean_waterlevel(data, col_names, legend_names , saveName=None)
    else:
        plot_pandas.plot_mean_waterlevel(data, col_names, legend_names , saveName=None)
