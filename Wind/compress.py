"""
This file is for converting the original wind data into speed and directions, and flip the data by latitude.
The next step is in local_create_file.py.
"""

import netCDF4
import numpy as np
import os
import time

def compress(source, path, resolution):
    """
    This function is for compressing the raw data to accelerate the processing speed.
    At the same time, the data will be vertically flipped.
    `source`: a string indicating the directory of the data folder.
    `path`: a string of the target file folder.
    `resolution`: a float number of spatial resolution. The actual resolution is multiplied by 0.1 degree.
    """
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
    # file_list = ['202401.nc']
    # mesh = np.array(range(0, 3600, resolution), dtype='int32')

    for i in file_list:
        # load raw file
        # file_exist = os.path.exists(source + i)
        with netCDF4.Dataset(source + i, 'a', format='NETCDF4') as file:
            u = file.variables['u10']
            v = file.variables['v10']
            f_time = file.variables['valid_time']
            # create new file / open file
            with netCDF4.Dataset(path + i, 'a', format='NETCDF4') as comp:
                comp.createDimension('time', f_time.shape[0])
                comp.createDimension('latitude', 1800 / resolution + 1)
                comp.createDimension('longitude', 3600 / resolution)
                # create variables
                c_time = comp.createVariable('time', 'int8', ('time',), compression='zlib')
                c_lat = comp.createVariable('latitude', 'float32', ('latitude',), compression='zlib')
                c_lon = comp.createVariable('longitude', 'float32', ('longitude',), compression='zlib')
                c_speed = comp.createVariable('speed', 'float32', ('time', 'latitude', 'longitude',), zlib=True, complevel=9, chunksizes=(100, 18, 360))
                c_direction = comp.createVariable('direction', 'int8', ('time', 'latitude', 'longitude',), zlib=True, complevel=9, chunksizes=(100, 18, 360))

                c_time[:] = np.arange(f_time.shape[0])
                c_lat[:] = np.arange(-90, 90.1, 0.1 * resolution)
                c_lon[:] = np.arange(0, 360, 0.1 * resolution)
                # if file_exist:
                #     c_time = comp.variables['time']
                #     c_lat = comp.variables['latitude']
                #     c_lon = comp.variables['longitude']
                #     c_speed = comp.variables['speed']
                #     c_direction = comp.variables['direction']
                # else:
                #     comp.createDimension('time', f_time.shape[0])
                #     comp.createDimension('latitude', 1800 / resolution + 1)
                #     comp.createDimension('longitude', 3600 / resolution)
                #     # create variables
                #     c_time = comp.createVariable('time', 'int8', ('time',), compression='zlib')
                #     c_lat = comp.createVariable('latitude', 'float32', ('latitude',), compression='zlib')
                #     c_lon = comp.createVariable('longitude', 'float32', ('longitude',), compression='zlib')
                #     c_speed = comp.createVariable('speed', 'float32', ('time', 'latitude', 'longitude',), zlib=True, complevel=9, chunksizes=(100, 18, 360))
                #     c_direction = comp.createVariable('direction', 'int8', ('time', 'latitude', 'longitude',), zlib=True, complevel=9, chunksizes=(100, 18, 360))

                #     c_time[:] = np.arange(f_time.shape[0])
                #     c_lat[:] = np.arange(-90, 90.1, 0.1 * resolution)
                #     c_lon[:] = np.arange(0, 360, 0.1 * resolution)
                
                step = 18
                t = time.time()

                for j in range(0, c_lat.shape[0], step):
                    if j < 1800:
                        j_list = [j + k for k in range(step)]  # this is for writing data
                        rev_j_list = [1800 - j - k for k in range(step)]  # this is for reading data
                    else:
                        j_list = [1800]
                        rev_j_list = [0]
                    print(j_list)
                    print(rev_j_list)
                    print('{}: {} time:{}'.format(i, j, time.time() - t))
                    # from south to north
                    # southward = -v[:, mesh[1800 // resolution - j], mesh]
                    # westward = -u[:, mesh[1800 // resolution - j], mesh]
                    southward = -v[:, rev_j_list, :]
                    westward = -u[:, rev_j_list, :]
                    
                    speed = (southward ** 2 + westward ** 2) ** 0.5
                    direction = np.arccos(southward / speed) / np.pi
                    mask = westward[:] < 0
                    direction[mask] = 2 - direction[mask]

                    # categorising the wind into 8 directions
                    c_speed[:, j_list, :] = speed[:]
                    temp = np.floor((direction[:] * 4 + 0.5))
                    temp[temp[:] == 8] = 0  # change the values 8 to 0
                    c_direction[:, j_list, :] = temp

                
if __name__ == '__main__':
    test_data1 = 'raw/'
    compressed_folder = 'compressed01d/'
    compress(test_data1, compressed_folder, 1)
