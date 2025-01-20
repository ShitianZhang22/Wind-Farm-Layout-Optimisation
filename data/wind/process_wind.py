"""
This file is for getting the historical wind data at a given location from the raw data.
Input: the directory path of the wind data downloaded
Return: an (time, 2) ndarray of the u and v component of the hourly wind speed

In the main function for test, the data is stored locally, but this is not necessary when operating.
"""

import netCDF4
import numpy as np

def process_wind(source, _lat, _lon):
    """
    This function is for getting the historical wind data at a given location.
    `source`: a string indicating the directory of the data
    `_lat`: a float number indicating the latitude target
    `_lon`: a float number indicating the longitude target
    return: the closest valid position
    """

    file = netCDF4.Dataset(source, 'r')

    # print(file.variables.keys())
    # for d in file.dimensions.items():
    #     print(d)

    u = file.variables['u10']
    v = file.variables['v10']
    n = file.variables['number']
    lat = file.variables['latitude']
    lon = file.variables['longitude']
    t = file.variables['valid_time']

    # print(u[0])
    # print(u[:].shape)
    # print(lat[:])
    # print(lon[:])
    # print(u[0].data)
    # print(type(u[:].data))
    
    '''
    There is a problem with the mask. If there is no masked area in the requested region,
    the downloaded data will not have a element-wise mask, but only a single False.
    This will make the following np.argwhere return [].
    '''
    valid_ind = np.argwhere(u[0].mask == False)
    if valid_ind.shape[1] == 0:
        valid_ind = np.zeros((lat.shape[0], lon.shape[0], 2), dtype='int32')
        for i in range(lat.shape[0]):
            valid_ind[i, :, 0] = i
        for j in range(lon.shape[0]):
            valid_ind[:, j, 1] = j
        valid_ind = valid_ind.reshape((lat.shape[0] * lon.shape[0], 2))
        # converting the indices of the original data to coordinates
        valid_pos = np.array([lat[valid_ind[:, 0]], lon[valid_ind[:, 1]]], dtype='float64').T
    # print(valid_pos)

    dist_sq = np.sum((valid_pos - np.array([_lat, _lon])) ** 2, 1)
    iy_min, ix_min = valid_ind[dist_sq.argmin()]

    # print(iy_min, ix_min)
    # print(u.dimensions)
    # print(u.shape)
    # print(lon[:])
    # print(lat[:])

    result = np.array([u[:, iy_min, ix_min], v[:, iy_min, ix_min]], dtype='float64').T
    file.close()
    return result

if __name__ == '__main__':
    test_data = 'raw/temp.nc'
    test_lat = 55.6745326
    test_lon = -4.2738257
    np.savetxt('raw/test_uv.txt', process_wind(test_data, test_lat, test_lon), encoding='utf-8')
