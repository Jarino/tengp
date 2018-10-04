from time import time
import random

import numpy as np
import pytest

from tengp import Parameters, simple_es
from tengp.utils import UnknownMutationException

def mean_squared_error(y_true, y_pred):
    return np.square(np.subtract(y_true, y_pred)).mean()

def print_result(result, start):
    print(f'Numpy result: {result}, time: {time() - start}')

def test_simple_es(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 3, function_set)

    random.seed(0)
    start = time()
    result = simple_es(X, y, mean_squared_error, params)

    print_result(result, start)

    assert True, "passed without errors"

def test_simple_es_with_log(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 3, function_set)
    log = []

    random.seed(0)
    start = time()
    result = simple_es(X, y, mean_squared_error, params, log=log)

    print_result(result, start)

    assert len(log) > 0

    assert True, "passed without errors"


def test_simple_es_with_inf(advanced_function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 3, advanced_function_set)

    random.seed(0)
    start = time()
    result = simple_es(X, y, mean_squared_error, params)

    print_result(result, start)

    assert True, "passed without errors"

def test_simple_es_with_single_mutation(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 4, function_set)

    random.seed(0)
    start = time()
    result = simple_es(X, y, mean_squared_error, params, mutation='single')

    print_result(result, start)

    assert True, "passed without errors"

def test_simple_es_with_active_mutation(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 4, function_set)

    random.seed(0)
    start = time()
    result = simple_es(X, y, mean_squared_error, params, mutation='active')

    print_result(result, start)

    assert True, "passed without errors"

def test_simple_es_with_probabilistic_mutation(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 4, function_set)

    random.seed(0)
    start = time()
    result = simple_es(X, y, mean_squared_error, params, mutation='probabilistic')

    print_result(result, start)

    assert True, "passed without errors"

def test_simple_es_with_non_existing_mutation(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 4, function_set)

    random.seed(0)
    try:
        _ = simple_es(X, y, mean_squared_error, params, mutation='rofl')
        assert False, "passed without expected exception"
    except UnknownMutationException:
        assert True, "mutation fired, good"

