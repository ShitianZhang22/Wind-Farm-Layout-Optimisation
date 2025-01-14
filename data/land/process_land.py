import netCDF4
import numpy as np


def getclosest(pos_list, pos):
    """
    This function is to find the closest valid position from the selected point
    `poslist`: an ndarray including coordinates (lat or lon) with valid data
    `_lat`: a float number indicating the latitude target
    `_lon`: a float number indicating the longitude target
    return: the closest valid position
    """
    try_list = np.zeros(0)
    margin = 0
    while len(try_list) != 0:
        margin += 1
        try_list = pos_list[(pos_list[:, 0] < _lat + margin)
                            & (pos_list[:, 0] > _lat - margin) & (pos_list[:, 1] < _lon - margin) & (pos_list[:, 1] > _lon - margin)]
        print(margin)
        print(try_list)
    # find squared distance of every point on grid
    dist_sq = np.sum((try_list - np.array([_lat * 10, _lon * 10])) ** 2, 1)
    print(dist_sq.shape)

    # 1D index of minimum dist_sq element
    return try_list[dist_sq.argmin()]


file = netCDF4.Dataset('raw/C3S-LC-L4-LCCS-Map-300m-P1Y-2022-v2.1.1.nc', 'r')

print(file.variables.keys())
for d in file.dimensions.items():
    print(d)

land = file.variables['lccs_class']
lat = file.variables['lat']
lon = file.variables['lon']
t = file.variables['time']

# print(land.shape)

in_lat = 55.63
in_lon = -4.3

valid_pos = np.zeros((0, 0))
# print(land[0])
print(land.dimensions)
print(t[:])
print(file.variables['time_bounds'][:])

margin = 0
while len(valid_pos) == 0:
    margin += 0.1
    lat_range = np.argwhere(
        (lat[:] < in_lat + margin) & (lat[:] > in_lat - margin))[:, 0]
    lon_range = np.argwhere(
        (lon[:] < in_lon + margin) & (lon[:] > in_lon - margin))[:, 0]
    print(lat_range)
    valid_pos = land[0, lat_range, lon_range]

print(valid_pos)
print(len(valid_pos))
# valid_pos = np.argwhere(land[0].mask == False)

# print('111')
# iy_min, ix_min = getclosest(land[0], in_lat, in_lon)

# print(u.dimensions)
# print(u.shape)

# print(iy_min, ix_min)
# print(land[:, iy_min, ix_min])

# file.close()
