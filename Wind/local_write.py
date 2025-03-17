"""
This file is for processing and storing the annual digest to a local file.
The last step is in local_create_file.py.
The writing process cannot be paused halfway, but the data can be saved if file.close() has been executed.
"""

import netCDF4
import numpy as np

def process_wind(source, path):
    """
    This function is for processing and storing the annual digest to a local file.
    `source`: a string indicating the directory of the data folder.
    Here the input data should be produced by compress.py and contains the speed and directions.
    `path`: the file path for storing the data.
    """

    # The data is to be written every several lines (note that the original data is from north to south)
    step = 180

    with netCDF4.Dataset(path, 'r', format='NETCDF4') as summary:
        lat_len = len(summary.variables['latitude'][:])
        lon_len = len(summary.variables['longitude'][:])
        # print(lon_len)
   
    # main loop of writing file
    for i in range(0, lat_len, step):
    # for i in range(0, 19, step):
        i_list = [i + j for j in range(step)]  # this is for writing data
        print(i_list)

        # containers for data
        speed = np.zeros((0, step, lon_len), dtype='float32')
        direction = np.zeros((0, step, lon_len), dtype='int32')

        # containers for final results
        s_speed = np.zeros((step, lon_len, 8), dtype='float32')
        s_frequency = np.zeros((step, lon_len, 8), dtype='float32')

        # read the data source
        file_list = [
            '202401.nc',
            '202402.nc',
            '202403.nc',
            '202404.nc',
            '202405.nc',
            '202406.nc',
            '202407.nc',
            '202408.nc',
            '202409.nc',
            '202410.nc',
            '202411.nc',
            '202412.nc',
        ]
        # file_list = ['202401.nc', '202402.nc']
        for j in file_list:
            print(source + j)
            with netCDF4.Dataset(source + j, 'r') as file:

                # print(file.variables.keys())
                # for d in file.dimensions.items():
                #     print(d)

                speed = np.concatenate((speed, file.variables['speed'][:, i_list, :]), axis=0)
                direction = np.concatenate((direction, file.variables['direction'][:, i_list, :]), axis=0)

        # summarise
        for k in range(8):
            mask = direction[:] == k  # whether a wind record is at a specific direction
            s_frequency[:, :, k] = np.sum(mask, axis=0)
            s_speed[:, :, k] = np.sum(speed * mask, axis=0)
            mask2 = np.sum(mask, axis=0).astype(np.bool)  # whether there exists wind at a specific direction
            # in this way, we can prevent division by zero
            np.divide(s_speed[:, :, k], s_frequency[:, :, k], where=mask2, out=s_speed[:, :, k])
        s_frequency /= speed.shape[0]

        # store the data
        with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
            summary.variables['speed'][i_list, :, :] = s_speed
            summary.variables['frequency'][i_list, :, :] = s_frequency


def process_wind2(source, path):
    """
    This function (along with process_wind3) does the same thing as process_wind(),but reads the original data once at a time because of the memory issue of WSL.
    `source`: a string indicating the directory of ONE DATA FILE.
    Here the input data should be produced by compress.py and contains the speed and directions.
    `path`: the file path for storing the data.
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

        # store the data (for the first month)
        # with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
        #     summary.variables['speed'][i_list, :, :] = s_speed
        #     summary.variables['frequency'][i_list, :, :] = s_frequency
        
        # store the data (for the following months)
        with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
            summary.variables['speed'][i_list, :, :] += s_speed
            summary.variables['frequency'][i_list, :, :] += s_frequency


def process_wind3(source, path):
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
    # process_wind(compressed_folder, test_data2)
    # process_wind2(test_data3, test_data4)

    process_wind3('raw/summary-01d-temp.nc', 'raw/summary-01d.nc')
    