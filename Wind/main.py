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
    # print(lat, lon)
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

    iy_min = np.argmin(np.abs(lat[:] - _lat))
    ix_min = np.argmin(np.abs(lon[:] - _lon))

    # print('Using wind data at:')
    # print(lat[iy_min], lon[ix_min] - 360)

    result = np.array([speed[iy_min, ix_min, :], frequency[iy_min, ix_min, :]], dtype='float64').T
    file.close()
    return result


if __name__ == '__main__':
    test_area = [55.7146943, -4.364574, 55.6343709, -4.1830774]
    # dir = 'raw/temp.nc'
    # y = ['2024']
    # m = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    # print(wind(test_area, dir, y, m, True))

