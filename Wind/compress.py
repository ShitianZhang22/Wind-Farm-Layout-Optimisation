import netCDF4
import numpy as np

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
    file_list = ['202401.nc']
    mesh = np.array(range(0, 3600, resolution), dtype='int32')

    for i in file_list:
        # load raw file
        with netCDF4.Dataset(source + i, 'a', format='NETCDF4') as file:
            u = file.variables['u10']
            v = file.variables['v10']
            f_time = file.variables['valid_time']
            # create new file
            with netCDF4.Dataset(path + i, 'a', format='NETCDF4') as comp:
                comp.createDimension('time', f_time.shape[0])
                comp.createDimension('latitude', 1800 / resolution + 1)
                comp.createDimension('longitude', 3600 / resolution)
                # create variables
                c_time = comp.createVariable('time', 'int8', ('time',), compression='zlib')
                c_lat = comp.createVariable('latitude', 'float32', ('latitude',), compression='zlib')
                c_lon = comp.createVariable('longitude', 'float32', ('longitude',), compression='zlib')
                c_speed = comp.createVariable('speed', 'float32', ('time', 'latitude', 'longitude',), zlib=True, complevel=9, chunksizes=(19, 40, 8))
                c_direction = comp.createVariable('direction', 'float32', ('time', 'latitude', 'longitude',), zlib=True, complevel=9, chunksizes=(19, 40, 8))

                c_time[:] = np.arange(f_time.shape[0])
                c_lat[:] = np.arange(-90, 90.1, 0.1 * resolution)
                c_lon[:] = np.arange(0, 360, 0.1 * resolution)

                for j in range(c_lat.shape[0]):
                    print(j)
                    # from south to north
                    southward = -v[:, mesh[1800 // resolution - j], mesh]
                    westward = -u[:, mesh[1800 // resolution - j], mesh]
                    
                    speed = (southward ** 2 + westward ** 2) ** 0.5
                    direction = np.arcsin(westward / speed)
                    mask = southward < 0
                    direction[mask] = np.pi - direction[mask]

                    # categorising the wind into 8 directions
                    c_speed[:, j, :] = speed[:]
                    c_direction[:, j, :] = (direction[:] + np.pi / 8) * 4 // np.pi

                
if __name__ == '__main__':
    test_data1 = 'raw/'
    compressed_folder = 'compressed/'
    compress(test_data1, compressed_folder, 5)
