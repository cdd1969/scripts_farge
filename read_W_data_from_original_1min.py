import os
import sys
import numpy as np
import re
from pylab import *


if __name__ == '__main__':

    
    fillvalue = -999.

    data_fname = 'FARGE_1min_01102014_13042015.all'
    fname = "../data/farge_W_data_ORIGINAL/"
    destination_folder = 'out/'
    out_fname = 'Farge-W1_1min.all'

    datetime_fmt = '%d.%m.%Y %H:%M:%S'


    ############################################################################################

    path = os.path.dirname(sys.argv[0])
    filename = os.path.join(path, fname, data_fname)

    a = np.loadtxt(filename, skiprows=27, usecols=[0, 1, 5],  dtype={'names': ('date', 'time', 'W_level'), 'formats': ('S20', 'S20', 'f4')},
                    converters={5: lambda s: float(re.sub(',', '.', s.strip() )) })
    with open(os.path.join(path, destination_folder, out_fname), mode="w+") as f:
        f.write("File is created with script 'read_W_data_from_original.py'\n")
        f.write("Datetime; Farge_W1   [mNN]\n")
        for i in xrange(len(a)):
            if a[i][1] == '24:00:00' and i != len(a)-1:
                a[i][0] = a[i+1][0]
                a[i][1] = '00:00:00'
            f.write('{0} {1}; {2:.2f}\n'.format(re.sub("/", ".", a[i][0]), a[i][1][:5], a[i][2]))
        f.close()
    print 'File created: ', os.path.abspath(os.path.join(path, destination_folder, out_fname))

