import os
import sys
import inspect
import numpy as np
from pylab import *
from datetime import timedelta
import pandas as pd
import copy
# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas


def method_2_from_cycle(savemode=None):

    '''
        DEPRECATED !!!
        USE FUNCTION method_3_from_cycle()
        DEPRECATED !!!


        calculates timelag based on modified method of Erskine 1991
        utilazing cycle approach (see documentation)

        the result is saved in an excel file

        Mean timelag is not saved, and only showed in console,
        since it can be easily assesed in excel
    '''

    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    file_folder       = '../data/SLICED_171020141500_130420150600/hydrographs/'
    amplitudes_folder = '../data/SLICED_171020141500_130420150600/amplitude/'
    file_name         = 'Farge-ALL_10min.all'
    river_name        = 'Farge-W1_1min.all'
    river_ampl_fname  = 'W_1_amplitude.all'

    path_out          = 'out/'
    fname_out         = 'timelag_calculated_for_every_cycle'
    
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
    # get hightide, lowtide for accessing TIME of each
    river_hightide, river_lowtide, _ = process2pandas.read_amplitudes_into_pandas(os.path.join(path, amplitudes_folder, river_ampl_fname))

    
    print 'shifting, amplifying well data...'
    data['shifted_amplified_GW_1'] = data['W_1'].mean() + (data['GW_1'] - data['GW_1'].mean()) / E_GW_1
    data['shifted_amplified_GW_2'] = data['W_1'].mean() + (data['GW_2'] - data['GW_2'].mean()) / E_GW_2
    data['shifted_amplified_GW_3'] = data['W_1'].mean() + (data['GW_3'] - data['GW_3'].mean()) / E_GW_3
    data['shifted_amplified_GW_4'] = data['W_1'].mean() + (data['GW_4'] - data['GW_4'].mean()) / E_GW_4
    data['shifted_amplified_GW_5'] = data['W_1'].mean() + (data['GW_5'] - data['GW_5'].mean()) / E_GW_5
    data['shifted_amplified_GW_6'] = data['W_1'].mean() + (data['GW_6'] - data['GW_6'].mean()) / E_GW_6

    TLAG = dict()
    TLAG['GW_1'] = []
    TLAG['GW_2'] = []
    TLAG['GW_3'] = []
    TLAG['GW_4'] = []
    TLAG['GW_5'] = []
    TLAG['GW_6'] = []
    
    
    
    number_of_cycles = len(river_lowtide['datetime'])
    print 'Looping over Tidal Cycles of a River...'
    for t_ht, t_lt, i in zip(river_hightide['datetime'], river_lowtide['datetime'], river_lowtide.index):  # iterate over RIVER cycle times...
        print '\n\n Calculating timelag... for cycle {0}/{1}'.format(i+1, number_of_cycles)
        
        TLAG_I = dict()
        # loop over wells...
        for n1, timetuple in zip(['GW_1',  'GW_2',   'GW_3',   'GW_4',   'GW_5',   'GW_6'],
                                [(-10, 80), (-10, 80), (-10, 80), (-10, 80), (-10, 80), (-10, 80)]):
            h = data.ix[t_ht:t_lt, 'shifted_amplified_'+n1]  # slice data for correct time (t_ht:t_lt), and select well
            SUMM_LIST = list()
            TLAG_LIST = list()
            
            # loop over possible timelag values.... (see explanation in script <calculate_timelag.py>)
            for timelag in xrange(timetuple[0], timetuple[1]+1):  # try all timelags specified in 'timetuple'
                timelag_datetime = timedelta(minutes=timelag)     # convert minutes to datetime object

                # now cycle through all records in GROUNDWATERLEVEL data...
                summ = 0.
                for time_index, h_value in h.iteritems():
                    T = RIVER_data.loc[(time_index-timelag_datetime)][0]
                    summ += (h_value - T)**2

                SUMM_LIST.append(summ)
                TLAG_LIST.append(timelag)

            TLAG_I[n1] = TLAG_LIST[SUMM_LIST.index(min(SUMM_LIST))]
        
        # save tlags of all wells into one dictionary
        for n, v in TLAG_I.iteritems():
            TLAG[n].append(v)


    # ------------------------------------------------------
    # now we got all timelags for each cycle for each well...
    # So... calculate mean!
    # ------------------------------------------------------

    print '+'*50
    for n, v in TLAG.iteritems():
        TLAG[n] = np.array(v)
        print n, '\t >>> average tlag = ', TLAG[n].mean(), 'min'
        


    # save to EXCEL file
    df = pd.DataFrame(data=TLAG)
    outputfname = os.path.abspath(os.path.join(path, path_out, fname_out+'.xls'))
    writer = pd.ExcelWriter(outputfname)
    df.to_excel(writer, na_rep='---', index=True)
    writer.save()
    print "File created:", outputfname
    



def method_3_from_cycle(savemode=None):
    '''
        calculates timelag based on modified method of Erskine 1991
        utilazing cycle approach (see documentation)

        the result is saved in an excel file

        Mean timelag is not saved, and only showed in console,
        since it can be easily assesed in excel
    '''
    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    file_folder       = '../data/SLICED_171020141500_130420150600/hydrographs/'
    amplitudes_folder = '../data/SLICED_171020141500_130420150600/amplitude/'
    file_name         = 'Farge-ALL_10min.all'
    river_name        = 'Farge-W1_1min.all'
    river_ampl_fname  = 'W_1_amplitude.all'
    fname_Ei          = '../data/SLICED_171020141500_130420150600/output_tidal_efficiency_with_E.xls'

    path_out          = 'out/'
    fname_out         = 'timelag_calculated_for_every_cycle'

    # search limits for a timelag, (0, 80) means that script will iterate OVER tlag=[0, 1, 2, ... 80]
    MIN = dict()
    MIN['GW_1'] = (0, 80)
    MIN['GW_2'] = (0, 80)
    MIN['GW_3'] = (0, 80)
    MIN['GW_4'] = (0, 80)
    MIN['GW_5'] = (0, 80)
    MIN['GW_6'] = (0, 80)
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------


    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    RIVER_fname = os.path.abspath(os.path.join(path, file_folder, river_name) )

    # read data into pd.dataframe
    data       = process2pandas.read_mean_hydrographs_into_pandas(fname, datetime_indexes=True, decimal='.',  skiprows=1)
    RIVER_data = process2pandas.read_mean_hydrographs_into_pandas(RIVER_fname, datetime_indexes=True, decimal='.',  skiprows=4)
    # get hightide, lowtide for accessing TIME of each
    river_hightide, river_lowtide, _ = process2pandas.read_amplitudes_into_pandas(os.path.join(path, amplitudes_folder, river_ampl_fname))

    print "reading xlx with Ei"
    # read_ XLS into dictionary with key=sheet_name, value=pd.DataFrame
    xl_file = pd.ExcelFile(os.path.join(path, fname_Ei))
    dfs = {sheet_name: xl_file.parse(sheet_name)  # read
          for sheet_name in xl_file.sheet_names}
    
    TLAG = dict()
    # loop over wells...
    for well in ['GW_1', 'GW_2', 'GW_3', 'GW_4', 'GW_5', 'GW_6']:
        # for each well...
        TLAG[well] = []

        mean = data[well].mean()
        print 'MEAN = ', mean

        t_ht = dfs[well]['Datetime High Tide']
        E_amp = dfs[well]['E_i (amplitude ratio)']
        E_std = dfs[well]['E_i (std ratio)']

        number_of_cycles = len(t_ht)

        i = 0
        TLAG_I = list()
        for t_ht_i, E_amp_i, E_std_i in zip(t_ht, E_amp, E_std):
        # for each cycle...
            i += 1
            t_stac_gw = t_ht_i   - timedelta(minutes=180)    # here we go 180min before highpeak
            t_endc_gw = t_stac_gw + timedelta(minutes=720)   # here we go 720min after beggining of cycle
            #t_stac_gw, t_endc_gw  - datetime of start, end of cycle in DataFrame "data[]" (hydrographs, 10min) for a specific well

            # now, we know exact time of start and stop of cycle >>> slice data!
            h = copy.deepcopy(data.ix[t_stac_gw:t_endc_gw, well])  # slice data for correct time (t_ht:t_lt), and select well
            mean = RIVER_data.ix[t_stac_gw:t_endc_gw].mean()[0]    # mean of a tidal stage for current cycle
            E = E_std_i                                            # tidal efficiency of current well for current cycle


            # shift, amplify data....
            h = mean + (h - mean) / E
            
            print '\nCalculating timelag... for well={2}, cycle {0}/{1}'.format(i, number_of_cycles, well)
            print '\ttstart={0}\n\ttstop={1}\n\tE={2}'.format(t_stac_gw, t_endc_gw, E)
            
            SUMM_LIST = list()
            TLAG_LIST = list()
            for timelag in xrange(MIN[well][0], MIN[well][1]+1):  # try all timelags from 0 to 60 minutes, or those specified in 'timetuple'
                timelag_datetime = timedelta(minutes=timelag)     # convert minutes to datetime object

                # now cycle through all records in GROUNDWATERLEVEL data...
                summ = 0.
                for time_index, h_value in h.iteritems():
                    T = RIVER_data.loc[(time_index-timelag_datetime)][0]
                    summ += (h_value - T)**2
                SUMM_LIST.append(summ)
                TLAG_LIST.append(timelag)

            print '\ttlag >>>', TLAG_LIST[SUMM_LIST.index(min(SUMM_LIST))], 'min'
            TLAG_I.append(TLAG_LIST[SUMM_LIST.index(min(SUMM_LIST))])  # append correct timelag corresponding to minimum sum
        TLAG[well] = TLAG_I


    print '+'*50
    for n, v in TLAG.iteritems():
        TLAG[n] = np.array(v)
        print n, '\t >>> average tlag = ', TLAG[n].mean(), 'min'



    # save to EXCEL file
    df = pd.DataFrame(data=TLAG)
    outputfname = os.path.abspath(os.path.join(path, path_out, fname_out+'.xls'))
    writer = pd.ExcelWriter(outputfname)
    df.to_excel(writer, na_rep='---', index=True)
    writer.save()
    print "File created:", outputfname
    
if __name__ == '__main__':
    method_3_from_cycle()
