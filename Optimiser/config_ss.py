"""
This is the configuration file and contains most of the hyperparameters.
This set of configuration is for Steady-State GA. It will converge quickly and rely on mutation to exploit to better results. Therefore, its fitness value is a logarithm function of iterations and will not converge.
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
rotor_radius = 93.0 / 2

'''
hyperparameters for GA
'''

num_generations = 10000

sol_per_pop = 3
num_parents_mating = sol_per_pop - 1

cell_width = rotor_radius * 4  # unit : m

parent_selection_type = 'sss'
keep_parents = -1
# keep_parents = 0

keep_elitism = 0

crossover_type = 'single_point'
crossover_probability = 1

mutation_type = 'random'
mutation_probability = 0.01  # this is the mutation rate but applies to gene
mutation_by_replacement = True

stop_criteria = None
# stop_criteria = 'saturate_200'

'''
processing
'''

save_solutions = True

parallel_processing = None
# parallel_processing = ['process', 10]

# random_seed = None
random_seed = 0

'''
data folder
'''

data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
