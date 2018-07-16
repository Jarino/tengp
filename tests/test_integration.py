from time import time
import random

import numpy as np
import pytest
from sklearn.metrics import mean_squared_error

from tengp import Parameters, FunctionSet, evolution_strategy

def test_integration(function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 3, function_set, use_tensorflow=False)

    random.seed(0)
    start = time()
    result = evolution_strategy(X, y, mean_squared_error, params)

    print(f'Numpy result: {result}, time: {time() - start}')

    assert True, "passed without errors"


@pytest.mark.skip
def test_integration_with_inf(advanced_function_set, input_data_1d):
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 3, advanced_function_set, use_tensorflow=False)

    random.seed(0)
    start = time()
    result = evolution_strategy(X, y, mean_squared_error, params)

    print(f'Numpy result: {result}, time: {time() - start}')

    assert True, "passed without errors"

