import os
import sys
import inspect
import numpy as np
from pylab import *
from matplotlib.dates import date2num
from datetime import datetime
import pandas as pd
# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas


def method_1_amplitude_ration():
    """
    this function calculates TIDAL EFFICIENCY as a mean of amplitude ratios
        E = sum(Ei)/n

        where:
            Ei = h0/h   - ration of amplitude in river and gw well at cycle i
            n           - total number of cycles

    Function also checks difference between time in corresponding peakvalues
    """
    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    skiplines = 2  #skip header when reading CSV files

    data_w  = 'W_1_amplitude.all'
    data_gw = ['GW_1_amplitude.all', 'GW_2_amplitude.all', 'GW_3_amplitude.all', 'GW_4_amplitude.all', 'GW_5_amplitude.all', 'GW_6_amplitude.all']
    fname   = "../data/SLICED_171020141500_130420150600/amplitude/"

    datetime_fmt = '%d.%m.%Y %H:%M'  # format of the datetime in input text files
    date_peak_tolerance = 2./24.     # datetime peaks tolerance in days (for cheking errors, see code)
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------
    
    path    = os.path.dirname(sys.argv[0])  # current path
    fname_w = os.path.join(path, fname, data_w)  #fullpath to river datafile
    

    # Loop over all files with groundwater data...
    for data_fname in data_gw:
        fname_gw = os.path.join(path, fname, data_fname)  #path to current gw-datafile

        # read river data into numpy array
        w  = np.loadtxt(fname_w,  skiprows=skiplines, usecols=[0, 1, 4],  dtype={'names': ('date1', 'date2', 'amp'), 'formats': ('S20', 'S20', 'f4')}, delimiter=';')
        # read groundwater data into numpy array
        gw = np.loadtxt(fname_gw, skiprows=skiplines, usecols=[0, 1, 4],  dtype={'names': ('date1', 'date2', 'amp'), 'formats': ('S20', 'S20', 'f4')}, delimiter=';')

        #number of measurements (entries) should be the same
        if len(w) != len(gw):
            raise ValueError('Amplitude arrays have different length\n{0}'.format(fname_gw))

        E = list()
        
        
        # Loop over all entries, check if measurements in river/gw wells are within same time borders...
        # ... and finally calculate amplitude ration
        for i in xrange(len(w)):
            # check that amplitudes are at the same time...
            date1_w = date2num(datetime.strptime(w[i][0].strip(), datetime_fmt))
            date2_w = date2num(datetime.strptime(w[i][1].strip(), datetime_fmt))
            date1_gw = date2num(datetime.strptime(gw[i][0].strip(), datetime_fmt))
            date2_gw = date2num(datetime.strptime(gw[i][1].strip(), datetime_fmt))
            if abs(date1_w - date1_gw) > date_peak_tolerance:
                print '-'*50
                print 'HIGH TIDE'
                print('Line {0}.\n {3} \n {1} \nAmplitudes datetimes are not corresponding. Try increasing tolerance\n{2}'.format(i,
                                 w[i][0] + "!= " + gw[i][0], fname_gw, "river-waterlevel != groundwaterlevel"))
                #raise ValueError('Line {0}.\n {1} \nAmplitudes datetimes are not corresponding. Try increasing tolerance\n{2}'.format(i,
                #                 w[i][0] + "!=" + gw[i][0], fname_gw))
            if abs(date2_w - date2_gw) > date_peak_tolerance:
                print '-'*50
                print 'LOW TIDE'
                print('Line {0}.\n {3} \n {1} \nAmplitudes datetimes are not corresponding. Try increasing tolerance\n{2}'.format(i,
                                 w[i][1] + "!=" + gw[i][1], fname_gw, "river-waterlevel != groundwaterlevel"))
                #raise ValueError('Line {0}.\n {1} \nAmplitudes datetimes are not corresponding. Try increasing tolerance\n{2}'.format(i,
                #                 w[i][1] + "!=" + gw[i][1], fname_gw))
            
            E.append(gw[i][2] / w[i][2])  # calculating and appending amplitude ratio

        E = float(sum(E))/float(len(E))  # overwriting list with one value, calculated according to E = sum(Ei)/n

        print '-'*50
        print fname_gw
        print "E=", E









def method_2_from_cycle_std(savemode=None):
    '''
        savemod =
                None              - Default. No output will be saved
                'excel' or 'xls'  - output will be saved into EXCEL spreedsheet
                'csv'             - output will be saved into CSV text file



        Functions caclulates tidal effcicency  for each t.cycle Ei in two ways:
                Ei = std(Hydrograph_gw_i)/std(Hydrograph_w_i)
                Ei = amplitude(Hydrograph_gw_i)/amplitude(Hydrograph_w_i)
        and them saves all values into output file
    '''
    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    
    file_folder       = '../data/SLICED_171020141500_130420150600/hydrographs/'
    amplitudes_folder = '../data/SLICED_171020141500_130420150600/amplitude/'
    file_name         = 'Farge-ALL_10min.all'
    path_out          = 'out/'
    fname_out         = 'output_tidal_efficiency'
    
    ampl_fnames = ['GW_1_amplitude.all', 'GW_2_amplitude.all', 'GW_3_amplitude.all', 'GW_4_amplitude.all', 'GW_5_amplitude.all', 'GW_6_amplitude.all']
    river_ampl_fname  = 'W_1_amplitude.all'
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------


    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )


    # checking how to save output
    if savemode in ['xls', 'xlsx', 'excel', 'msexcel', 'Excel', 'XLS', 'XLSX']:
            outputfname = os.path.abspath(os.path.join(path, path_out, fname_out+'.xls'))
            writer = pd.ExcelWriter(outputfname)
    elif savemode in ['CSV', 'csv']:
        writer = None
    else:
        writer = None


    # read hydrographs into pandas dataframe
    data = process2pandas.read_hydrographs_into_pandas(fname, log=False)
    
    print '-'*50
    print 'Standart deviation all hydrographs'
    for n in ['GW_1', 'GW_2', 'GW_3', 'GW_4', 'GW_5', 'GW_6', 'W_1', ]:
        print '\t', n, data[n].std()
    print '-'*50
    
    # read amplitude&high/low-tide into pandas dataframe
    river_hightide, river_lowtide, river_amp = process2pandas.read_amplitudes_into_pandas(os.path.join(path, amplitudes_folder, river_ampl_fname))
    
    # -------------------------------------------------------------------------------
    # (1) WORKING WITH River data............................
    # -------------------------------------------------------------------------------
    W_1 = pd.DataFrame()  # creating new dataframe
    
    W_1['Datetime High Tide'] = river_hightide['datetime']
    W_1['Datetime Low Tide']  = river_lowtide['datetime']
    W_1['High Tide [m AMSL]'] = river_hightide['y']
    W_1['Low Tide [m AMSL]']  = river_lowtide['y']
    W_1['Amplitude_W [m]']    = river_amp
    W_1['STD_W_i']            = 0

    W_1['H_gw1_at_W_low[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw2_at_W_low[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw3_at_W_low[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw4_at_W_low[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw5_at_W_low[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw6_at_W_low[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    
    W_1['H_gw1_at_W_high[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw2_at_W_high[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw3_at_W_high[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw4_at_W_high[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw5_at_W_high[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks
    W_1['H_gw6_at_W_high[m AMSL]'] = 0  # waterlevel at GW wells at the moment of River peaks

    
    # now loop over tidal-cycles, picking values at corresponding H/L-tides in wells
    nCycle = 0
    for t_ht_w, t_lt_w in zip(river_hightide["datetime"], river_lowtide["datetime"]):
        
        i_ht_w = data[data['datetime'] == t_ht_w].index[0]  # should return index of an element <t_ht_gw> in series <data>
        
        i_start_cycle_w = i_ht_w - 18           # here we go 180min before highpeak
        i_end_cycle_w   = i_start_cycle_w + 73  # here we go 730min after beggining of cycle
        
        std_w = data.ix[i_start_cycle_w:i_end_cycle_w, "W_1"].std()  # calculate standart deviation of current tidal-cycle for river
        W_1.ix[nCycle, 'STD_W_i'] = std_w  # save value

        W_1.ix[nCycle, 'H_gw1_at_W_high[m AMSL]'] = data.ix[i_ht_w, 'GW_1']
        W_1.ix[nCycle, 'H_gw2_at_W_high[m AMSL]'] = data.ix[i_ht_w, 'GW_2']
        W_1.ix[nCycle, 'H_gw3_at_W_high[m AMSL]'] = data.ix[i_ht_w, 'GW_3']
        W_1.ix[nCycle, 'H_gw4_at_W_high[m AMSL]'] = data.ix[i_ht_w, 'GW_4']
        W_1.ix[nCycle, 'H_gw5_at_W_high[m AMSL]'] = data.ix[i_ht_w, 'GW_5']
        W_1.ix[nCycle, 'H_gw6_at_W_high[m AMSL]'] = data.ix[i_ht_w, 'GW_6']

        i_lt_w = data[data['datetime'] == t_lt_w].index[0]  # should return index of an element <t_lt_gw> in series <data>
        W_1.ix[nCycle, 'H_gw1_at_W_low[m AMSL]'] = data.ix[i_lt_w, 'GW_1']
        W_1.ix[nCycle, 'H_gw2_at_W_low[m AMSL]'] = data.ix[i_lt_w, 'GW_2']
        W_1.ix[nCycle, 'H_gw3_at_W_low[m AMSL]'] = data.ix[i_lt_w, 'GW_3']
        W_1.ix[nCycle, 'H_gw4_at_W_low[m AMSL]'] = data.ix[i_lt_w, 'GW_4']
        W_1.ix[nCycle, 'H_gw5_at_W_low[m AMSL]'] = data.ix[i_lt_w, 'GW_5']
        W_1.ix[nCycle, 'H_gw6_at_W_low[m AMSL]'] = data.ix[i_lt_w, 'GW_6']
        
        nCycle += 1


    # calculate overheads (ovepressure?) for each well
    W_1['Overhead_gw1_at_W_low[m]'] = W_1['H_gw1_at_W_low[m AMSL]']-W_1['Low Tide [m AMSL]']
    W_1['Overhead_gw2_at_W_low[m]'] = W_1['H_gw2_at_W_low[m AMSL]']-W_1['Low Tide [m AMSL]']
    W_1['Overhead_gw3_at_W_low[m]'] = W_1['H_gw3_at_W_low[m AMSL]']-W_1['Low Tide [m AMSL]']
    W_1['Overhead_gw4_at_W_low[m]'] = W_1['H_gw4_at_W_low[m AMSL]']-W_1['Low Tide [m AMSL]']
    W_1['Overhead_gw5_at_W_low[m]'] = W_1['H_gw5_at_W_low[m AMSL]']-W_1['Low Tide [m AMSL]']
    W_1['Overhead_gw6_at_W_low[m]'] = W_1['H_gw6_at_W_low[m AMSL]']-W_1['Low Tide [m AMSL]']

    W_1['Overhead_gw1_at_W_high[m]'] = W_1['H_gw1_at_W_high[m AMSL]']-W_1['High Tide [m AMSL]']
    W_1['Overhead_gw2_at_W_high[m]'] = W_1['H_gw2_at_W_high[m AMSL]']-W_1['High Tide [m AMSL]']
    W_1['Overhead_gw3_at_W_high[m]'] = W_1['H_gw3_at_W_high[m AMSL]']-W_1['High Tide [m AMSL]']
    W_1['Overhead_gw4_at_W_high[m]'] = W_1['H_gw4_at_W_high[m AMSL]']-W_1['High Tide [m AMSL]']
    W_1['Overhead_gw5_at_W_high[m]'] = W_1['H_gw5_at_W_high[m AMSL]']-W_1['High Tide [m AMSL]']
    W_1['Overhead_gw6_at_W_high[m]'] = W_1['H_gw6_at_W_high[m AMSL]']-W_1['High Tide [m AMSL]']


    # SAVING......
    W_1['STD_W_i'] = W_1['STD_W_i'].map(lambda x: '%.3f' % x)
    if savemode in ['xls', 'xlsx', 'excel', 'msexcel', 'Excel', 'XLS', 'XLSX']:
        W_1.to_excel(writer, 'RIVER', na_rep='---', index=False)
    elif savemode in ['CSV', 'csv']:
            outputfname = os.path.abspath(os.path.join(path, path_out, 'output_'+'river_data'+'.csv'))
            datetime_fmt = '%d.%m.%Y %H:%M'
 
            with open(outputfname, 'w') as csv:
                header = '\n'.join(
                    [unicode(line, 'utf8') for line in 
                        [ 'This File is created by script "calculate_tidal_efficiencies.py',
                        'In order to convert it to EXCEL use parameter savemode="xlsx"',
                        'It is possible to save all files to different excel-sheets',
                        '-'*100, '',  # Ends up being the header name for the index.
                        ]
                    ]
                )
                for line in header:
                    csv.write(line)
                hightide.to_csv(csv, sep=';', na_rep='---', index=False, encoding='utf-8', date_format=datetime_fmt, float_format='%.3f')
                csv.close()
            print "File created:", outputfname
    


    # -------------------------------------------------------------------------------
    # (2) WORKING WITH GW data............................
    # -------------------------------------------------------------------------------

    # Loop over files with amplitude data for gw well...
    for ampl_fn in ampl_fnames:
        a_fn = os.path.abspath(os.path.join(path, amplitudes_folder, ampl_fn))
        hightide, lowtide, amp = process2pandas.read_amplitudes_into_pandas(a_fn)  # read amplitude&high/low-tide into pandas dataframe
        
        #add columns....
        hightide['Amplitude_GW [m]'] = amp
        hightide['Amplitude_W [m]']  = river_amp
        hightide['STD_GW_i']         = 0.
        hightide['STD_W_i']          = 0.
        hightide['E_i (amplitude ratio)'] = hightide['Amplitude_GW [m]']/hightide['Amplitude_W [m]']
        hightide['E_i (std ratio)']  = 0.
        
        # now loop trough all tidal-cycles (more precisely - hightide datetimes)
        for nCycle, t_ht_gw in enumerate(hightide["datetime"]):  # nCycle - number of current tidal-cycle
            # find indexes in hydrograph series for gw...
            i_ht_gw = data[data['datetime'] == t_ht_gw].index[0]  # should return index of an element <t_ht_gw> in series <data>
            i_start_cycle_gw = i_ht_gw - 18           # (same values as in River section above) here we go 180min before highpeak
            i_end_cycle_gw   = i_start_cycle_gw + 73  # (same values as in River section above) here we go 730min after beggining of cycle
            # find indexes in hydrograph series for w...
            t_ht_w = river_hightide.ix[nCycle, "datetime"]
            i_ht_w = data[data['datetime'] == t_ht_w].index[0]  # should return index of an element <t_ht_w> in series <data>
            i_start_cycle_w = i_ht_w - 18           # (same values as in River section above) here we go 180min before highpeak
            i_end_cycle_w   = i_start_cycle_w + 73  # (same values as in River section above) here we go 730min after beggining of cycle

            # calculate STD for current tidal-cycle
            std_w  = data.ix[i_start_cycle_w:i_end_cycle_w, "W_1"].std()
            std_gw = data.ix[i_start_cycle_gw:i_end_cycle_gw, ampl_fn[:4]].std()
            E_i = std_gw/std_w
            
            #print ampl_fn[:4], '\te_cycle:', E_i, std_w, std_gw
            hightide.ix[nCycle, 'STD_GW_i'] = std_gw  # save to dataframe
            hightide.ix[nCycle, 'STD_W_i']  = std_w   # save to dataframe
            hightide.ix[nCycle, 'E_i (std ratio)'] = E_i  # save to dataframe

        #--------------------------------------------------------------------------------
        # at this moment everything is already caclculated and stays in memory....
        #--------------------------------------------------------------------------------

        # Now create nice file....
        col_names    = list(hightide.columns.values)
        col_names[0] = "Datetime High Tide"
        col_names[1] = "High Tide [m AMSL]"
        hightide.columns = col_names
        hightide.insert(1, 'Datetime Low Tide', lowtide["datetime"])
        hightide.insert(3, 'Low Tide [m AMSL]', lowtide["y"])
        E1 = hightide['E_i (std ratio)'].mean()
        E2 = hightide['E_i (amplitude ratio)'].mean()
        
        print ampl_fn
        print 'mean_E(std), mean_E(ampl)', E1, E2

        # change precision to 3 digits
        hightide['STD_GW_i'] = hightide['STD_GW_i'].map(lambda x: '%.3f' % x)
        hightide['STD_W_i']  = hightide['STD_W_i'].map(lambda x: '%.3f' % x)
        hightide['E_i (std ratio)'] = hightide['E_i (std ratio)'].map(lambda x: '%.3f' % x)
        hightide['E_i (amplitude ratio)'] = hightide['E_i (amplitude ratio)'].map(lambda x: '%.3f' % x)



        # Write to file
        if savemode in ['xls', 'xlsx', 'excel', 'msexcel', 'Excel', 'XLS', 'XLSX']:
            hightide.to_excel(writer, ampl_fn[:4], na_rep='---', index=False)
        
        elif savemode in ['CSV', 'csv']:
            outputfname = os.path.abspath(os.path.join(path, path_out, 'output_'+ampl_fn[:-4]+'.csv'))
            datetime_fmt = '%d.%m.%Y %H:%M'
 
            with open(outputfname, 'w') as csv:
                header = '\n'.join(
                    [unicode(line, 'utf8') for line in
                        [ 'This File is created by script "calculate_tidal_efficiencies.py',
                        'In order to convert it to EXCEL use parameter savemode="xlsx"',
                        'It is possible to save all files to different excel-sheets',
                        '-'*100, '',  # Ends up being the header name for the index.
                        ]
                    ]
                )
                for line in header:
                    csv.write(line)
                hightide.to_csv(csv, sep=';', na_rep='---', index=False, encoding='utf-8', date_format=datetime_fmt, float_format='%.3f')
                csv.close()
            print "File created:", outputfname

    # close XLS writer if exist
    if savemode and writer:
        writer.save()
        print "File created:", outputfname







if __name__ == '__main__':
    #method_1_amplitude_ration()
    method_2_from_cycle_std(savemode='xls')
    


