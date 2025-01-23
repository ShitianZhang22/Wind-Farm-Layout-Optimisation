"""
This is the currently used wind farm layout optimisation algorithm using PyGAD library.
Expanding from left to right, then from top to bottom

version 3.0
** Please make sure that 'data/wake0.txt' and 'data/wake1.txt' exist. Otherwise, run pre_computation.py first.

Files in use:
main.py
config.py
fitness_pre.py
pre_computation.py
"""

import pygad
from Optimiser.config import *
# from Optimiser.fitness_pre import fitness_func
# from Optimiser.fitness import fitness_func
import time
# import cProfile

t = time.time()


def on_start(ga):
    print("Initial population\n", ga.initial_population)

 
def on_generation(ga):
    print("Generation", ga.generations_completed)

def optimisation(wt_number, rows, cols):
    global trans_xy

    print('Rows:{}\nColumns:{}'.format(rows, cols))
    print('Number of genes:{}'.format(wt_number))

    # an array can be used in gene_space to manually set all available positions for a turbine
    gene_space = list(range(rows * cols))
    restriction = False # whether there are unavailable cells
    if restriction:
        unavailable = np.loadtxt(r'data/Unavailable_Cells.txt', dtype='int', delimiter=',', encoding='utf-8')
        unavailable = np.argwhere(unavailable.reshape(rows * cols))
        unavailable = unavailable.reshape(unavailable.shape[0])
        for i in range(unavailable.shape[0]-1, -1, -1):
            gene_space.pop(unavailable[i])

    '''
    xy position initialisation
    from 1-D index to xy position
    '''
    xy = np.zeros((rows, cols, 2), dtype='float64')
    for i in range(rows):
        xy[i, :, 1] = i
    for i in range(cols):
        xy[:, i, 0] = i
    xy = xy.reshape(rows * cols, 2)
    xy = xy * cell_width + cell_width / 2
    xy = xy.transpose()

    trans_matrix = np.zeros((len(theta), 2, 2), dtype='float64')
    trans_xy = np.zeros((len(theta), 2, rows * cols), dtype='float64')
    for i in range(len(theta)):
        trans_matrix[i] = np.array(
            [[np.cos(theta[i]), -np.sin(theta[i])],
            [np.sin(theta[i]), np.cos(theta[i])]],
            dtype='float64')
        trans_xy[i] = np.matmul(trans_matrix[i], xy)

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_func,
                           sol_per_pop=sol_per_pop,
                           num_genes=wt_number,
                           gene_type=int,
                           init_range_low=0,
                           init_range_high=rows * cols - 1,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           keep_elitism=keep_elitism,
                           crossover_type=crossover_type,
                           crossover_probability=crossover_probability,
                           mutation_type=mutation_type,
                           mutation_probability=mutation_probability,
                           mutation_by_replacement=mutation_by_replacement,
                           gene_space=gene_space,
                           on_start=None,
                           on_generation=on_generation,
                           suppress_warnings=True,
                           allow_duplicate_genes=False,
                           stop_criteria=stop_criteria,
                           parallel_processing=parallel_processing,
                           random_seed=random_seed,
                           )
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution :\n {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    # print(time.time() - t)
    # ga_instance.plot_fitness()
    return solution

'''
Below is the part of fitness function.
'''
def fitness_func(ga_instance, solution, solution_idx):
    num_genes = ga_instance.num_genes
    fitness = 0  # a specific layout power accumulate
    for ind_t in range(len(theta)):
        # need an extra transpose. the indices will auto trans once
        trans_xy_position = trans_xy[ind_t, :, solution].transpose()

        speed_deficiency = wake(trans_xy_position, num_genes)

        actual_velocity = (1 - speed_deficiency) * velocity[ind_t, 0]
        lp_power = layout_power(actual_velocity, num_genes)  # total power of a specific layout specific wind speed specific theta
        fitness += lp_power.sum() * velocity[ind_t, 1]
    return fitness

def wake(trans_xy_position, n):
    # y value increasingly sort
    sorted_index = np.argsort(trans_xy_position[1, :])
    wake_deficiency = np.zeros(n, dtype='float64')
    for j in range(n):
        for k in range(j):
            dx = np.absolute(trans_xy_position[0, sorted_index[j]] - trans_xy_position[0, sorted_index[k]])
            dy = np.absolute(trans_xy_position[1, sorted_index[j]] - trans_xy_position[1, sorted_index[k]])
            d = cal_deficiency(dx=dx, dy=dy)
            wake_deficiency[sorted_index[k]] += d ** 2
    return np.sqrt(wake_deficiency)


def cal_deficiency(dx, dy):
    r_wake = rotor_radius + entrainment_const * dy
    if dx >= rotor_radius + r_wake:
        intersection = 0
    elif dx > r_wake - rotor_radius:
        alpha = np.arccos((r_wake ** 2 + dx ** 2 - rotor_radius ** 2) / (2 * r_wake * dx))
        beta = np.arccos((rotor_radius ** 2 + dx ** 2 - r_wake ** 2) / (2 * rotor_radius * dx))
        intersection = alpha * r_wake ** 2 + beta * rotor_radius ** 2 - r_wake * dx * np.sin(alpha)
    else:
        intersection = np.pi * rotor_radius ** 2
    return 2.0 / 3.0 * intersection / (np.pi * r_wake ** 2)


def layout_power(v, n):
    power = np.zeros(n, dtype='float64')
    for j in range(n):
        if 2.0 <= v[j] < 18:
            if v[j] < 12.8:
                power[j] = 0.3 * v[j] ** 3
            else:
                power[j] = 629.1
    return power

if __name__ == '__main__':
    optimisation(1)
    # cProfile.run('ga_instance.run()')
    # a = fitness_func(None, [3349, 2685, 3663, 896, 2268, 4090, 266, 3303, 1824, 3428, 964, 163, 2391, 1111, 738, 1044, 3098, 2460, 1804, 2833], 0)
    # print(a)
