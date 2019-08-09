import sys
import random
from argparse import ArgumentParser

import numpy as np
from sklearn.metrics import mean_squared_error

import tengp
from experiments.symreg import get_benchmark_poly
from experiments.funsets import nguyen7_funset


def parse_arugments():
    parser = ArgumentParser()
    parser.add_argument("benchmark_name", type=str, help="name of benchmark to run")
    parser.add_argument("--difficulty", "-d", type=str, choices=["train", "test"], help="difficulty of given benchmark")

    parser.add_argument("--trials", "-t", type=int, help="number of repeats of experiment", default=10)
    parser.add_argument("--output", "-o", type=str, help="File, to which resulting logs are stored. If none, stdout is used")

    
    return parser.parse_args()

class SaveOutput():
    def __init__(self, filename):
        self.filename = filename
        self.open_file = None

    def __enter__(self):
        if self.filename is None:
            return sys.stdout
        else:
            self.open_file = open(self.filename, 'w')
            return self.open_file

    def __exit__(self, *args):
        if self.open_file is not None:
            self.open_file.close()
        


def main():
    args = parse_arugments()

    print(args)

    params = tengp.Parameters(
            n_inputs=2,
            n_outputs=1,
            n_rows=1,
            n_columns=50,
            function_set=nguyen7_funset,
            real_valued=False,
            max_back=20
        )

    random.seed(42)

    X_train, y_train, X_test, y_test = get_benchmark_poly(random, 6)

    # add constant input
    X_train = np.c_[X_train, np.ones(len(X_train))]
    X_test = np.c_[X_test, np.ones(len(X_test))]

    with SaveOutput(args.output) as output_file:

        for trial in range(args.trials):
            print(f"Trial {trial}")

            log = []

            res = tengp.simple_es(
                    X_train,
                    y_train,
                    mean_squared_error,
                    params,
                    evaluations=100,
                    mutation='single',
                    log=log
                )

            print(log, file=output_file)

if __name__ == '__main__':
    main()
