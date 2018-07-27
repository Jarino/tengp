""" Tests for real valued representation of node. """
import math

import pytest
import numpy as np

from tengp.node import RealValuedNode
from tengp import FunctionSet, Parameters
from tengp.individual import NPIndividual
from tengp.utils import map_to_np_phenotype, active_paths

def test_real_valued_mapping():
    funset = FunctionSet()
    funset.add(None, 2)
    genes = [0, 0.1, 0.7, 0, 0, 0, 0, 0.7, 1.2, 4]

    params = Parameters(2, 1, 1, 3, funset)

    nodes = map_to_np_phenotype(genes, params, real_valued=True)

    print(nodes)

    paths = active_paths(nodes, real_valued=True)

    print(paths)

    assert True

def test_mapping_single_node():
    inputs = np.array([[1,2], [3,4]])
    nodes = [np.array([1,3]), np.array([2,4])]
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

    lower_function = (1-a)*( fun_lower((1-b) * nodes[b_lower], b*nodes[b_upper]))

    upper_function = a*( fun_upper((1-c) * nodes[c_lower], c * nodes[c_upper]))

    value = lower_function + upper_function
    print('test', nodes[b_lower], value)

    # assert
    np.testing.assert_allclose(value, [0.92, 2.44])

def test_real_valued_individual_creation():
    funset = FunctionSet()
    funset.add(None, 2)
    genes = [0, 0.1, 0.7, 0, 0, 0, 0, 0.7, 1.2, 4]
    bounds = [0, 1, 1, 0, 2, 2, 0, 3, 3, 4]

    params = Parameters(2, 1, 1, 3, funset, real_valued=True)


    individual = NPIndividual(genes, bounds, params)

    print(individual.active_nodes)

    assert individual.active_nodes == {0, 1, 2, 4, 5}

def test_real_valued_individual_evaluation():
    X = np.array([[1,2], [3,4]])
    funset = FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.multiply, 2)
    genes = [0, 0.1, 0.7, 0, 0, 0, 0, 0.7, 1.2, 4]
    bounds = [0, 1, 1, 0, 2, 2, 0, 3, 3, 4]

    params = Parameters(2, 1, 1, 3, funset, real_valued=True)


    individual = NPIndividual(genes, bounds, params)

    output = individual.transform(X).T[0]

    print(output)

    # assert
    np.testing.assert_allclose(output, [1.7, 3.7])

