''' Script processes hydrograph and draws its
     + original signal, PDF, CDF
     + calculated mean and STD
    Plots this info on a nice figure
'''
import os
import sys
import numpy as np
import inspect
import seaborn as sns

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import plot_pandas
import process2pandas



def read_waterlevel_values(fname, wtype=None, usecols=None, skiprows=3, delimiter=';'):
    """
        type = 'amplitude'
        type = 'high_tide'
        type = 'low_tide'
        type = 'waterlevel'
        type = None   ==> 'usecols' is used
    """
    if wtype not in ['amplitude', 'high_tide', 'low_tide', 'waterlevel', None]:
        raise KeyError("Invalid type specified, should be one from list: ['amplitude', 'high_tide', 'low_tide', 'waterlevel', None]")

    USECOLS = dict()
    USECOLS['amplitude'] = 4
    USECOLS['high_tide'] = 1
    USECOLS['low_tide'] = 1
    USECOLS['waterlevel'] = 1
    
    if wtype is None:
        if usecols:
            wtype = 'None'
            USECOLS['None'] = usecols
        else:
            raise KeyError("wtype is None ==> using USECOLS. Found None. USECOLS should be int")

    a = np.genfromtxt(fname, delimiter=delimiter, skip_header=skiprows, usecols=USECOLS[wtype], autostrip=True)
    return a


def read_folder():
        # this function is usefull for amplitudes
        file_folder = '../data/SLICED_171020141500_130420150600/amplitude/'
        river_wl_fname = 'W_1_amplitude.all'
        wtype = "amplitude"
        wtype = None


        file_folder = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), file_folder) )
        fnames = [ f for f in os.listdir(file_folder) if f.endswith(".all") ]
        path = os.path.dirname(sys.argv[0])


        y2 = read_waterlevel_values(os.path.abspath(os.path.join(path, file_folder, river_wl_fname) ), wtype=wtype, usecols=3)

        for fname in fnames:
            data_fname = os.path.abspath(os.path.join(path, file_folder, fname) )
            print data_fname
            
            
            y = read_waterlevel_values(data_fname, wtype=wtype, usecols=3)

            fig_name = os.path.abspath(os.path.join(path, file_folder, 'distribution_LOWTIDE_'+os.path.splitext(fname)[0]+'___-2.5_2.0.jpg') )
            plt_title = '{0}: Original signal LOW TIDE'.format(fname)
            with sns.axes_style("whitegrid"):
                plot_pandas.plot_statistical_analysis(y, data2=y2, save=True, figurename=fig_name, plot_title=plt_title, ylims=[-2.5, 2.0],
                    ylabel1="m AMSL",                                     xlabel1="number of data points",
                    ylabel2="Normal PDF", xlabel2="m AMSL",
                    ylabel3="Normal CDF",      xlabel3="m AMSL",
                    papersize='A4',
                    axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.)



def read_file():
    # this function is usefull for hydrographs from 1n file
    file_folder = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name = 'Farge-ALL_10min.all'
    wtype = "waterlevel"
    usecols = [1, 2, 3, 4, 5, 6, 7]
    colnames = ['GW1', 'GW2', 'GW3', 'GW4', 'GW5', 'GW6', 'W1']
    wtype = "waterlevel"

    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    print fname

    

    y2 = read_waterlevel_values(fname, usecols=[7], skiprows=2, delimiter=';')
    for col, name in zip(usecols, colnames):
        print name, col
        fig_name = os.path.abspath(os.path.join(path, file_folder, 'distribution_hydrograph_'+name+'__-3._5.0.pdf') )
        

        #y = read_waterlevel_values(fname, usecols=[col], skiprows=2, delimiter=';')
        y = process2pandas.read_hydrographs_into_pandas(fname, datetime_indexes=True, log=False, delimiter=';', usecols=[0, col], skiprows=1)
        #print y
        #print 'mean, std:', plot_pandas.calculate_mean_std(y)
        
        

        if not col == 7:
            data_river = y2
            pass
        else:
            data_river = None

        data_river = None
        

        plt_title = '{0}: Measured waterlevel'.format(name)
        with sns.axes_style("whitegrid"):
            plot_pandas.plot_statistical_analysis(y, data2=data_river, save=False, figurename=fig_name, plot_title=plt_title, ylims=[-3., 5.0],
                    ylabel1="m AMSL",                                     xlabel1="number of data points",
                    ylabel2="Normal PDF", xlabel2="m AMSL",
                    ylabel3="Normal CDF",      xlabel3="m AMSL",
                    papersize='A4',
                    axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.)


if __name__ == '__main__':
        read_file()
        #read_folder()
