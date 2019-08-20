"""
Source for experiment with fixed function rows, without coefficients.
Optimized using PSO from PyGMO library.
"""

from time import time
import sys
import random
from argparse import ArgumentParser

import numpy as np
from sklearn.metrics import mean_squared_error

import tengp
from experiments.funsets import nguyen7_funset_with_identity
from experiments.utils import SaveOutput, get_benchmark_data, get_benchmark_funset

def parse_arugments():
    parser = ArgumentParser()
    parser.add_argument("benchmark_name", type=str, help="name of benchmark to run")
    parser.add_argument("--difficulty", "-d", type=str, choices=["train", "test"], help="difficulty of given benchmark")

    parser.add_argument("--trials", "-t", type=int, help="number of repeats of experiment", default=10)
    parser.add_argument("--output", "-o", type=str, help="File, to which resulting logs are stored. If none, stdout is used")

    
    return parser.parse_args()

def create_fitness_fn(engine, X, y):
    def fitness_fn(genotype):
        pred = engine.execute(genotype, X)
        try:
            return mean_squared_error(pred, y)
        except ValueError:
            return 10e10
    return fitness_fn

def mutate_genotype(genotype, l, u):
    #np.random.normal(global_best_genes, scale=(scale*scale_coeff), size=len(global_best_genes))
    # pick random position
    new_genotype = genotype[:]
    for gene in genotype:
        if random.random() > 0.9:
            index = random.randrange(len(genotype))
            new_genotype[index] = np.random.normal(genotype[index], scale=1)
    return new_genotype


def main():
    args = parse_arugments()

    X_train, y_train, X_test, y_test = get_benchmark_data(args.benchmark_name)

    #funset = get_benchmark_funset(args.benchmark_name)
    funset = nguyen7_funset_with_identity

    params = tengp.Parameters(
            n_inputs=2,
            n_outputs=1,
            n_rows=len(funset),
            n_columns=25,
            function_set=funset,
            max_back=25
        )

    factory = tengp.FixedFunctionRowGenotypeFactory(params) 
    engine = tengp.FixedFunctionRowEngine(params)


    with SaveOutput(args.output) as output_file:
        for trial in range(args.trials):
            print(f"Trial {trial}")
            log = []
            fitness = create_fitness_fn(engine, X_train, y_train)
            pop = [factory.get_random_genes() for _ in range(5)]
            global_best_fitness = None
            global_best_genes = None
            
            n_evals = 0
            scale = np.array(np.array(factory.u_bounds) - np.array(factory.l_bounds))
            scale_coeff = 1
            max_evals = 10000
            while n_evals < max_evals:
                scale_coeff = (max_evals + n_evals)/max_evals
                fitnesses = [fitness(genotype) for genotype in pop]
                log.append(fitnesses)
                n_evals += 5
                
                if global_best_fitness is None:
                    global_best_genes = pop[np.argmin(fitnesses)]
                    global_best_fitness = min(fitnesses)

                best_fitness = min(fitnesses)
                if best_fitness <= global_best_fitness:
                    global_best_fitness = best_fitness
                    global_best_genes = pop[np.argmin(fitnesses)]
                
                pop = [mutate_genotype(global_best_genes, factory.l_bounds, factory.u_bounds) for _ in range(5)]



                pop = [np.clip(x, factory.l_bounds, factory.u_bounds) for x in pop]
            print(global_best_fitness)


            print(log, file=output_file)

if __name__ == '__main__':
    start = time()
    main()
    print(f'done in {time() - start}')
