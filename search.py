from mutations import point_mutation
from individual import IndividualBuilder
from parameters import FunctionSet, Parameters


def evolution_strategy(X, y, cost_function, params,
        target_fitness=0,
        population_size=5,
        evaluations=5000,
        verbose=True):
    # initial generation
    ib = IndividualBuilder(params)

    population = [ib.create() for _ in range(population_size)]

    n_evals = 0

    generation = 0 

    for individual in population:
        output = individual.transform(X)
        individual.fitness = cost_function(X, output)
        n_evals += 1


    while n_evals < evaluations:
        generation += 1
        
        parent = min(population, key=lambda x: x.fitness)

        if parent.fitness <= target_fitness:
            return population
        
        population = [point_mutation(parent) for _ in range(population_size - 1)]

        population += [parent]

        for individual in population:
            output = individual.transform(X)
            individual.fitness = cost_function(X, output)
            n_evals += 1

        print(set([x.fitness for x in population]))

    return population


    

    
