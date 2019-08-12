""" Test suite for genotype factory """
import numpy as np

import tengp


def test_bounds_wo_max_back():
    """ Should create an individual with lower and upper bounds
    according to max_back attribute. """
    funset = tengp.FunctionSet()
    funset.add(np.add, 2)
    params = tengp.Parameters(2, 1, 1, 6, funset)

    factory = tengp.genotype_factory.GenotypeFactory(params)
    l_bounds, u_bounds = factory.get_bounds()
    genes = factory.get_random_genes()

    assert l_bounds == [0, 0, 0,
                        0, 0, 0,
                        0, 0, 0,
                        0, 0, 0,
                        0, 0, 0,
                        0, 0, 0,
                        0]

    assert u_bounds == [0, 1, 1,
                        0, 2, 2,
                        0, 3, 3,
                        0, 4, 4,
                        0, 5, 5,
                        0, 6, 6,
                        7]

def test_bounds_w_max_back():
    """ Should create an individual with lower and upper bounds
    according to max_back attribute. """
    funset = tengp.FunctionSet()
    funset.add(np.add, 2)
    params = tengp.Parameters(2, 1, 1, 6, funset, max_back=3)

    factory = tengp.genotype_factory.GenotypeFactory(params)
    l_bounds, u_bounds = factory.get_bounds()
    genes = factory.get_random_genes()
    
    assert l_bounds == [0, 0, 0,
                        0, 0, 0,
                        0, 1, 1,
                        0, 2, 2,
                        0, 3, 3,
                        0, 4, 4,
                        5]

    assert u_bounds == [0, 1, 1,
                        0, 2, 2,
                        0, 3, 3,
                        0, 4, 4,
                        0, 5, 5,
                        0, 6, 6,
                        7]
