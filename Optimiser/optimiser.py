from Optimiser.main_new import *

def optimisation():
    ga_instance.run()
    # cProfile.run('ga_instance.run()')
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution :\n {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    return solution
    # print(time.time() - t)
    # ga_instance.plot_fitness()
