""" Tests for real valued representation of node. """
import math

import pytest
import numpy as np

from tengp.node import RealValuedNode
from tengp import FunctionSet

def test_mapping_single_node():
    inputs = np.array([[1,2], [3,4]])
    funset = FunctionSet()

    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.multiply, 2)

    node = RealValuedNode(0.6, [0.7, 0.2])

    # coefficients
    a = node.fun
    b = node.inputs[0]
    c = node.inputs[1]

    fun_lower, _ = funset[math.floor(a)]
    fun_upper, _ = funset[math.ceil(a)]

    # actual indices
    b_lower = math.floor(b)
    b_upper = math.ceil(b)

    # actual indices
    c_lower = math.floor(c)
    c_upper = math.ceil(b)

    lower_function = (1-a)*( fun_lower((1-b) * inputs[:,b_lower], b*inputs[:,b_upper]))

    upper_function = a*( fun_upper((1-c) * inputs[:,c_lower], c * inputs[:,b_upper]))

    value = lower_function + upper_function

    # assert
    np.testing.assert_allclose(value, [0.92, 2.44])






