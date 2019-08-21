import warnings
import sys
import random
from argparse import ArgumentParser

import numpy as np
from sklearn.metrics import mean_squared_error

import tengp
from experiments.funsets import nguyen7_funset
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


def main():
    warnings.filterwarnings('ignore')
    
    args = parse_arugments()

    X_train, y_train, X_test, y_test = get_benchmark_data(args.benchmark_name)
    funset = get_benchmark_funset(args.benchmark_name)
    n_inputs, n_outputs = get_benchmark_io(args.benchmark_name)

    params = tengp.Parameters(
            n_inputs=n_inputs,
            n_outputs=n_outputs,
            n_rows=1,
            n_columns=50,
            function_set=funset,
            real_valued=False,
            max_back=20
        )

    with SaveOutput(args.output) as output_file:
        random.seed(42)
        for trial in range(args.trials):
            print(f"{args.benchmark_name}, trial {trial}")

            log = []

            res = tengp.simple_es(
                    X_train,
                    y_train,
                    mean_squared_error,
                    params,
                    evaluations=100000,
                    mutation='single',
                    log=log
                )

            print(log, file=output_file)

if __name__ == '__main__':
    main()
