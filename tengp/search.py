from collections import deque
import random

from .mutations import point_mutation
from .individual import IndividualBuilder
from .parameters import FunctionSet, Parameters


def evolution_strategy(X, y, cost_function, params,
        target_fitness=0,
        population_size=5,
        evaluations=5000,
        random_state=None,
        verbose=True):

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


def tabu_search(X, y, cost_function, params,
        target_fitness=0,
        evaluations=5000,
        memory_size=10,
        random_state=None,
        verbose=True):
        
        same = 0
        cycles = 0

        if random_state:
            random.seed(random_state)

        n_evals = 0
        memory = deque(maxlen=memory_size)

        ib = IndividualBuilder(params)

        individual = ib.create()

        output = individual.transform(X)
        individual.fitness = cost_function(y, output)
        n_evals += 1


        while n_evals < evaluations:
            if verbose and n_evals % 500 == 0:
                print(f'N_evals: {n_evals}, fitness: {individual.fitness}')

            # generate moves
            moves = [point_mutation(individual) for _ in range(5)]
            
            children = []

            for move in moves:
                child = individual.apply(move)
                if child == individual:
                    child.fitness = individual.fitness
                else:
                    output = child.transform(X)
                    child.fitness = cost_function(y, output)
                    n_evals += 1
                children.append((child, move))

            children.sort(key=lambda x: x[0].fitness)
            
            best = children[0]
            
            if best[0] in memory:
                same += 1
                continue

            individual = best[0]
            memory.append(best[0])




        return individual, same, cycles

