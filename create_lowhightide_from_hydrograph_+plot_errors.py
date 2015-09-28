import os
import sys
import numpy as np
from pylab import *
from matplotlib.dates import date2num, num2date
from datetime import datetime, timedelta
import scipy
import scipy.signal
import matplotlib.pyplot as plt
try:
    import seaborn as sns
    _sns = True
except:
    _sns = False

def check_data_to_be_correct(filename, skip_header=3):
    with open(filename, mode='r') as f:
        fc = f.readlines()
        f.close()

    for i, line in enumerate(fc):
        if i < skip_header-1:
            continue
        ll = line.split(';')
        for j in xrange(1, len(ll)):
            if ll[j] in ['\n', '', "\r\n"]:
                continue
            try:
                ll[j] = float(ll[j])
            except:
                print 'line:', i, '; ', ll
                print ll[j]
                raise ValueError('could not convert string to float')
    print 'Data has no errors...'



def load_timeseries_from_csv_file(filename, usecols=None, skiprows=0, delimiter=None, datetime_fmt='%d.%m.%Y %H:%M', fillvalue=-999, return_mode=1):
    a = np.loadtxt(filename, delimiter=delimiter, skiprows=skiprows, usecols=usecols,  dtype={'names': ('time', 'GW_level'), 'formats': ('S20', 'f4')})

    if return_mode == 1:
        return a

    elif return_mode == 2:
        # this is a hardcode part....
        time = np.zeros(len(a))
        wl = np.zeros(len(a))

        for i in xrange(len(a)):
            time[i] = convert_str_to_datenum(a[i][0], datetime_fmt=datetime_fmt, log=False)
            if a[i][1] == fillvalue:
                wl[i] = np.nan
            else:
                wl[i] = a[i][1]
        return [time, wl]




def convert_str_to_datenum(string, days_to_skip=0, datetime_fmt='%d.%m.%Y %H:%M', log=False):
    if log: print 'pure date:', datetime.strptime(string.strip(), datetime_fmt)
    if log: print 'timedelta', timedelta(days=days_to_skip)
    
    DateTime = datetime.strptime(string.strip(), datetime_fmt) - timedelta(days=days_to_skip)
    DateNum = date2num(DateTime)
    
    if log: print 'returns:', DateNum
    return DateNum


def remove_regions_from_extremums(extremums_array, log=False):
    """
        extremums_array  - is produced with scipy.signal.argrelextrema()[0]
    """
    
    # check minimums
    region = list()
    new_extremums_array = list()
    for i, v in enumerate(extremums_array):
        # TREATING PERSONALLY LAST VALUE
        if i == len(extremums_array)-1:
            if region:
                region.append(extremums_array[i])
                # now process the region
                middle_of_region = sum(region)/len(region)
                if log: print 'region:', region
                if log: print 'middle_of_region:', middle_of_region
                new_extremums_array.append(middle_of_region)
                region = list()
            else:
                new_extremums_array.append(extremums_array[i])
            # exiting loop after appending last extremum
            continue
        
    
        # if not last value....
        if extremums_array[i+1] == extremums_array[i]+1 :  # neighbour indexes
            region.append(extremums_array[i])
        else:
            if region:
                region.append(extremums_array[i])
                # now process the region
                middle_of_region = sum(region)/len(region)
                if log: print 'region:', region
                if log: print 'middle_of_region:', middle_of_region
                new_extremums_array.append(middle_of_region)
                region = list()
            else:
                new_extremums_array.append(extremums_array[i])
    if log:
        print '-'*50
        print 'old array:\n', extremums_array
        print 'new array:\n', new_extremums_array
        print 'Lenght decreased from {0} to {1}'.format(len(extremums_array), len(new_extremums_array))
        print '-'*50

    return new_extremums_array


def check_extremums_dt(extremum_array, time_array, tau=12.42/24., prc=1./24., log=False):
    not_correct_dt = list()
    for i in xrange(len(extremum_array)):
        if i == 0:
            continue
        t_prev = time_array[extremum_array[i-1]]
        t_cur = time_array[extremum_array[i]]

        if  tau-prc <= (t_cur - t_prev) and (t_cur - t_prev) <= tau+prc:
            pass
        else:
            not_correct_dt.append([extremum_array[i-1], extremum_array[i]])
            if log: print '{2}) Differece in time is not corresponding to tidal cycle:\ndt={0}\nt_cycle={1}'.format((t_cur - t_prev), tau, i)
            if log: print ' time_index_current minima = {0}\n time_index previous minima = {1}'.format(extremum_array[i], extremum_array[i-1])
    return not_correct_dt




def plot_extremums(t, wl, low_tide_indexes, high_tide_indexes, time_errors_high=None, time_errors_low=None, date_xaxis=False, dt=None, plot_title="",
                    axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.):
    """
        t  - time array
        wl  - waterlevel original array
        low/high_tide_indexes - arrays with indexes of low/high tides
    """
   
    wl_low = np.array([wl[i] for i in low_tide_indexes])
    wl_high = np.array([wl[i] for i in high_tide_indexes])
    t_low = np.array([t[i] for i in low_tide_indexes])
    t_high = np.array([t[i] for i in high_tide_indexes])
    


    if not date_xaxis:
        plt.plot(np.arange(len(t)), wl, color='b', label='original signal', lw='0.5')
        plt.scatter(low_tide_indexes, wl_low, color='k', label='low_tide')
        plt.scatter(high_tide_indexes, wl_high, color='g', label='high_tide')
        if time_errors_high:
            plt.plot(time_errors_high[0], [wl[time_errors_high[0][0]], wl[time_errors_high[0][1]]], color='r',
                        marker='s', lw='1.5', label='High tide Error\ndt > t(cycle)')
            for indexes in time_errors_high:
                plt.plot(indexes, [wl[indexes[0]], wl[indexes[1]]], color='r', marker='s', lw='1.5')
        if time_errors_low:
            plt.plot(time_errors_low[0], [wl[time_errors_low[0][0]], wl[time_errors_low[0][1]]], color='r',
                        marker='s', lw='1.5', label='Low tide Error\ndt > t(cycle)')
            for indexes in time_errors_low:
                plt.plot(indexes, [wl[indexes[0]], wl[indexes[1]]], color='r', marker='s', lw='1.5')
    
        plt.xlabel('number of data point')
        plt.xlim([-len(t)*.1, len(t)*1.1])

    if date_xaxis:
        plt.plot(t, wl, color='b', label='original signal', lw='0.5')
        plt.scatter(t_low, wl_low, color='k', label='low_tide')
        plt.scatter(t_high, wl_high, color='g', label='high_tide')
        
        if time_errors_high:
            plt.plot([t[time_errors_high[0][0]], t[time_errors_high[0][1]]], [wl[time_errors_high[0][0]], wl[time_errors_high[0][1]]],
                     color='r', marker='s', lw='1.5', label='High tide Error\nt(cycle) < dt < t(cycle)')
            for indexes in time_errors_high:
                time = [t[indexes[0]], t[indexes[1]]]
                plt.plot(time, [wl[indexes[0]], wl[indexes[1]]], color='r', marker='s', lw='1.5')
        if time_errors_low:
            plt.plot([t[time_errors_low[0][0]], t[time_errors_low[0][1]]], [wl[time_errors_low[0][0]], wl[time_errors_low[0][1]]],
                     color='r', marker='s', lw='1.5', label='Low tide Error\nt(cycle) < dt < t(cycle)')
            for indexes in time_errors_low:
                time = [t[indexes[0]], t[indexes[1]]]
                plt.plot(time, [wl[indexes[0]], wl[indexes[1]]], color='r', marker='s', lw='1.5')
    
        import matplotlib.dates as mdates
        t0 = t[0]-(t[-1]-t[0])*.1   # -10% of all range
        t1 = t[-1]+(t[-1]-t[0])*.1  # +10% of all range
        plt.xlim([t0, t1])
        plt.gca().xaxis_date()
        myFmt = mdates.DateFormatter('%b %d')
        plt.gca().xaxis.set_major_formatter(myFmt)


        #xticks(fontsize=20, rotation=45)
        xticks(fontsize=axesvalues_fontsize)
        yticks(fontsize=axesvalues_fontsize)

    plt.legend(fontsize=legend_fontsize)
    plt.title('{0}: Filtering LOW and HIGH tide value from signal'.format(plot_title), fontsize=title_fontsize)
    plt.ylabel('m AMSL', fontsize=axeslabel_fontsize)


    if dt:
        from matplotlib.patches import Rectangle
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        handles, labels = gca().get_legend_handles_labels()
        handles.append(extra)
        labels.append('\nt(cycle)={0:.2f}+-{1:.2f} h'.format(dt[0]*24., dt[1]*24. ) )
        gca().legend(handles, labels, fontsize=legend_fontsize)


    plt.show()





def find_LowHighTide_Amplitudes(time_array, wl_array, tau=12.42/24., prc=1./24., order=1, plot=False, log=False, datetime_fmt='%d.%m.%Y %H:%M', plot_title="",
                                axeslabel_fontsize=18., title_fontsize=20., axesvalues_fontsize=18., annotation_fontsize=18., legend_fontsize=18.):
    """
        This script should be used with data which has no missing regions. Although it will work with all data, but
        may produce inaccuraces. Missing values should be represented by np.nan in wl_array.


        time_array    - numpy array with datetime objects
        wl_array      - numpy array with measured values of waterlevel. Must have same lenght as time_array
        tau           - float, signal period in days
        prc           - indicates presicion value +- for comparing time diffrerence between found extremums
                        with tidal_cycle
        order         -  integer for scipy.signal.argrelextrema()
        plot          - boolean flag to show plot
        log           - boolean flag to show log

        # tidal cycle is aproximately 12h25min. Each timestep is 10 min => tidal cycle is 74.5 timesteps
        # therefore, maxima and minima will be filtered in a range of 73 to 76 timesteps from each other
        # for safety reasons lets take 720min
    """

    if len(time_array) != len(wl_array):
        raise ValueError('time and waterlevel arays should have equal lenght.\nGot: len(time)={0}, len(wl)={1}'.format( len(time_array), len(wl_array)))
    

    local_maximums = scipy.signal.argrelextrema(wl_array, np.greater_equal, order=order, mode='clip')[0]
    local_minimums = scipy.signal.argrelextrema(wl_array, np.less_equal, order=order, mode='clip')[0]
    
    local_maximums = remove_regions_from_extremums(local_maximums, log=log)
    local_minimums = remove_regions_from_extremums(local_minimums, log=log)

    errors_high = check_extremums_dt(local_maximums, time_array, tau=tau, prc=prc, log=log)
    errors_low = check_extremums_dt(local_minimums, time_array, tau=tau, prc=prc , log=log)
    
    if plot:
        with sns.axes_style("whitegrid"):
            plot_extremums(time_array, wl_array, local_minimums, local_maximums, time_errors_high=errors_high, time_errors_low=errors_low,
                        date_xaxis=True, dt=[tau, prc], plot_title=plot_title,
                        axeslabel_fontsize=axeslabel_fontsize, title_fontsize=title_fontsize, axesvalues_fontsize=axesvalues_fontsize,
                        annotation_fontsize=annotation_fontsize, legend_fontsize=legend_fontsize)

    #####################
    # now create list for return....
    LOW_TIDE = list()
    for v in local_minimums:
        t = time_array[v]
        w = wl_array[v]

        DateTime = datetime.strftime(num2date(t), datetime_fmt)
        LOW_TIDE.append([DateTime, w])
    
    HIGH_TIDE = list()
    for v in local_maximums:
        t = time_array[v]
        w = wl_array[v]

        DateTime = datetime.strftime(num2date(t), datetime_fmt)
        HIGH_TIDE.append([DateTime, w])

    return LOW_TIDE, HIGH_TIDE











if __name__ == '__main__':
    '''
        script filters out LOW and HIGH tide values from a
        hydrograph, then plots it in a pop-up window.
        After user has closed that window, the script saves
        two files (each for Low and High tide values)
    '''

    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    fillvalue   = -999.
    time_column = 0
    names       = ["GW_1", "GW_2", "GW_3", "GW_4", "GW_5", "GW_6"]
    gwl_column  = [1, 2, 3, 4, 5, 6]
    #names = ["W_1"]
    #gwl_column = [1]
    skiprows    = 2

    low_tide_fname  = 'low_tide.all'
    high_tide_fname = 'high_tide.all'
    destination_folder = 'out/'
    fname = "../data/SLICED_171020141500_130420150600/hydrographs/Farge-ALL_10min.all"

    datetime_fmt = '%d.%m.%Y %H:%M'
    savefiles    = True
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------

    path = os.path.dirname(sys.argv[0])
    filename = os.path.join(path, fname)
    check_data_to_be_correct(filename)
    
   
    for NAME, column in zip(names, gwl_column):

        time, wl = load_timeseries_from_csv_file(filename, usecols=[time_column, column],
                    skiprows=skiprows, delimiter=';',  datetime_fmt=datetime_fmt, fillvalue=fillvalue, return_mode=2)
        LT, HT = find_LowHighTide_Amplitudes(time, wl, tau=12.42/24., prc=2/24., order=25,
                    datetime_fmt=datetime_fmt, plot=True, plot_title=NAME, log=False,
                    axeslabel_fontsize=20., title_fontsize=22., axesvalues_fontsize=20., annotation_fontsize=20., legend_fontsize=20.)

        if savefiles:
            for fn, title , data in zip([low_tide_fname, high_tide_fname], ["Low Tide", "High Tide"], [LT, HT]):
                # now write to file
                fn_ = os.path.join(path, destination_folder, '{0}_{1}'.format(NAME, os.path.basename(fn) ))

                with open(fn_, mode='w+') as f:
                    f.write('#  This file is created automatically by script: find_amplitudes.py/n')
                    f.write('#  {0}: {1} are present. [meters above MSL]\n'.format(NAME, title))
                    f.write('#  --------------------------------------------------------------------------------------------\n')
                    for d in data:
                        line = '{0:20s}; {1:.2f}\n'.format(d[0], d[1])
                        f.write(line)

                    f.close()
                print "File created: {0}".format(fn_)
