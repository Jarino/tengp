import random
from operator import add, sub

from ..individual import IndividualBuilder
from ..mutations import  Move

def hillclimber(X,
        y,
        cost_function,
        params,
        target_fitness=0,
        evaluations=5000,
        initial_solution=None,
        random_state=None,
        verbose=True):
    """ simple hillclimbing algorithm """

    if random_state:
        random.seed(random_state)

    solution = initial_solution

    if not initial_solution:
        ib = IndividualBuilder(params)
        solution = ib.create()


    n_evals = 0
    genereation = 0
    return False
    while n_evals < evaluations:
        generation += 1

        # local move
        # how to perform local move?
        # we can stochastically choose one gene and randomly increase
        # or decrease its value
        # or we can iterate the genotype and try all combinations, unless
        # better one is found
        # for now, let's go with the deterministic route
        # so let's generate and test moves:
        for index, (gene, bound) in enumerate(zip(solution.genes, solution.bounds)):
            ops = []
            if gene != bound:
                ops.append(add)
            if gene != 0:
                ops.append(sub)

            candidates = []
            for operator in ops:
                move = Move([index], [operator(gene, 1)])
                new_solution = solution.apply(move)
                if new_solution == solution:
                    new_solution.fitness = solution.fitness
                else:
                    output = solution.transform(X)
                    new_solution.fitness = cost_function(y, output)
                    n_evals += 1
                candidates.append(new_solution)

            best_candidate = max(candidates, key=lambda x: x.fitness)

            if best_candidate.fitness <= solution.fitness:
                solution = best_candidate

        # test for terminate conditions







