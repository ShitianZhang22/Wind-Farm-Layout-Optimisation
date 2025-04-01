"""
This file is for processing and storing the annual digest to a local file.
The last step is local_create_file.py (run process_wind() for all compressed data, and run process_wind2() once).
The next step is fill.py.
The writing process cannot be paused halfway, but the data can be saved if file.close() has been executed.
"""

import netCDF4
import numpy as np


def process_wind(source, path, first_month):
    """
    This function (along with process_wind3) is for creating the annual digest from the wind speed and direction data.
    Because of the memory issue of WSL, this function reads one original file (oen month) at a time and add it to the summary.
    The sum of speed and frequency are recorded in this function, and finally the summary is created by running process_wind2() once.
    `source`: a string indicating the directory of ONE DATA FILE.
    Here the input data should be produced by compress.py and contains the speed and directions.
    `path`: a string of the file path for storing the data.
    `first_month`: a bool variable indicating whether the input data is the first month.
    No return. Save a file of the sum of wind speed and total number of samples in each direction.
    """

    # The data is to be written every several lines (note that the original data is from north to south)
    step = 180

    with netCDF4.Dataset(path, 'r', format='NETCDF4') as summary:
        lat_len = len(summary.variables['latitude'][:])
        lon_len = len(summary.variables['longitude'][:])
        # print(lon_len)
   
    # main loop of writing file
    for i in range(0, lat_len, step):
        if i < 1800:
            i_list = [i + j for j in range(step)]  # this is for writing data
        else:
            i_list = [1800]
        print(i_list)

        # containers for final results
        # note that there is no nan value any more, but 0 instead
        s_speed = np.zeros((len(i_list), lon_len, 8), dtype='float64')
        s_frequency = np.zeros((len(i_list), lon_len, 8), dtype='int32')

        # read data source
        with netCDF4.Dataset(source, 'r') as file:

            # print(file.variables.keys())
            # for d in file.dimensions.items():
            #     print(d)

            speed = file.variables['speed'][:, i_list, :]
            direction = file.variables['direction'][:, i_list, :]

            # summarise
            for k in range(8):
                mask = direction[:] == k  # whether a wind record is at a specific direction
                s_frequency[:, :, k] = np.sum(mask, axis=0)
                s_speed[:, :, k] = np.sum(speed * mask, axis=0)

        if first_month:
            # store the data (for the first month)
            with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
                summary.variables['speed'][i_list, :, :] = s_speed
                summary.variables['frequency'][i_list, :, :] = s_frequency
        else:
            # store the data (for the following months)
            with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
                summary.variables['speed'][i_list, :, :] += s_speed
                summary.variables['frequency'][i_list, :, :] += s_frequency


def process_wind2(source, path):
    """
    This function (along with process_wind2) does the same thing as process_wind(),but reads the original data once at a time because of the memory issue of WSL.
    `source`: a string indicating the directory of the sum data from process_wind2().
    Here the input data should be produced by compress.py and contains the speed and directions.
    `path`: the file path for storing the data.
    No return. Save a file of the sum of wind speed and total number of samples in each direction.
    """

    with netCDF4.Dataset(source, 'r') as file:
        speed = file.variables['speed']
        frequency = file.variables['frequency']
        lat_len = len(file.variables['latitude'][:])
        lon_len = len(file.variables['longitude'][:])

        with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
            temp = np.zeros((lat_len, lon_len, 8), dtype='float32')
            np.divide(speed[:], frequency[:], where=(speed[:].mask == False), out=temp[:])
            summary.variables['speed'][:] = np.nan_to_num(temp)
            # the total number of samples
            temp = np.sum(frequency[:], axis=2).reshape((temp.shape[0], temp.shape[1], 1))
            summary.variables['frequency'][:] = np.nan_to_num(frequency / temp)


if __name__ == '__main__':
    # test_data1 = 'raw/'
    # test_data2 = 'raw/summary-01d.nc'
    # compressed_folder = 'compressed01d/'
    test_data3 = 'compressed01d/202412.nc'
    test_data4 = 'raw/summary-01d-temp.nc'

    # process_wind(test_data3, test_data4, False)

    process_wind2('raw/summary-01d-temp.nc', 'raw/summary-01d.nc')
    