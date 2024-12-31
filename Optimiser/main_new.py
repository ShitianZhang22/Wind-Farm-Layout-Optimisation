"""
This is the currently used wind farm layout optimisation algorithm using PyGAD library.
Expanding from left to right, then from top to bottom

version 3.0
** Please make sure that 'data/wake0.txt' and 'data/wake1.txt' exist. Otherwise, run pre_computation.py first.

Files in use:
main_new.py
config.py
fitness_pre.py
pre_computation.py
"""

import pygad
from Optimiser.config import *
# from Optimiser.fitness_pre import fitness_func
from Optimiser.fitness import fitness_func
import time
import cProfile

t = time.time()


def on_start(ga):
    print("Initial population\n", ga.initial_population)

 
def on_generation(ga):
    print("Generation", ga.generations_completed)


ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       gene_type=int,
                       init_range_low=0,
                       init_range_high=init_range_high,
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
if __name__ == '__main__':
    ga_instance.run()
    # cProfile.run('ga_instance.run()')
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution :\n {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    # print(time.time() - t)
    # ga_instance.plot_fitness()
