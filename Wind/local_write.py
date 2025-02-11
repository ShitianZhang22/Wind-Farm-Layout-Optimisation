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
    `path`: the file path for storing the data.
    """

    # The data is to be written every 19 lines (note that the original data is from north to south)
    step = 19
    # Since I need to cut down the spatial resolution, I need to create a sparse mesh
    resolution = 5
    mesh = np.array(range(0, 3600, resolution), dtype='int32')

    with netCDF4.Dataset(path, 'a', format='NETCDF4') as summary:
        lat_len = len(summary.variables['latitude'][:])
        lon_len = len(summary.variables['longitude'][:])
        print(lon_len)
   
    # main loop of writing file
    # for i in range(0, lat_len, step):
    for i in range(0, 19, step):
        i_list = [i + j for j in range(step)]  # this is for writing data
        flip_list = [lat_len - 1 - i - j for j in range(step)]  # this is for reading data (the end is south)
        print(i_list)
        print(flip_list)

        # containers for concatenating monthly data
        u = np.zeros((0, step, lon_len), dtype='float32')
        v = np.zeros((0, step, lon_len), dtype='float32')

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
        file_list = ['202401.nc', '202402.nc']
        for j in file_list:
            print(source + j)
            with netCDF4.Dataset(source + j, 'r') as file:

                # print(file.variables.keys())
                # for d in file.dimensions.items():
                #     print(d)

                westward = -file.variables['u10'][:, mesh[flip_list], mesh]
                southward = -file.variables['v10'][:, mesh[flip_list], mesh]

                speed = (southward ** 2 + westward ** 2) ** 0.5
                direction = np.arcsin(westward / speed)
                mask = southward < 0
                direction[mask] = np.pi - direction[mask]

                # categorising the wind into 8 directions
                direction[:] = (direction[:] + np.pi / 8) * 4 // np.pi

                # # summarise
                # for k in range(8):
                #     mask = direction[:] == k
                #     s_freqency[i, j, k] = mask.sum()
                #     if s_freqency[i, j, k]:
                #         s_speed[i, j, k] = speed[mask].mean()
                #     else:
                #         s_speed[i, j, k] = 0.0
                # s_freqency[i, j, :] /= s_freqency[i, j, :].sum()


                # n = file.variables['number']
                # lat = file.variables['latitude']
                # lon = file.variables['longitude']
                # t = file.variables['valid_time']

        print(u.shape)

    # # write variables (and save for every)
    # for i in range(40, 181):
    #     summary = netCDF4.Dataset(path, 'a', format='NETCDF4')

    #     # spatial resolution (resolution * 0.1 degree)
    #     resolution = 10

    #     # read variables
    #     s_lat = summary.variables['latitude']
    #     s_lon = summary.variables['longitude']
    #     # s_dir = summary.variables['direction']
    #     s_speed = summary.variables['speed']
    #     s_freqency = summary.variables['frequency']

    #     for j in range(len(s_lon)):
    #         print('current: {}, {}'.format(i, j))
    #         if not u[0, i * resolution, j * resolution].mask:
    #             southward = -v[:, i * resolution, j * resolution]
    #             westward = -u[:, i * resolution, j * resolution]
    #             # print(southward)
    #             speed = (southward ** 2 + westward ** 2) ** 0.5
    #             direction = np.arcsin(westward / speed)
    #             mask = southward < 0
    #             direction[mask] = np.pi - direction[mask]

    #             # categorising the wind into 8 directions
    #             direction[:] = (direction[:] + np.pi / 8) * 4 // np.pi

    #             # summarise
    #             for k in range(8):
    #                 mask = direction[:] == k
    #                 s_freqency[i, j, k] = mask.sum()
    #                 if s_freqency[i, j, k]:
    #                     s_speed[i, j, k] = speed[mask].mean()
    #                 else:
    #                     s_speed[i, j, k] = 0.0
    #             s_freqency[i, j, :] /= s_freqency[i, j, :].sum()
    #     summary.close()

    # file.close()


if __name__ == '__main__':
    test_data1 = 'raw/'
    test_data2 = 'raw/summary-05d.nc'
    compressed_folder = 'compressed'
    process_wind(test_data1, test_data2)
