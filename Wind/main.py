"""
This is the master structure managing the process of wind data, including:
1. Downloading and deleting the temporary file of wind data
2. Get the data from the raw data downloaded
3. Converting the data to annual wind distribution

Input: a list of site bounds, and a path for caching data.
Return: an (8, 2) ndarray of the average wind speed and frequency at 8 directions
"""

import netCDF4
import numpy as np


def wind(area, save_dir):
    """
    This is the master structure managing the process of wind data.

    `area`: a list of Northern, Western, Southern, Eastern bounds of the site.
    `save_dir`: the directory to temporarily save the downloaded data.
    Return: an (8, 2) ndarray of the average wind speed and frequency at 8 directions
    """
    # get the centre of the site
    lat, lon = (area[0] + area[2]) / 2, (area[1] + area[3]) / 2
    return local_sum(save_dir, lat, lon)


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

    # print(lat[iy_min], lon[ix_min])

    result = np.array([speed[iy_min, ix_min, :], frequency[iy_min, ix_min, :]], dtype='float64').T
    file.close()
    return result


if __name__ == '__main__':
    test_area = [55.7146943, -4.364574, 55.6343709, -4.1830774]
    # dir = 'raw/temp.nc'
    # y = ['2024']
    # m = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    # print(wind(test_area, dir, y, m, True))

