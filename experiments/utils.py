"""
Various helper stuff for experiments.
"""
import sys
import numpy as np
import random
from experiments.symreg import (
    get_benchmark_poly,
    get_benchmark_nguyen7,
    get_benchmark_nguyen8,
    get_benchmark_nguyen10,
    get_benchmark_keijzer,
    get_benchmark_korns,
    get_benchmark_pagie1,
    get_benchmark_vladislasleva4
)
from experiments.funsets import (
    nguyen7_funset,
    keijzer_funset,
    korns_funset,
    pagie_funset,
    vlad_funset
)

def add_constant_input(X_train, y_train, X_test, y_test):
    X_train = np.c_[X_train, np.ones(len(X_train))]
    X_test = np.c_[X_test, np.ones(len(X_test))]
    return X_train, y_train, X_test, y_test


def nguyen4():
    random.seed(42)
    return add_constant_input(*get_benchmark_poly(random, 6))

def nguyen7():
    random.seed(42)
    return add_constant_input(*get_benchmark_nguyen7(random, None))

def nguyen8():
    random.seed(42)
    return add_constant_input(*get_benchmark_nguyen8(random, None))

def nguyen10():
    random.seed(42)
    return add_constant_input(*get_benchmark_nguyen10(random, None))

def keijzer4():
    random.seed(42)
    return add_constant_input(*get_benchmark_keijzer(random, 1))

def keijzer11():
    random.seed(42)
    return add_constant_input(*get_benchmark_keijzer(random, 10))

def keijzer12():
    random.seed(42)
    return add_constant_input(*get_benchmark_keijzer(random, 11))

def korns1():
    random.seed(42)
    return add_constant_input(*get_benchmark_korns(random, 1))

def korns7():
    random.seed(42)
    return add_constant_input(*get_benchmark_korns(random, 7))

def korns12():
    random.seed(42)
    return add_constant_input(*get_benchmark_korns(random, 12))

def pagie1():
    random.seed(42)
    return add_constant_input(*get_benchmark_pagie1(random, None))

def vladislasleva4():
    random.seed(42)
    return add_constant_input(*get_benchmark_vladislasleva4(random, None))

BENCHMARKS_LIST = {
    'nguyen4': nguyen4,
    'nguyen7': nguyen7,
    'nguyen8': nguyen8,
    'nguyen10': nguyen10,
    'keijzer4': keijzer4,
    'keijzer11': keijzer11,
    'keijzer12': keijzer12,
    'korns1': korns1,
    'korns7': korns7,
    'korns12': korns12,
    'pagie1': pagie1,
    'vladislasleva4': vladislasleva4
}

FUNSETS = {
    'nguyen4': nguyen7_funset,
    'nguyen7': nguyen7_funset,
    'nguyen8': nguyen7_funset,
    'nguyen10': nguyen7_funset,
    'keijzer4': keijzer_funset,
    'keijzer11': keijzer_funset,
    'keijzer12': keijzer_funset,
    'korns1': korns_funset,
    'korns7': korns_funset,
    'korns12': korns_funset,
    'pagie1': pagie_funset,
    'vladislasleva4': vlad_funset
}

BENCHMARKS_IO = {
    'nguyen4': (2,1),
    'nguyen7': (2,1),
    'nguyen8': (2,1),
    'nguyen10': (3,1),
    'keijzer4': (2,1),
    'keijzer11': (3,1),
    'keijzer12': (3,1),
    'korns1': (5,1),
    'korns7': (2,1),
    'korns12': (6, 1),
    'pagie1': (3,1),
    'vladislasleva4': (6,1) 
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
    if name not in BENCHMARKS_LIST:
        raise RuntimeError(f"Request benchmark not available, available benchmarks: {list(BENCHMARKS_LIST.keys())}")

    return BENCHMARKS_LIST[name]()

def get_benchmark_funset(name: str):
    if name not in FUNSETS:
        raise RuntimeError(f"Request funset for given benchmark not available, available funsets: {list(FUNSETS.keys())}")

    return FUNSETS[name]

def get_benchmark_io(name: str):
    if name not in BENCHMARKS_IO:
        raise RuntimeError(f"Request io for given benchmark not available, available funsets: {list(FUNSETS.keys())}")
    return BENCHMARKS_IO[name]

