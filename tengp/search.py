from array import array
from collections import deque
import random
from functools import partial

from deap import creator, base, cma, algorithms, tools
import numpy as np

from .mutations import MUTATIONS
from .individual import IndividualBuilder
from .parameters import FunctionSet, Parameters
from .utils import round_cma_vector, handle_invalid_decorator, UnknownMutationException

@handle_invalid_decorator
def simple_es(X, y, cost_function, params,
              target_fitness=0,
              population_size=5,
              evaluations=5000,
              random_state=None,
              mutation='point',
              mutation_probability=0.25,
              verbose=False):

    if mutation not in MUTATIONS:
        raise UnknownMutationException("Provided type of mutation is not implemented.")

    move = MUTATIONS[mutation]
    if mutation == 'probabilistic':
        move = partial(move, probability=mutation_probability)

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

        population = [parent.apply(move(parent)) for _ in range(population_size - 1)]

        population += [parent]

        for individual in population:
            output = individual.transform(X)
            individual.fitness = cost_function(y, output)
            n_evals += 1

        if verbose and generation % 100 == 0:
            print(f'Gen: {generation}, population: {sorted([x.fitness for x in population])}')

    population.sort(key=lambda x: x.fitness)
    return population

@handle_invalid_decorator
def gems_es(X, y, cost_function, params):
    pass

@handle_invalid_decorator
def tabu_es(X, y, cost_function, params,
            target_fitness=0,
            population_size=5,
            evaluations=5000,
            random_state=None,
            mutation='point',
            mutation_probability=0.25,
            memory_size=10,
            verbose=False):

    if mutation not in MUTATIONS:
        raise UnknownMutationException("Provided type of mutation is not implemented.")

    move = MUTATIONS[mutation]
    if mutation == 'probabilistic':
        move = partial(move, probability=mutation_probability)

    if random_state:
        random.seed(random_state)

    # initialize memory
    memory = []

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

        population = []
        for _ in range(population_size -1):
            _move = move(parent)

            while _move in memory:
                _move = move(parent)

            if len(memory) > memory_size:
                del memory[0]

            memory.append(_move)

            population.append(parent.apply(_move))

        population = [parent.apply(move(parent)) for _ in range(population_size - 1)]

        population += [parent]

        for individual in population:
            output = individual.transform(X)
            individual.fitness = cost_function(y, output)
            n_evals += 1

        if verbose and generation % 100 == 0:
            print(f'Gen: {generation}, population: {sorted([x.fitness for x in population])}')

    population.sort(key=lambda x: x.fitness)
    return population

@handle_invalid_decorator
def cma_es(X, y, cost_function, params,
           sigma=1,
           lambda_=20,
           evaluations=5000,
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
    creator.create('Individual', array, typecode='f', fitness=creator.FitnessMin)

    strategy = cma.Strategy(
        centroid=initial_solution.genes, sigma=sigma)

    toolbox = base.Toolbox()

    toolbox.register('evaluate', cost_function_wrapper)
    toolbox.register('generate', strategy.generate, creator.Individual)
    toolbox.register('update', strategy.update)
    halloffame = tools.HallOfFame(hof_size)

#    res = algorithms.eaGenerateUpdate(
#        toolbox, ngen=max_generations, halloffame=hof, verbose=verbose)

    # this is just a copy paste of eaGenerateUpdate function, with modification
    # so it can terminate when a maximum number of evaluations is reached
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals', 'total_evals']
    nevals = 0
    gen = 0

    while nevals <= evaluations:
        gen += 1
        # Generate a new population
        population = toolbox.generate()
        # Evaluate the individuals
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        if halloffame is not None:
            halloffame.update(population)

        # Update the strategy with the evaluated individuals
        toolbox.update(population)

        #record = stats.compile(population) if stats is not None else {}
        nevals += len(population)
        logbook.record(gen=gen, nevals=len(population), total_evals=nevals)#, **record)
        if verbose:
            print(logbook.stream)

    # return the best individual
    individual = params.individual_class(round_cma_vector(halloffame[0], bounds), bounds, params)
    output = individual.transform(X)
    individual.fitness = cost_function(y, output)
    return individual, logbook


