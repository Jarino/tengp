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


def test_fixed_function_row_genotype_factory():
    """ Should create an individual, only with input genes """
    funset = tengp.FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.division, 2)
    params = tengp.Parameters(2, 2, len(funset), 2, funset, max_back=1)

    factory = tengp.genotype_factory.FixedFunctionRowGenotypeFactory(params)
    l_bounds = [0]*6 + [2]*6 + [5]*2
    u_bounds = [1]*6 + [4]*6 + [7]*2 
    
    assert factory.l_bounds == l_bounds
    assert factory.u_bounds == u_bounds


def test_fixed_function_row_genotype_factory_w_max_back():
    """ Should create an individual, only with input genes respecting
    the max_back parameter. """
    funset = tengp.FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.division, 2)
    params = tengp.Parameters(2, 2, len(funset), 2, funset, max_back=2)

    factory = tengp.genotype_factory.FixedFunctionRowGenotypeFactory(params)
    l_bounds = [0]*6 + [0]*6 + [2]*2
    u_bounds = [1]*6 + [4]*6 + [7]*2 
    
    assert factory.l_bounds == l_bounds
    assert factory.u_bounds == u_bounds

def test_fixed_function_row_genotype_factory_w_max_back_and_coefficients():
    """ Should create an individual, only with input genes respecting
    the max_back parameter. """
    funset = tengp.FunctionSet()
    funset.add(np.add, 2)
    funset.add(np.subtract, 2)
    funset.add(np.division, 2)
    params = tengp.Parameters(2, 2, len(funset), 2, funset, max_back=2)

    factory = tengp.FFRCoeffGenotypeFactory(params, 0, 10)
    l_bounds = [0, 0, 0]*3 + [0, 0, 0]*3 + [2]*2
    u_bounds = [10,1, 1]*3 + [10,4, 4]*3 + [7]*2 
    
    assert factory.l_bounds == l_bounds
    assert factory.u_bounds == u_bounds

