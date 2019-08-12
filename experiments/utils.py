"""
Various helper stuff for experiments.
"""
import sys
import numpy as np
import random
from experiments.symreg import (
    get_benchmark_nguyen7,
    get_benchmark_nguyen10
)

def add_constant_input(X_train, y_train, X_test, y_test):
    X_train = np.c_[X_train, np.ones(len(X_train))]
    X_test = np.c_[X_test, np.ones(len(X_test))]
    return X_train, y_train, X_test, y_test

def nguyen7():
    random.seed(42)
    return add_constant_input(*get_benchmark_nguyen7(random, None))

def nguyen10():
    random.seed(42)
    return add_constant_input(*get_benchmark_nguyen10(random, None))

BENCHMARKS_LIST = {
    'nguyen7': nguyen7,
    'nguyen10': nguyen10
}

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


def get_benchmark_data(name: str):
    random.seed(42)

    if name not in BENCHMARKS_LIST:
        raise RuntimeError(f"Request benchmark not available, available benchmarks: {list(BENCHMARKS_LIST.keys())}")

    return BENCHMARKS_LIST[name]()


