import os
import sys
import numpy as np
import re
from pylab import *


if __name__ == '__main__':
    '''
        create file for each well and store info about amplitude of each tidal cycle

        low/high tide data required.
    '''
    # ---------------------------------------
    # user inputs
    # ---------------------------------------
    lt  = ['GW_1_low_tide.all',  'GW_2_low_tide.all',  'GW_3_low_tide.all',  'GW_4_low_tide.all',  'GW_5_low_tide.all',  'GW_6_low_tide.all',  'W_1_low_tide.all']
    ht  = ['GW_1_high_tide.all', 'GW_2_high_tide.all', 'GW_3_high_tide.all', 'GW_4_high_tide.all', 'GW_5_high_tide.all', 'GW_6_high_tide.all', 'W_1_high_tide.all']
    amp = ['GW_1_amplitude.all', 'GW_2_amplitude.all', 'GW_3_amplitude.all', 'GW_4_amplitude.all', 'GW_5_amplitude.all', 'GW_6_amplitude.all', 'W_1_amplitude.all']
    lt_folder = "../data/low_tide/"
    ht_folder = "../data/high_tide/"
    destination_folder = 'out/'
    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------


    path = os.path.dirname(sys.argv[0])

    for l , h , a in zip(lt, ht, amp):
        lt_fn = os.path.join(path, lt_folder, l)
        ht_fn = os.path.join(path, ht_folder, h)
    
        # load files into numpy...
        lt_d = np.loadtxt(lt_fn, skiprows=3, delimiter=';',  dtype={'names': ('time', 'W_level'), 'formats': ('S20', 'f4')})
        ht_d = np.loadtxt(ht_fn, skiprows=3, delimiter=';',  dtype={'names': ('time', 'W_level'), 'formats': ('S20', 'f4')})
        
        with open(os.path.join(path, destination_folder, a), mode="w+") as f:
            f.write("File is created with script 'create_amplitudes_from_lowhightide.py'\n")
            f.write("Datetime(high tide); Datetime(low tide)  ; high-tide [mNN]; low-tide [mNN]; amplitude [m]\n")
            for i in xrange(len(ht_d)):
                f.write('{0}; {1}; {2:.2f};\t{3:.2f};\t{4:.2f}\n'.format(ht_d[i][0], lt_d[i+1][0], ht_d[i][1], lt_d[i+1][1], abs(ht_d[i][1]-lt_d[i+1][1]) ))
            f.close()
