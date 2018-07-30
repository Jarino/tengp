""" Tests for real valued representation of node. """
import math

import pytest
import numpy as np

from tengp.node import RealValuedNode
from tengp import FunctionSet, Parameters
from tengp.individual import NPIndividual, IndividualBuilder
from tengp.utils import map_to_np_phenotype, active_paths

@pytest.mark.skip
def test_real_valued_mapping():
    funset = FunctionSet()
    funset.add(None, 2)
    genes = [0, 0.1, 0.7, 0, 0, 0, 0, 0.7, 1.2, 4]

    params = Parameters(2, 1, 1, 3, funset)

    nodes = map_to_np_phenotype(genes, params, real_valued=True)

    paths = active_paths(nodes, real_valued=True)

    assert True


@pytest.mark.skip
def test_real_valued_individual_creation():
    funset = FunctionSet()
    funset.add(None, 2)
    genes = [0, 0.1, 0.7, 0, 0, 0, 0, 0.7, 1.2, 4]
    bounds = [0, 1, 1, 0, 2, 2, 0, 3, 3, 4]

    params = Parameters(2, 1, 1, 3, funset, real_valued=True)


    individual = NPIndividual(genes, bounds, params)


    assert individual.active_nodes == {0, 1, 2, 4, 5}

@pytest.mark.skip
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


    # assert
    np.testing.assert_allclose(output, [1.7, 3.7])


def test_same_output():
    """ Classic integer individuals should output the same  value as the real
    valued individual with same genes"""

    X = np.array([[1,2], [3,4]])

    def pdivide(x, y):
        return np.divide(x, y, out=np.copy(x), where=x!=0)

    funset = FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.multiply, 2)
    funset.add(pdivide, 2)

    genes = [2, 1, 0, 0, 1, 0, 2, 2, 1, 2, 3, 2, 2, 5, 5, 2, 5, 4, 0, 7, 6, 1, 0, 1, 1, 8, 9, 2, 1, 8, 8]
    params = Parameters(2, 1, 1, 10, funset)
    rv_params = Parameters(2, 1, 1, 10, funset, real_valued=True)
    bounds = IndividualBuilder(params).create().bounds[:]


    int_individual = params.individual_class(genes, bounds, params)


    int_output = int_individual.transform(X)
    print(int_output)

    rv_individual = rv_params.individual_class(genes, bounds, rv_params)

    rv_output = rv_individual.transform(X)
    print(rv_output)

    #assert int_output == rv_output
    np.testing.assert_allclose(int_output, rv_output)

