"""
This file is for filling the invalid data point in the wind data.
In the data processed by local_write.py, there is no empty data like --. Such data are all 0.
"""

import netCDF4
import numpy as np

def fill(source, path):

    """
    This function is for filling the empty data point in the wind data.
    `source`: the file path of the original data.
    `path`: the file path for storing the data. There should be a copy of the original data at this directory at the beginning of this process.
    """

    with netCDF4.Dataset(source, 'r', format='NETCDF4') as summary:
        # lat = summary.variables['latitude']
        # lon = summary.variables['longitude']
        speed0 = summary.variables['speed']
        frequency0 = summary.variables['frequency']

        with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
            # lat = summary.variables['latitude']
            # lon = summary.variables['longitude']
            speed = summary.variables['speed']
            frequency = summary.variables['frequency']

            # Find the non-zero wind data positions as grid indices.
            valid_ind = np.argwhere(np.sum(speed0[:], axis=2) != 0)
            invalid_ind = np.argwhere(np.sum(speed[:], axis=2) == 0)
            # print(invalid_ind)
        
            # for ind in invalid_ind[invalid_ind[:, 0] < 1700]:
            for ind in invalid_ind:
                print('Current:', ind)
                dist_sq = np.sum((valid_ind - ind) ** 2, axis=1)
                match = valid_ind[dist_sq.argmin()]
                print('Match:', match)
                speed[ind[0], ind[1], :] = speed0[match[0], match[1], :]
                frequency[ind[0], ind[1], :] = frequency0[match[0], match[1], :]

if __name__ == '__main__':
    fill('raw/summary-01d.nc', 'data/summary-01d.nc')
