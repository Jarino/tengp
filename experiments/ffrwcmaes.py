"""
Source for experiment with fixed function rows, with coefficients.
Optimized using PSO from PyGMO library.
"""

import sys
import random
import math
from argparse import ArgumentParser

import pygmo as pg
from sklearn.metrics import mean_squared_error

import tengp
from experiments.utils import (
    SaveOutput,
    get_benchmark_data,
    get_benchmark_funset,
    get_benchmark_io
)

def parse_arugments():
    parser = ArgumentParser()
    parser.add_argument("benchmark_name", type=str, help="name of benchmark to run")
    parser.add_argument("--difficulty", "-d", type=str, choices=["train", "test"], help="difficulty of given benchmark")

    parser.add_argument("--trials", "-t", type=int, help="number of repeats of experiment", default=10)
    parser.add_argument("--output", "-o", type=str, help="File, to which resulting logs are stored. If none, stdout is used")

    
    return parser.parse_args()

def trans(a, b, x):
    return a + (b-a) * (1-math.cos(math.pi * x / 10)) /2

class CostFunction:
    def __init__(self, X, Y, engine, bounds):
        self.X = X
        self.Y = Y
        self.engine = engine
        self.bounds = bounds
        self.cma_bounds = ([0]*len(self.bounds[0]), [10]*len(self.bounds[1]))

    def fitness(self, x):
        # x should come in cma_bounds, so [0, 10]
        # therefore we need to map it back to our domain
        transformed_genotype = []
        for gene, l, u in zip(x, self.bounds[0], self.bounds[1]):
            transformed_genotype.append(trans(l,u,gene))

        pred = self.engine.execute(transformed_genotype, self.X)

        try:
            return [mean_squared_error(pred, self.Y)]
        except ValueError:
            return [10e10]

    def get_bounds(self):
        return self.cma_bounds
        
def identity(x, y):
    return x

def main():
    args = parse_arugments()

    X_train, y_train, X_test, y_test = get_benchmark_data(args.benchmark_name)
    funset = get_benchmark_funset(args.benchmark_name)
    n_inputs, n_outputs = get_benchmark_io(args.benchmark_name)

    params = tengp.Parameters(
            n_inputs=n_inputs,
            n_outputs=n_outputs,
            n_rows=len(funset),
            n_columns=50//len(funset),
            function_set=funset,
            max_back=1
        )

    factory = tengp.FFRCoeffGenotypeFactory(params, 0, 1) 
    engine = tengp.FFRWeightEngine(params)

    pg.set_global_rng_seed(seed=42)
    with SaveOutput(args.output) as output_file:
        for trial in range(args.trials):
            print(f"Trial {trial}")

            cost_function = CostFunction(
                    X_train, y_train, engine, (factory.l_bounds, factory.u_bounds))

            prob = pg.problem(cost_function)
            algo = pg.algorithm(pg.cmaes(gen=5000, sigma0=0.1))
            algo.set_verbosity(1)
            pop = pg.population(prob, 20)
            pop = algo.evolve(pop)
            uda = algo.extract(pg.cmaes)


            print([x[2] for x in uda.get_log()], file=output_file)

if __name__ == '__main__':
    main()
