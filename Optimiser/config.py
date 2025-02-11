"""
This is the configuration file and contains most of the hyperparameters.
"""

import os
import numpy as np

'''
wind farm data
'''

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

cell_width = 77.0 * 2  # unit : m

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
