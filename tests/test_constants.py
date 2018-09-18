""" Test suite for constants """
import pytest
import numpy as np

from tengp import FunctionSet, Parameters
from tengp.individual import NPIndividual, IndividualBuilder
from tengp.utils import map_to_np_phenotype, active_paths

def test_constant_node():
    def constant(x, y):
        return x

    funset = FunctionSet()
    funset.add(constant, 0)
    funset.add(np.add, 2)
    genes = [0, 0, 0, 4.55, 1]
    params = Parameters(1, 1, 1, 1, funset, real_valued=True, constants=100)

    bounds = IndividualBuilder(params).create().bounds

    assert bounds == ([0, 0, 0, 0, 0], [1, 0, 0, 100, 1])

    individual = params.individual_class(genes, bounds, params)
    output = individual.transform(np.array([1, 2]).reshape(-1, 1))
    assert (output == np.array([[4.55], [4.55]])).all()

def test_constant_multiple_nodes():
    def constant(x, y):
        return x

    funset = FunctionSet()
    funset.add(constant, 0)
    funset.add(np.add, 2)
    genes = [0, 0, 0, 4.55, 1, 0, 1, 6.66, 2]
    params = Parameters(1, 1, 1, 2, funset, real_valued=True, constants=100)

    bounds = IndividualBuilder(params).create().bounds

    assert bounds == ([0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 100, 1, 1, 1, 100, 2])

    individual = params.individual_class(genes, bounds, params)

    assert individual.paths == [[0, 0, 1, 2, 3]]

    output = individual.transform(np.array([1, 2]).reshape(-1, 1))
    assert (output == np.array([[5.55], [6.55]])).all()


