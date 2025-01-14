import netCDF4
import numpy as np


def getclosest(pos_list, _lat, _lon):
    """
    This function is to find the closest valid position from the selected point
    `poslist`: an ndarray including coordinates (lat or lon) with valid data
    `_lat`: a float number indicating the latitude target
    `_lon`: a float number indicating the longitude target
    return: the closest valid position
    """
    # find squared distance of every point on grid
    dist_sq = np.sum((pos_list - np.array([_lat * 10, _lon * 10])) ** 2, 1)
    print(dist_sq.shape)

    # 1D index of minimum dist_sq element
    return pos_list[dist_sq.argmin()]


file = netCDF4.Dataset('test/2024dec.nc', 'r')

# print(file.variables.keys())
# for d in file.dimensions.items():
#     print(d)

u = file.variables['u10']
v = file.variables['v10']
n = file.variables['number']
lat = file.variables['latitude']
lon = file.variables['longitude']
t = file.variables['valid_time']

in_lat = 55.63
in_lon = -4.3 + 360

valid_pos = np.argwhere(u[0].mask == False)

iy_min, ix_min = getclosest(valid_pos, in_lat, in_lon)

# print(u.dimensions)
# print(u.shape)

print(u[:, iy_min, ix_min])

file.close()
