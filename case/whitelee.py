"""
This file is not part of the website, but is used once to get the bounding box of the Whitelee Wind Farm.
"""

import pandas as pd
import openpyxl
import numpy as np
from crs_init import CRSConvertor

df = pd.read_excel('Turbines_At_Whitelee_Wind_Farm.xlsx', index_col=0).iloc[:, :2]

# The bound below is from the spatial range of the original wind turbines
bound1 = [df['Latitude'].max(), df['Longitude'].min(), df['Latitude'].min(), df['Longitude'].max()]
print('The original spatial bound according to the wind turbines is {}'.format(bound1))
conv = CRSConvertor(bound1)

cell_size = 154
# Get the Southwestern (bottom left) corner of the site, and expand further at half of a cell
corner1 = list(conv.to_pcs(bound1[2], bound1[1]))
corner1[0] -= cell_size / 2
corner1[1] -= cell_size / 2
# Get the Northeastern (top right) corner of the site, and expand further at half of a cell
corner2 = list(conv.to_pcs(bound1[0], bound1[3]))
corner2[0] += cell_size / 2
corner2[1] += cell_size / 2

# based on the two corner points above, get the input bounding box of the wind farm
corner1_gcs = list(conv.to_gcs(corner1[0], corner1[1]))
corner2_gcs = list(conv.to_gcs(corner2[0], corner2[1]))
bound2 = [corner2_gcs[0], corner1_gcs[1], corner1_gcs[0], corner2_gcs[1]]
print('The input spatial range is {}'.format(bound2))

'''
[55.714704134580245,
-4.364543821199962,
55.634359319706036,
-4.183104393719847]
'''

# print(conv.to_gcs(orient[0], orient[1]))

rows = int((corner2[0] - corner1[0]) // cell_size)
cols = int((corner2[1] - corner1[1]) // cell_size)
print('rows:{}\ncols:{}'.format(rows, cols))

# Set the Southwestern corner of the site as the origin, 
# and cut the northern and eastern edge of the site to fit the cell size
corner3= [corner1[0] + cell_size * rows, corner1[1] + cell_size * cols]
bound2 = [corner3[0], corner1[1], corner1[0], corner3[1]]

print('The pcs of the site boundary is:', bound2)

corner1_gcs = list(conv.to_gcs(corner1[0], corner1[1]))
corner3_gcs = list(conv.to_gcs(corner3[0], corner3[1]))
bound2_gcs = [corner3_gcs[0], corner1_gcs[1], corner1_gcs[0], corner3_gcs[1]]
print('The gcs of the site boundary is:', bound2_gcs)

# get all the grid centres and the corresponding PCS
grid_pcs = np.zeros((rows, cols, 2), dtype='float64')
temp = corner1[0] + cell_size / 2
for i in range(rows):
    grid_pcs[i, :, 0] = temp
    temp += cell_size
temp = corner1[1] + cell_size / 2
for i in range(cols):
    grid_pcs[:, i, 1] = temp
    temp += cell_size

# Then convert the coordinates to GCS and flatten the grid
grid_gcs = np.zeros((rows, cols, 2), dtype='float64')
for i in range(rows):
    for j in range(cols):
        grid_gcs[i, j, 0], grid_gcs[i, j, 1] = conv.to_gcs(grid_pcs[i, j, 0], grid_pcs[i, j, 1])
grid_gcs = grid_gcs.reshape(rows * cols, 2)

print(grid_gcs)
print(grid_gcs.shape)

# save the file for coordinate-gene conversion
# np.savetxt('grid.txt', grid_gcs, fmt='%f', encoding='utf-8')
