""" Tests for utility functions """

from tengp.utils import round_cma_vector

def test_rounding_cma_vector():
    bounds = [1,2,2, 2,2,2, 3,2,2, 4]
    cma_vector = [1.90,-0.1,1.1, 1.9,0.3,1.3, 4.1,1,1.2,6]
    target_genes = [1,0,1, 2,0,1, 3,1,1, 4]

    converted_genes = round_cma_vector(cma_vector, bounds)

    assert target_genes == converted_genes
