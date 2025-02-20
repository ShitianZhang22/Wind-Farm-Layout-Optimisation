"""
This file is for creating a netCDF4 file to process and store the land data to a local file.
The previous step is in local_create_file.py.
"""

import netCDF4
import numpy as np

def process_wind(path, source):
    """
    This function is for creating a file for writing infeasible area.
    `path`: the file path for storing the data.
    `source`: the flile path for the data source.
    """

    # feasibility
    # feasibility = np.array([0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0], dtype='int')  # This is the previous version.
    feasibility = np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0], dtype='int')  # This is the new version.

    # data source
    file = netCDF4.Dataset(source, 'r')

    # lat = file.variables['lat']
    # lon = file.variables['lon']
    land = file.variables['lccs_class']

    step = 648

    # new dataset
    for i in range(0, 64800, step):
        i_list = [i + j for j in range(step)]
        flip_list = [64799 - i - j for j in range(step)]
        print(i_list)
        print(flip_list)
        summary = netCDF4.Dataset(path, 'a', format='NETCDF4')

        # create variables
        # s_lat = summary.variables['latitude']
        # s_lon = summary.variables['longitude']
        s_fea = summary.variables['feasible']

        s_fea[i_list, :] = feasibility[land[0, flip_list, :] // 10]

        summary.close()
    file.close()


if __name__ == '__main__':
    test_data = 'data/infeasible2.nc'
    s = 'raw/C3S-LC-L4-LCCS-Map-300m-P1Y-2022-v2.1.1.nc'
    process_wind(test_data, s)
 