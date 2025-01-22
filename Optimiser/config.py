"""
This is the configuration file and contains most of the hyperparameters.
"""

import os
import numpy as np
from Wind.main import wind

'''
wind speed data
'''
test_area = [55.7146943, -4.364574, 55.6343709, -4.1830774]
dir = 'Wind/raw/temp.nc'
y = ['2024']
m = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
# m = ['11', '12']

# For speed, the wind data download is disabled, but it can normally work.
# If the wind data needs to be downloaded, the website will be rendered after the data is ready.
# velocity = wind(test_area, dir, y, m)
velocity = wind(test_area, dir, y, m, True)

'''
wind farm data
'''

# wind farm size in cells
rows = 58
cols = 73
# rows = 56
# cols = 75

theta = np.array([0, np.pi / 4.0, np.pi / 2.0, 3 * np.pi / 4.0, np.pi, 5 * np.pi / 4.0, 3 * np.pi / 2.0,
                  7 * np.pi / 4.0], dtype='float64')

hub_height = 80.0  # unit (m)
surface_roughness = 0.25 * 0.001
entrainment_const = 0.5 / np.log(hub_height / surface_roughness)
rotor_radius = 77.0 / 2

'''
hyperparameters for GA
'''

num_generations = 5

sol_per_pop = 10
select_rate = 0.3
num_parents_mating = int(sol_per_pop * select_rate)

# num_genes = 5  # number of wind turbines
# an array can be used in gene_space to manually set all available positions for a turbine
gene_space = list(range(rows * cols))
restriction = False # whether there are unavailable cells
if restriction:
    unavailable = np.loadtxt(r'data/Unavailable_Cells.txt', dtype='int', delimiter=',', encoding='utf-8')
    unavailable = np.argwhere(unavailable.reshape(rows * cols))
    unavailable = unavailable.reshape(unavailable.shape[0])
    for i in range(unavailable.shape[0]-1, -1, -1):
        gene_space.pop(unavailable[i])


cell_width = 77.0 * 2  # unit : m
init_range_high = rows * cols - 1

parent_selection_type = 'sss'
keep_parents = -1

elite_rate = 0.1
keep_elitism = int(sol_per_pop * elite_rate)

crossover_type = 'single_point'
crossover_probability = 0.3  # this is the selection rate for crossover

mutation_type = 'random'
mutation_probability = 0.01  # this is the mutation rate but applies to gene
mutation_by_replacement = True

stop_criteria = None

parallel_processing = None
# parallel_processing = ['process', 10]

random_seed = None
# random_seed = 0

'''
data folder
'''

data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
