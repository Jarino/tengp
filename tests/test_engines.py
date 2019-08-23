""" Test suite for engines """
from operator import add, sub
import tengp


import numpy as np

def test_real_valued_with_coeff_engine():
    """ Should execute fixed function row genotype and return its output """
    X = np.array([[1], [2], [3]])
    funset = tengp.FunctionSet()
    funset.add(add, 2)
    funset.add(sub, 2)
    
    params = tengp.Parameters(1, 1, len(funset), 2, funset)

    genotype = [3, 0, 0, 0,
                4, 1, 0, 0,
                5, 0, 1, 2,
                0, 0, 0, 0,
                3]

    engine = tengp.engines.RealValuedCoeffEngine(params)

    res = engine.execute(genotype, X)

    assert (res == [[30, 60, 90]]).all()

def test_execution_of_fixed_function_row_genotype():
    """ Should execute fixed function row genotype and return its output """
    X = np.array([[1], [2], [3]])
    funset = tengp.FunctionSet()
    funset.add(add, 2)
    funset.add(sub, 2)
    
    params = tengp.Parameters(1, 1, len(funset), 2, funset)

    genotype = [0, 0, 0, 0, 1, 2, 2, 2, 3]

    engine = tengp.engines.FixedFunctionRowEngine(params)

    res = engine.execute(genotype, X)

    assert (res == [[2, 4, 6]]).all()

def test_execution_of_fixed_function_row_genotype_with_real_number():
    """ Should execute fixed function row genotype and return its output """
    X = np.array([[1], [2], [3]])
    funset = tengp.FunctionSet()
    funset.add(add, 2)
    funset.add(sub, 2)
    
    params = tengp.Parameters(1, 1, len(funset), 2, funset)

    genotype = [0, 0, 0, 0, 1.5, 2, 2, 2, 3.5]

    engine = tengp.engines.FixedFunctionRowEngine(params)

    res = engine.execute(genotype, X)

    assert (res == [0.5, 1, 1.5]).all()



def test_execution_of_fixed_function_row_with_coeff_genotype():
    """ Should execute fixed function row genotype and return its output """
    X = np.array([[1], [2], [3]])
    funset = tengp.FunctionSet()
    funset.add(add, 2)
    funset.add(sub, 2)
    
    params = tengp.Parameters(1, 1, len(funset), 2, funset)

    genotype = [3, 0, 0, 1, 0, 0, 0.5, 1, 2, 2, 2, 2, 3]

    engine = tengp.engines.FFRCoeffEngine(params)

    res = engine.execute(genotype, X)

    assert (res == [[3, 6, 9]]).all()

