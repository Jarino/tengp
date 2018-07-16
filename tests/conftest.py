import numpy as np
import pytest

from tengp import FunctionSet, Parameters

@pytest.fixture
def function_set():
    funset = FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.multiply, 2)
    return funset

@pytest.fixture
def advanced_function_set():
    funset = FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.multiply, 2)
    funset.add(np.log, 1)
    return funset

@pytest.fixture
def input_data_1d():
    X = np.array([
        [1],
        [2],
        [3],
        [90],
        [180],
        [1],
    ], dtype=np.float32)

    y = np.array([3, 6, 9, 2,  12,  1])

    return X, y
