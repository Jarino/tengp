import random
from operator import add, sub

from ..individual import IndividualBuilder
from ..mutations import  Move

class Memory():
    def __init__(self):
        self.solutions = []

    def add(self, solution):
        self.solutions.append(solution.genes)

    def __contains__(self, solution):
        return solution.genes in self.solutions

    def __repr__(self):
        print('\n'.join(self.solutions))

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

    output = solution.transform(X)
    solution.fitness = cost_function(y, output)

    stats = {'genes': []}
    n_evals = 0
    generation = 0
    memory = Memory()

    while n_evals < evaluations:
        generation += 1
        if verbose:
            print(f'Gen: {generation}, n_evals: {n_evals}, fitness: {solution.fitness}')

        # local move
        # how to perform local move?
        # we can stochastically choose one gene and randomly increase
        # or decrease its value
        # or we can iterate the genotype and try all combinations, unless
        # better one is found
        # for now, let's go with the deterministic route
        # so let's generate and test moves:
        for index, (gene, bound) in enumerate(zip(solution.genes, solution.bounds)):
            # check for possible changes (i.e. can't increase when on upper bound
            ops = []
            if gene != bound:
                ops.append(add)
            if gene != 0:
                ops.append(sub)

            if len(ops) == 0:
                continue # not possible change for given gene

            candidates = []
            for operator in ops:
                new_gene = operator(gene, 1)
                move = Move([index], [new_gene])
                new_solution = solution.apply(move)
                while new_solution in memory:
                    new_gene = operator(new_gene, 1)
                    if new_gene > bound or new_gene < 0:
                        new_solution = None
                        break
                    move = Move([index], [new_gene])
                    new_solution = solution.apply(move)

                if new_solution is None:
                    continue

                memory.add(new_solution)

                if new_solution == solution:
                    new_solution.fitness = solution.fitness
                else:
                    output = solution.transform(X)
                    new_solution.fitness = cost_function(y, output)
                    n_evals += 1

                stats['genes'].append(new_solution.genes)
                candidates.append(new_solution)

            if len(candidates) == 0:
                continue

            best_candidate = max(candidates, key=lambda x: x.fitness)

            if best_candidate.fitness <= solution.fitness:
                solution = best_candidate

        if solution.fitness <= target_fitness:
            break

    stats['n_evals'] = n_evals
    stats['generations'] = generation
    return solution, stats






