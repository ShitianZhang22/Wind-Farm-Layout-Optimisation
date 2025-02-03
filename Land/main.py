"""
This file is for getting the information of availavle cells and transfer the information into gene space for GA.
Input: the directory path of the wind data downloaded and the wind turbine locations.
Return: available cells marked with genes as gene space.

In the main function for test, the data is stored locally, but this is not necessary when operating.
"""

import netCDF4
import numpy as np

def land(source, _loc):
    """
    This function is for getting the historical wind data at a given location.
    `source`: a string indicating the directory of the data
    `_loc`: an (n, 2) numpy ndarray including the coordinates (deg) of all wind turbines.
    return: a list including all the feasible cells as the format of gene space for GA.
    """

    with netCDF4.Dataset(source, 'r') as file:

        # print(file.variables.keys())
        # for d in file.dimensions.items():
        #     print(d)

        fea = file.variables['feasible']
        lat = file.variables['latitude']
        lon = file.variables['longitude']
         
        ## find the closest location. No need to deal with empty data.
        gene_space = []
        for i in range(_loc.shape[0]):
            dist_sq = (lat[:] - _loc[i, 0]) ** 2
            iy_min = dist_sq.argmin()
            dist_sq = (lon[:] - _loc[i, 1]) ** 2
            ix_min = dist_sq.argmin()
            if fea[iy_min, ix_min]:
                gene_space.append(i)

        return gene_space
    

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
