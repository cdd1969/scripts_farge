''' Script reads hydrograph into pandas dataframe,
    then calculates mean according to Serfes1991
    and saves output into EXCEL or CSV file
'''
import os
import sys
import numpy as np
from pylab import *
# use this if you want to include modules from a subfolder
import inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
                    inspect.getfile( inspect.currentframe() ))[0], "lib")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import process2pandas


def filter_wl_71h_serfes1991(data, savemode=None, outputfname=None):
    '''
    data - is pandas dataframe, where indexes are Datetime objects,
           see 'parse_dates' parameters
    '''
    writer = None
    print "Passed data has shape:", data.shape
    #print number of items per day
    #print(data.groupby(data.index.date).count())

    # ok, we see, that we have 144 measurements per day....
    N = 144
    for col_name in data.columns:  # cycle through each column...
        print "working with column:", col_name
        data[col_name+'_averaging1'] = np.nan
        data[col_name+'_averaging2'] = np.nan
        data[col_name+'_averaging3'] = np.nan
        
        print "\t Calculating first mean:", col_name
        for i in xrange(N/2, len(data.index)-N/2):  # cycle trough correct indexes
            data.ix[i, col_name+'_averaging1'] = data.ix[i-N/2:i+N/2, col_name].mean()
        
        print "\t Calculating second mean:", col_name
        for i in xrange(N, len(data.index)-N):  # cycle trough correct indexes
            data.ix[i, col_name+'_averaging2'] = data.ix[i-N/2:i+N/2, col_name+'_averaging1'].mean()
        
        print "\t Calculating third mean:", col_name
        for i in xrange(N+N/2, len(data.index)-N-N/2):  # cycle trough correct indexes
            data.ix[i, col_name+'_averaging3'] = data.ix[i-N/2:i+N/2, col_name+'_averaging2'].mean()
        #break



    if savemode in ['xls', 'xlsx', 'excel', 'msexcel', 'Excel', 'XLS', 'XLSX']:
        #outputfname = os.path.abspath(os.path.join(path, pth_out, fname_out+'.xlsx'))
        writer = ExcelWriter(outputfname)
        hightide.to_excel(writer, sheet_name=ampl_fn[:-4], na_rep='---', index=False)

    elif savemode in ['CSV', 'csv']:
        #outputfname = os.path.abspath(os.path.join(path, pth_out, 'output_'+ampl_fn[:-4]+'.csv'))
        datetime_fmt = '%d.%m.%Y %H:%M'
        #for col_name in data.columns:
        #    data[col_name] = data[col_name].map(lambda x: '%.2f' % x)


        with open(outputfname, 'w') as csv:
            header = '\n'.join(
                [unicode(line, 'utf8') for line in
                    [ 'This File is created by script "read_hydrographs_calculate_mean.py',
                    'In order to convert it to EXCEL use parameter savemode="xlsx"',
                    'It is possible to save all files to different excel-sheets',
                    '-'*100, '',  # Ends up being the header name for the index.
                    ]
                ]
            )
            for line in header:
                csv.write(line)
            data.to_csv(csv, sep=';', na_rep='---', index=True, encoding='utf-8', date_format=datetime_fmt, float_format='%.2f', decimal=',')
            csv.close()
        print "File created:", outputfname

    if savemode:
        if writer:
            writer.save()
            print "File created:", outputfname



if __name__ == '__main__':
    # --------------------------------------------------------------------------------------
    # user inputs
    # --------------------------------------------------------------------------------------
    file_folder = '../data/SLICED_171020141500_130420150600/hydrographs/'
    file_name   = 'Farge-ALL_10min.all'
    pth_out     = "out/"
    fileout     = 'averaging_mean.csv'
    savemode    = 'CSV'
    # --------------------------------------------------------------------------------------
    # END user inputs END
    # --------------------------------------------------------------------------------------




    path = os.path.dirname(sys.argv[0])
    fname = os.path.abspath(os.path.join(path, file_folder, file_name) )
    outname = os.path.abspath(os.path.join(path, pth_out, fileout))

    data = process2pandas.read_hydrographs_into_pandas(fname, datetime_indexes=True)
    filter_wl_71h_serfes1991(data, savemode=savemode, outputfname=outname)











