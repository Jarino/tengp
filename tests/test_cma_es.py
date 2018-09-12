""" Tests for CMA-ES optimization method of CGP system """
import random
from time import time

import pytest
from sklearn.metrics import mean_squared_error

from tengp import cma_es, Parameters

@pytest.mark.skip(reason="to be deleted functionality")
def test_cma_es_integration(function_set, input_data_1d):
    """ Test happy path for basic CMA-ES run """
    X, y = input_data_1d

    params = Parameters(1,1,1,3,function_set,use_tensorflow=False)

    random.seed(0)
    start = time()
    hof, result = cma_es(X, y, mean_squared_error, params)

    print(f'CMA-ES hall of fame: {hof}, time: {time() - start}')

    assert True, "passed without error"

@pytest.mark.skip(reason="to be deleted functionality")
def test_integration_with_inf_and_CMA(advanced_function_set, input_data_1d):
    """ Test whether CMA-ES will pass also with NaN or infinity in input for
    cost_function evaluation."""
    X, y = input_data_1d

    params = Parameters(1, 1, 1, 3, advanced_function_set, use_tensorflow=False)

    random.seed(0)
    start = time()
    hof, result = cma_es(X, y, mean_squared_error, params)

    print(f'CMA-ES hall of fame: {hof}, time: {time() - start}')

    assert True, "passed without errors"
