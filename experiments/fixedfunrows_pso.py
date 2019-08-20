"""
Source for experiment with fixed function rows, without coefficients.
Optimized using PSO from PyGMO library.
"""

import sys
import random
from argparse import ArgumentParser

import pygmo as pg
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


class CostFunction:
    def __init__(self, X, Y, engine, bounds):
        self.X = X
        self.Y = Y
        self.engine = engine
        self.bounds = bounds

    def fitness(self, x):
        pred = self.engine.execute(list(x), self.X)

        try:
            return [mean_squared_error(pred, self.Y)]
        except ValueError:
            return [10e10]

    def get_bounds(self):
        return self.bounds
        

def main():
    args = parse_arugments()

    X_train, y_train, X_test, y_test = get_benchmark_data(args.benchmark_name)

    #funset = get_benchmark_funset(args.benchmark_name)
    funset = nguyen7_funset_with_identity

    params = tengp.Parameters(
            n_inputs=2,
            n_outputs=1,
            n_rows=len(funset),
            n_columns=5,
            function_set=funset
        )

    factory = tengp.FixedFunctionRowGenotypeFactory(params) 
    engine = tengp.FixedFunctionRowEngine(params)

    pg.set_global_rng_seed(seed=42)
    with SaveOutput(args.output) as output_file:
        for trial in range(args.trials):
            print(f"Trial {trial}")

            cost_function = CostFunction(
                    X_train, y_train, engine, (factory.l_bounds, factory.u_bounds))

            prob = pg.problem(cost_function)
            algo = pg.algorithm(pg.pso(gen=100))
            algo.set_verbosity(1)
            pop = pg.population(prob, 50)
            pop = algo.evolve(pop)
            uda = algo.extract(pg.pso)


            print([x[2] for x in uda.get_log()], file=output_file)

if __name__ == '__main__':
    main()