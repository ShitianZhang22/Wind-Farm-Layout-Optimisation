"""
This file is for creating a netCDF4 file to process and store the annual digest to a local file.
The next step is in local_write.py.
"""

import netCDF4
import numpy as np

def process_wind(path):
    """
    This function is for creating a file for writing annual digest.
    `path`: the file path for storing the data.
    """

    summary = netCDF4.Dataset(path, 'a', format='NETCDF4')

    # spatial resolution (resolution * 0.1 degree)
    resolution = 10

    summary.createDimension('latitude', 181)
    summary.createDimension('longitude', 360)
    summary.createDimension('direction', 8)

    # create variables
    s_lat = summary.createVariable('latitude', 'float32', ('latitude',), compression='zlib')
    s_lon = summary.createVariable('longitude', 'float32', ('longitude',), compression='zlib')
    s_dir = summary.createVariable('direction', 'int8', ('direction',), compression='zlib')
    s_speed = summary.createVariable('speed', 'float32', ('latitude', 'longitude', 'direction',), compression='zlib', least_significant_digit=2)
    s_freqency = summary.createVariable('frequency', 'float32', ('latitude', 'longitude', 'direction',), compression='zlib', least_significant_digit=2)

    s_lat[:] = np.arange(-90, 90.1, 0.1 * resolution)
    s_lon[:] = np.arange(0, 360, 0.1 * resolution)
    s_dir[:] = np.arange(0, 8, 1)

    summary.close()


if __name__ == '__main__':
    test_data = 'backup/summary-1d.nc'
    process_wind(test_data)
