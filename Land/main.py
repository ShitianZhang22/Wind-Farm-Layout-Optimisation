"""
This file is for getting the information of availavle cells and transfer the information into gene space for GA.
Input: the directory path of the wind data downloaded and the wind turbine locations.
Return: available cells marked with genes as gene space.

In the main function for test, the data is stored locally, but this is not necessary when operating.
"""

import netCDF4
import numpy as np
from Land.case import CASE


def land(source, _loc, site=None):
    """
    This function is for information of availavle cells and transfer the information into gene space for GA.
    `source`: a string indicating the directory of the data
    `_loc`: an (n, 2) numpy ndarray including the coordinates (deg) of all wind turbines.
    return: a list including all the feasible cells as the format of gene space for GA.
    """

    with netCDF4.Dataset(source, 'r') as file:

        # print(file.variables.keys())
        # for d in file.dimensions.items():
        #     print(d)

        if site in CASE.keys(): 
            return CASE[site]

        fea = file.variables['feasible']
        lat = file.variables['latitude']
        lon = file.variables['longitude']
         
        ## find the closest location. No need to deal with empty data.
        gene_space = []
        for i in range(_loc.shape[0]):
            dist = np.abs(lat[:] - _loc[i, 0])
            iy_min = dist.argmin()
            dist = np.abs(lon[:] - _loc[i, 1])
            ix_min = dist.argmin()
            if fea[iy_min, ix_min]:
                gene_space.append(i)
        
        # print(gene_space)

        return gene_space
    

def feasibility(source, area):
    """
    This function is for producing raster image of feasibility within the given spatial range
    `source`: a string indicating the directory of the data
    `area`: a list of Northern, Western, Southern, Eastern bounds of the site.
    return: an arraylike image and the spatial bound (2 * 2 list with bot-left and top-right corner)
    """
    with netCDF4.Dataset(source, 'r') as file:
        fea = file.variables['feasible']
        lat = file.variables['latitude']
        lon = file.variables['longitude']

        y_range = np.argwhere((lat[:] < area[0]) & (lat[:] > area[2])).T[0]
        x_range = np.argwhere((lon[:] < area[3]) & (lon[:] > area[1])).T[0]

        # mask has to be removed here, or 'data==0' cannot find anything.
        data = fea[y_range, x_range].data

        image = np.zeros((len(y_range), len(x_range), 4), dtype=np.uint8)
        image[data == 1] = [255, 255, 255, 0]
        image[data == 0] = [0, 0, 0, 50]

        # remove mask
        _lat = lat[:].tolist()
        _lon = lon[:].tolist()

        return image, [[_lat[y_range[-1]], _lon[x_range[0]]], [_lat[y_range[0]], _lon[x_range[-1]]]]

        # return np.asarray(data, dtype=np.uint8), [[lat[y_range[-1]], lon[x_range[0]]], [lat[y_range[0]], lon[x_range[-1]]]]
        
    
if __name__ == '__main__':
    test_data = 'data/infeasible.nc'
    test_lat = 55.6745326
    test_lon = -4.2738257
    test_pos = np.array([
        [55.6350646,  -4.3633451 ],
        [55.63509175, -4.36089957],
        [55.63511886, -4.35845403],
        [55.71298516, -4.18956348],
        [55.71300887, -4.18711292],
        [55.71303253, -4.18466236],
    ])
    print(land(test_data, test_pos))
    # np.savetxt('raw/test_uv.txt', process_wind(test_data, test_lat, test_lon), encoding='utf-8')
