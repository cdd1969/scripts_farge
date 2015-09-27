import os
import sys
import inspect
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

import scipy
import scipy.stats
import matplotlib.lines as mlines


# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas
import plot_pandas




if __name__ == '__main__':

    file_folder       = '../analysis/timelag/MEANi/'
    file_name         = 'timelag_calculated_for_every_cycle_MEANi.xlsx'
    
    figure_name = 'out/figure'
    save_fnames = ['GW_1', 'GW_2', 'GW_3', 'GW_4', 'GW_5', 'GW_6']
    

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    



    #-------------------------------------------------------------------
    #  WORKING WITH EXCEL SHEET
    #-------------------------------------------------------------------

    print 'reading data from XLX'
    data = process2pandas.read_xlx_into_pandas(fname, sheetname='Sheet1')
    #-------------------------------------------------------------------
    #  ACTUALLY PLOTTING
    #-------------------------------------------------------------------
    for well in save_fnames:
        print 'plotting... >>>', well
        fign = os.path.abspath(os.path.join(path, 'out', 'timelag_cyclic_statistics_'+well+'.pdf'))


        with sns.axes_style("whitegrid"):
            plot_pandas.plot_statistical_analysis(data[well], data2=None, save=False, figurename=fign,  plot_title='Timelag calculated for each out of 344 tidal cycles: {0}'.format(well),
                    ylims=None,
                    ylabel1="Timelag [min]",                              xlabel1="Tidal cycles",
                    ylabel2="Normal PDF", xlabel2="Timelag [min]",
                    ylabel3="Normal CDF",      xlabel3="Timelag [min]",
                    papersize='A4',
                    axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.)
