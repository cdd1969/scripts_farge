import os, sys
import datetime
# use this if you want to include modules from a subfolder
import inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas

if __name__ == '__main__':
    '''
    Calculating Timelag after Erskine 1991.
    The results will be printed in console and are not saved anywhere (!)

    Using 10min ground water data and 1min river water data
    '''
    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    file_folder = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name   = 'Farge-ALL_10min.all'
    river_name  = 'Farge-W1_1min.all'

    E_GW_1 = 0.25218  #  Tidal Efficiency [-] for well 1
    E_GW_2 = 0.31209  #  Tidal Efficiency [-] for well 2
    E_GW_3 = 0.24625  #  Tidal Efficiency [-] for well 3
    E_GW_4 = 0.17867  #  Tidal Efficiency [-] for well 4
    E_GW_5 = 0.33024  #  Tidal Efficiency [-] for well 5
    E_GW_6 = 0.36874  #  Tidal Efficiency [-] for well 6
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------


    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    RIVER_fname = os.path.abspath(os.path.join(path, file_folder, river_name) )

    # load data into pd.dataframe
    data       = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal='.',  skiprows=1)
    RIVER_data = process2pandas.read_mean_hydrographs_into_pandas(RIVER_fname, datetime_indexes=True, decimal='.',  skiprows=4)



    print 'shifting, amplifying well data...'
    data['shifted_amplified_GW_1'] = data['W_1'].mean() + (data['GW_1'] - data['GW_1'].mean()) / E_GW_1
    data['shifted_amplified_GW_2'] = data['W_1'].mean() + (data['GW_2'] - data['GW_2'].mean()) / E_GW_2
    data['shifted_amplified_GW_3'] = data['W_1'].mean() + (data['GW_3'] - data['GW_3'].mean()) / E_GW_3
    data['shifted_amplified_GW_4'] = data['W_1'].mean() + (data['GW_4'] - data['GW_4'].mean()) / E_GW_4
    data['shifted_amplified_GW_5'] = data['W_1'].mean() + (data['GW_5'] - data['GW_5'].mean()) / E_GW_5
    data['shifted_amplified_GW_6'] = data['W_1'].mean() + (data['GW_6'] - data['GW_6'].mean()) / E_GW_6

    # loop over gw wells and USERDEFINED possible timelags
    #   i.e. timetuple=(20, 30) means that the script will try to match all timelags in list [20, 21, 22, ..., 30]
    #   we use these timetuples to increase speed of calculation, cause this approach of Erskine is timeconsuming
    #   by default it is recommended to set all of the timetuples to (0, 60) or some other awaited region
    #   then user can play around with the values.
    print 'Calculating timelag...'
    for n1, timetuple in zip(['GW_1',  'GW_2',   'GW_3',   'GW_4',   'GW_5',   'GW_6'],    # gw well
                            [(20, 30), (5, 15), (10, 20), (15, 30), (10, 20), (30, 40)]):  # corresponding timelag tuple
        # skip unnesessary things....
        #if n1 in ['GW_1', 'GW_2', 'GW_3', 'GW_4', 'GW_5']:  # 'GW_5', 'GW_6']:
        #    continue

        h = data['shifted_amplified_' + n1]  # select correct gw well data
        SUMM_LIST = list()
        TLAG_LIST = list()
        for timelag in xrange(timetuple[0], timetuple[1]+1):        # try all timelags specified in 'timetuple'
            timelag_datetime = datetime.timedelta(minutes=timelag)  # convert minutes to datetime object

            # now loop over all records in GROUNDWATERLEVEL data... and calculate sum according to Erskine 1991 equation
            summ = 0.
            for time_index, h_value in h.iteritems():
                T = RIVER_data.loc[(time_index-timelag_datetime)][0]
                summ += (h_value - T)**2

            print n1, 'timelag=', timelag, 'minutes >>> summ =', summ
            SUMM_LIST.append(summ)
            TLAG_LIST.append(timelag)
        
        print '-'*100
        print '\t', n1
        print '\t minimal SUMM       :', min(SUMM_LIST)
        print '\t corresponding TLAG :', TLAG_LIST[SUMM_LIST.index(min(SUMM_LIST))]
        print '-'*100
