"""
This is the currently used wind farm layout optimisation algorithm using PyGAD library.
Expanding from left to right, then from top to bottom

Files in use:
main.py
config.py
"""

import pygad
from Optimiser.config import *
# from Optimiser.config_ss import *  # This is the version for steady-state selection
# from Optimiser.fitness_pre import fitness_func
import time
# import cProfile

# locally define a variable for storing the wind data
_wind_data = None


def on_start(ga):
    global t
    global log
    global best_layout
    global best_fitness
    t = time.time()
    log = []
    best_fitness = 0
    best_layout= []
    # print("Initial population\n", ga.initial_population)

 
def on_generation(ga):
    """
    This function is for recording the time cost of each generation and plotting fitness curve.
    """
    # global log
    # print("Generation {}: time cost: {:.1f}; fitness:{:.0f}".format(ga.generations_completed, time.time() - t, ga.best_solutions_fitness[-1]))
    # log.append([time.time() - t, ga.best_solutions_fitness[-1]])

    # The following part is for Steady-State version, which has too many generations.
    if ga.generations_completed % 10 == 0:
        global log
        print("Generation {}: time cost: {:.1f}; fitness:{:.0f}".format(ga.generations_completed, time.time() - t, ga.best_solutions_fitness[-1]))
        log.append([time.time() - t, ga.best_solutions_fitness[-1]])


def on_stop(ga, last_fit):
    """
    This function is for saving a log including the running time and fitness value of each generation.
    """
    _log = np.array(log, dtype='float64')
    np.savetxt('log/log.csv', _log, fmt='%f', delimiter=',', encoding='utf-8')


def optimisation(wt_number, rows, cols, wind_data, feasible_loc=None):
    """
    This is the main function of optimisation. It is called once when the user send an optimisation request.
    First, it prepares some variables used for optimisation.
    Then it creates an Pygad.GA instance and runs the optimisation.
    Finally, it provides the summary for the optimal layout.
    `wt_number`: an integer of wind turbine numbers.
    `rows` and `cols`: integers of rows and columns in the grid.
    `wind`:  an (8, 2) ndarray of the average wind speed and frequency at 8 directions
    `feasible_loc`: a list of feasible locations represented by genes. If it is None, then all positions are regareded feasible.
    """
    global trans_xy
    global _wind_data

    print('Rows:{}\nColumns:{}'.format(rows, cols))
    # print('Number of genes:{}'.format(wt_number))

    # print(wt_number, rows, cols, wind_data, feasible_loc)

    '''
    Parameter preparation.
    '''

    # store the local data into global varialbes
    _wind_data = wind_data.copy()
    if feasible_loc is None:
        # an array can be used in gene_space to manually set all available positions for a turbine
        gene_space = list(range(rows * cols))
    else:
        gene_space = feasible_loc

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

    # trans_matrix is for rotating the coordinates to fit different wind directions.
    trans_matrix = np.zeros((len(theta) // 2, 2, 2), dtype='float64')
    trans_xy = np.zeros((len(theta) // 2, rows * cols, 2), dtype='float64')
    for i in range(len(theta) // 2):
        trans_matrix[i] = np.array(
            [[np.cos(theta[i]), -np.sin(theta[i])],
            [np.sin(theta[i]), np.cos(theta[i])]],
            dtype='float64')
        trans_xy[i] = np.matmul(trans_matrix[i], xy).transpose()
    
    '''
    Optimisation.
    '''
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
                           on_start=on_start,
                           on_generation=on_generation,
                           on_stop=on_stop,
                           suppress_warnings=False,
                           allow_duplicate_genes=False,
                           stop_criteria=stop_criteria,
                           parallel_processing=parallel_processing,
                           random_seed=random_seed,
                           save_solutions=save_solutions,
                           save_best_solutions=True,
                           )
    ga_instance.run()
    # The next line is the best solution in the last generation, which may not be historically best.
    # solution, solution_fitness, solution_idx = ga_instance.best_solution()
    solution = ga_instance.best_solutions[ga_instance.best_solution_generation]
    print("The best solution :\n {}".format(solution.tolist()))
    # print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    # print(time.time() - t)
    # ga_instance.plot_fitness()

    '''
    Summary
    (The content is similar to fitness_func())
    '''
    num_genes = len(solution)
    wt_summary = np.zeros((num_genes,), dtype='float64')
    ideal_power = 0  # the ideal power of a wind turbine (kW)
    for ind_t in range(len(theta) // 2):
        trans_xy_position = trans_xy[ind_t, solution, :]

        speed_deficiency0, speed_deficiency1 = wake(trans_xy_position, num_genes)

        actual_velocity = (1 - speed_deficiency0) * _wind_data[ind_t, 0]
        lp_power = layout_power(actual_velocity, num_genes)  # total power of a specific layout specific wind speed specific theta
        wt_summary += lp_power * _wind_data[ind_t, 1]  # the weight of wind frequency at a given direction
        ideal_power += layout_power([_wind_data[ind_t, 0]], 1)[0] * _wind_data[ind_t, 1]

        actual_velocity = (1 - speed_deficiency1) * _wind_data[ind_t + 4, 0]
        lp_power = layout_power(actual_velocity, num_genes)  # total power of a specific layout specific wind speed specific theta
        wt_summary += lp_power * _wind_data[ind_t + 4, 1]  # the weight of wind frequency at a given direction
        ideal_power += layout_power([_wind_data[ind_t + 4, 0]], 1)[0] * _wind_data[ind_t + 4, 1]
    
    if ideal_power != 0:  # avoid the scenario of dividing zero
        wt_efficiency = wt_summary / ideal_power
    else:
        wt_efficiency = np.zeros((num_genes,), dtype='float64')
    efficiency = wt_efficiency.mean()
    '''
    The power prediction is not correct at the moment.
    Unit: MWh
    '''
    # wt_summary *= 24 * 365 * 0.3 / 1000
    wt_summary *= 24 * 365 * 56 / 1000
    # print(wt_summary.sum(), efficiency, wt_summary, wt_efficiency)

    # wt = pd.DataFrame({
    #     'Annual Energy Production': wt_summary,
    #     'Efficiency': wt_efficiency
    #     })

    wt = np.array([wt_summary, wt_efficiency], dtype='float64').T
    
    # print(wt)
    
    return solution, float(wt_summary.sum()), float(efficiency), wt

'''
Below is the part of fitness function.
'''
def fitness_func(ga_instance, solution, solution_idx):
    num_genes = ga_instance.num_genes
    fitness = 0  # a specific layout power accumulate
    for ind_t in range(len(theta) // 2):
        trans_xy_position = trans_xy[ind_t, solution, :]
        # print(trans_xy_position.shape)

        speed_deficiency0, speed_deficiency1 = wake(trans_xy_position, num_genes)

        # total power of a specific layout under a wind direction
        actual_velocity = (1 - speed_deficiency0) * _wind_data[ind_t, 0]
        lp_power = layout_power(actual_velocity, num_genes)
        fitness += lp_power.sum() * _wind_data[ind_t, 1]
        # calculation for the opposite wind direction
        actual_velocity = (1 - speed_deficiency1) * _wind_data[ind_t + 4, 0]
        lp_power = layout_power(actual_velocity, num_genes)
        fitness += lp_power.sum() * _wind_data[ind_t + 4, 1]
    return fitness


def wake(trans_xy_position, n):
    """
    This function is used by fitness_func().
    """
    # y value increasingly sort
    sorted_index = np.argsort(trans_xy_position[:, 1])
    wake_deficiency0 = np.zeros(n, dtype='float64')
    wake_deficiency1 = np.zeros(n, dtype='float64')
    for j in range(n):
        for k in range(j):
            dx = np.absolute(trans_xy_position[sorted_index[j], 0] - trans_xy_position[sorted_index[k], 0])
            dy = np.absolute(trans_xy_position[sorted_index[j], 1] - trans_xy_position[sorted_index[k], 1])
            d = cal_deficiency(dx=dx, dy=dy)
            # calculate the wake deficiency in two opposite directions at the same time.
            wake_deficiency0[sorted_index[k]] += d ** 2
            wake_deficiency1[sorted_index[j]] += d ** 2
    return np.sqrt(wake_deficiency0), np.sqrt(wake_deficiency1)


def cal_deficiency(dx, dy):
    """
    This function is used by wake().
    """
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
    """
    This function is used by fitness_func().
    Power unit: kW
    """
    power = np.zeros(n, dtype='float64')
    for j in range(n):
        if 2.0 <= v[j] < 18:
            if v[j] < 12.8:
                power[j] = 0.3 * v[j] ** 3
            else:
                power[j] = 629.1
    return power


if __name__ == '__main__':
    # optimisation(1)
    # cProfile.run('ga_instance.run()')
    a = optimisation([3349, 2685, 3663, 896, 2268, 4090, 266, 3303, 1824, 3428, 964, 163, 2391, 1111, 738, 1044, 3098, 2460, 1804, 2833])
    print(a)
 