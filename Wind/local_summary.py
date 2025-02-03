"""
This file is for reading the local wind summary
"""

import netCDF4
import numpy as np

def local_sum(source, _lat, _lon):
    """
    This function is for reading the local summary.
    `source`: a string of the file directory.
    `_lat`: a float number indicating the latitude target.
    `_lon`: a float number indicating the longitude target.
    return: an (8, 2) ndarray of the average wind speed and frequency at 8 directions
    """

    _lon += 360

    file = netCDF4.Dataset(source, 'r')

    speed = file.variables['speed']
    frequency = file.variables['frequency']
    lat = file.variables['latitude']
    lon = file.variables['longitude']

    # print(speed[:].shape)

    '''
    There is a problem with the mask. If there is no masked area in the requested region,
    the downloaded data will not have a element-wise mask, but only a single False.
    This will make the following np.argwhere return [].
    '''
    valid_ind = np.argwhere(speed[:, :, 0].mask == False)
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

    result = np.array([speed[iy_min, ix_min, :], frequency[iy_min, ix_min, :]], dtype='float64').T
    file.close()
    return result


if __name__ == '__main__':
    dir = 'backup/summary-1d.nc'
    test_lat = 55.6745326
    test_lon = -4.2738257
    print(local_sum(dir, test_lat, test_lon))
