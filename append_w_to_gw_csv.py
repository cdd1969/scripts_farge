import numpy as np
import os, sys

if __name__ == '__main__':

    # ---------------------------------------
    # user inputs
    # ---------------------------------------

    # specify input files
    data_fname1 = 'Farge_gw_interpolated_for_py.csv'
    data_fname2 = 'Farge-W1_10min__101020140610_130420150600.csv'
    fname       = "../data/hydrographs_101020140610_130420150600/"
    
    # specify output file
    destination_folder = 'out/'
    out_fname = 'Farge-ALL_10min.all'

    # ---------------------------------------
    # END user inputs END
    # ---------------------------------------

    path = os.path.dirname(sys.argv[0])  #current path

    # load CSV file into numpy array
    a = np.loadtxt(os.path.join(path, fname, data_fname2), skiprows=2, usecols=[0, 1],  dtype={'names': ('date', 'W_level'), 'formats': ('S20', 'f4')}, delimiter=';')

    # read line by line CSV file
    with open(os.path.join(path, fname, data_fname1), mode="r") as f:
        fcontent = f.readlines()
        f.close()

    # save new file, appending data from numpy array to existing lines
    with open(os.path.join(path, destination_folder, out_fname), mode="w+") as f:
        for i, fl in enumerate(fcontent):
            if i > 1 and fl != '\n':
                f.write('{0}{1:.2f};\n'.format(fl[:-2], a[i-2][1]))
            else:
                f.write(fl)
