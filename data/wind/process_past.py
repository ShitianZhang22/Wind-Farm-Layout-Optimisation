import netCDF4
import numpy as np

file = netCDF4.Dataset('test/10m_u_component_of_wind_0_daily-mean.nc', 'r')

# print(file)
print(file.variables.keys())
for d in file.dimensions.items():
    print(d)

u = file.variables['u10']
n = file.variables['number']
lat = file.variables['latitude']
lon = file.variables['longitude']
t = file.variables['valid_time']

in_lat = 55.63
in_lon = -4.3 + 360

# extract lat/lon values (in degrees) to numpy arrays
latvals = lat[:]; lonvals = lon[:] 
# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.
def getclosest(lats, latpt):
    # find squared distance of every point on grid
    dist_sq = (lats-latpt)**2 
    # 1D index of minimum dist_sq element
    minindex = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex, lats.shape)
iy_min, ix_min = getclosest(latvals, in_lat), getclosest(lonvals, in_lon)

print(iy_min, ix_min)
print(u.dimensions)
print(u.shape)
print(u[0])

# print(round(in_lat, 1))
# print(round(in_lon, 1))
# print(u[0, 0, 0])

file.close()
