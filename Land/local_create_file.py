"""
This file is for creating a netCDF4 file to process and store the land data to a local file.
The next step is in local_write.py.
"""

import netCDF4
import numpy as np

def process_wind(path, source):
    """
    This function is for creating a file for writing infeasible area.
    `path`: the file path for storing the data.
    `source`: the flile path for the data source.
    """

    # data source
    file = netCDF4.Dataset(source, 'r')

    lat = file.variables['lat']
    lon = file.variables['lon']
    land = file.variables['lccs_class']

    # new dataset
    summary = netCDF4.Dataset(path, 'a', format='NETCDF4')

    summary.createDimension('latitude', len(lat))
    summary.createDimension('longitude', len(lon))

    # create variables
    s_lat = summary.createVariable('latitude', 'float32', ('latitude',), compression='zlib')
    s_lon = summary.createVariable('longitude', 'float32', ('longitude',), compression='zlib')
    s_fea = summary.createVariable(
        'feasible', 'b', ('latitude', 'longitude',),
        zlib=True, complevel=9, chunksizes=(648, 1296), fill_value=0
        )

    # the latitude in the data source is from north to south
    s_lat[:] = np.flip(lat[:])
    s_lon[:] = lon[:]

    print(s_lat[:])
    print(s_lon[:])

    summary.close()
    file.close()


if __name__ == '__main__':
    test_data = 'data/infeasible.nc'
    s = 'raw/C3S-LC-L4-LCCS-Map-300m-P1Y-2022-v2.1.1.nc'
    process_wind(test_data, s)
