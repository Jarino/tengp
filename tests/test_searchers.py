import random
from time import time

import numpy as np
from sklearn.metrics import mean_squared_error

from tengp import hillclimber, FunctionSet, Parameters


def test_hillclimber():
    """ test case for hillclimber search algorithm """
    X = np.array([
        [1],
        [2],
        [3],
        [90],
        [180],
        [1],
    ], dtype=np.float32)

    y = np.array([3, 6, 9, 2, 12, 1])

    funset = FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.multiply, 2)
    funset.add(np.log, 1)

    params = Parameters(1, 1, 1, 3, funset)

    random.seed(0)
    start = time()
    result = hillclimber(X, y, mean_squared_error, params)

    print(f'Hillclimber result: {result}, time: {time() - start}')
