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
    `source`: a string indicating the directory of the data
    `path`: the file path for storing the data.
    """

    file = netCDF4.Dataset(source, 'r')

    # print(file.variables.keys())
    # for d in file.dimensions.items():
    #     print(d)

    u = file.variables['u10']
    v = file.variables['v10']
    # n = file.variables['number']
    # lat = file.variables['latitude']
    # lon = file.variables['longitude']
    # t = file.variables['valid_time']

    # write variables (and save for every)
    for i in range(40, 181):
        summary = netCDF4.Dataset(path, 'a', format='NETCDF4')

        # spatial resolution (resolution * 0.1 degree)
        resolution = 10

        # read variables
        s_lat = summary.variables['latitude']
        s_lon = summary.variables['longitude']
        # s_dir = summary.variables['direction']
        s_speed = summary.variables['speed']
        s_freqency = summary.variables['frequency']

        for j in range(len(s_lon)):
            print('current: {}, {}'.format(i, j))
            if not u[0, i * resolution, j * resolution].mask:
                southward = -v[:, i * resolution, j * resolution]
                westward = -u[:, i * resolution, j * resolution]
                # print(southward)
                speed = (southward ** 2 + westward ** 2) ** 0.5
                direction = np.arcsin(westward / speed)
                mask = southward < 0
                direction[mask] = np.pi - direction[mask]

                # categorising the wind into 8 directions
                direction[:] = (direction[:] + np.pi / 8) * 4 // np.pi

                # summarise
                for k in range(8):
                    mask = direction[:] == k
                    s_freqency[i, j, k] = mask.sum()
                    if s_freqency[i, j, k]:
                        s_speed[i, j, k] = speed[mask].mean()
                    else:
                        s_speed[i, j, k] = 0.0
                s_freqency[i, j, :] /= s_freqency[i, j, :].sum()
        summary.close()

    file.close()


if __name__ == '__main__':
    test_data1 = 'data/2024Dec.nc'
    test_data2 = 'data/summary-1d.nc'
    process_wind(test_data1, test_data2)
