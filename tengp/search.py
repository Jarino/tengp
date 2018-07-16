from collections import deque
import random

from deap import creator, base, cma, algorithms, tools

from .mutations import point_mutation
from .individual import IndividualBuilder
from .parameters import FunctionSet, Parameters
from .utils import round_cma_vector, handle_invalid_decorator

@handle_invalid_decorator
def simple_es(X, y, cost_function, params,
              target_fitness=0,
              population_size=5,
              evaluations=5000,
              random_state=None,
              verbose=False):

    if random_state:
        random.seed(random_state)

    # initial generation
    ib = IndividualBuilder(params)

    population = [ib.create() for _ in range(population_size)]

    n_evals = 0

    generation = 0

    for individual in population:
        output = individual.transform(X)
        individual.fitness = cost_function(y, output)
        n_evals += 1


    while n_evals < evaluations:
        generation += 1

        parent = min(population, key=lambda x: x.fitness)

        if parent.fitness <= target_fitness:
            return population

        population = [parent.apply(point_mutation(parent)) for _ in range(population_size - 1)]

        population += [parent]

        for individual in population:
            output = individual.transform(X)
            individual.fitness = cost_function(y, output)
            n_evals += 1

        if verbose and generation % 100 == 0:
            print(f'Gen: {generation}, population: {sorted([x.fitness for x in population])}')

    return population


def cma_es(X, y, cost_function, params,
           sigma=1,
           lambda_=20,
           max_generations=250,
           hof_size=1,
           random_state=None,
           verbose=False):
    """ Optimizes the CGP system using the CMA-ES algorithm (DEAP library). 
    Returns the hall of fame object and result object in a tuple."""
    builder = IndividualBuilder(params)
    initial_solution = builder.create()
    bounds = initial_solution.bounds[:]

    if random_state:
        random.seed(random_state)

    def cost_function_wrapper(cma_vector):
        """ Wrapper for user provided cost function, so it works with DEAP """
        genes = round_cma_vector(cma_vector, bounds)
        individual = params.individual_class(genes, bounds, params)
        output = individual.transform(X)
        return cost_function(output, y),

    # deap shit
    creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    strategy = cma.Strategy(
        centroid=initial_solution.genes, sigma=sigma, lambda_=lambda_*len(bounds))

    toolbox = base.Toolbox()

    toolbox.register('evaluate', cost_function_wrapper)
    toolbox.register('generate', strategy.generate, creator.Individual)
    toolbox.register('update', strategy.update)
    hof = tools.HallOfFame(hof_size)

    res = algorithms.eaGenerateUpdate(
        toolbox, ngen=max_generations, halloffame=hof, verbose=verbose)

    # return the best individual
    individual = params.individual_class(round_cma_vector(hof[0], bounds), bounds, params)
    output = individual.transform(X)
    individual.fitness = cost_function(y, output)
    return individual, res


