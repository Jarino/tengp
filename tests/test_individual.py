""" Tests for individual abstract class and its derivatives """
import numpy as np
import pytest

def test_active_gene_check(individual):
    """ Should return true/false value depending on whether the
    gene is active or not."""
    gene_index = 3
    assert not individual.active_gene(gene_index)
    gene_index = 4
    assert not individual.active_gene(gene_index)
    gene_index = 5
    assert not individual.active_gene(gene_index)
    gene_index = 2
    assert individual.active_gene(gene_index)
    gene_index = 6
    assert individual.active_gene(gene_index)
    gene_index = 9
    assert individual.active_gene(gene_index)

def test_get_active_genes(individual):
    """ Should return indicies of all active genes of given individual """
    active_genes = individual.get_active_genes()

    assert  active_genes == [0, 1, 2, 6, 7, 8, 9]

def test_get_active_genes_multi(individual_multi):
    """ Should return indicies of all active genes of given individual with multiple
    inputs and outputs"""
    active_genes = individual_multi.get_active_genes()

    assert  active_genes == [3, 4, 5, 9, 10]

def test_str_of_individual(individual):
    """ Should return a phenotype (function expression) as string. """
    expression = individual.get_expression()

    assert expression == ['add(add(x0,x0),x0)']

def test_str_of_multi_individual(individual_multi):
    """ Should return a phenotype (function expression) as string. """
    expression = individual_multi.get_expression()
    assert expression == ['add(x1,x0)', 'add(x1,x0)']

def test_arity_one_inactivity(individual_sin):
    """ If there is arity of node lesser than max arity, unused inputs should
    not be considered active. """
    active_nodes = [i for i, n in enumerate(individual_sin.nodes) if not n.is_input and i in individual_sin.active_nodes]

    assert active_nodes == [3, 4, 5]


def test_single_feature_data(individual_multiply):
    """ Should return transform each sample individually."""
    X = np.array([[1], [2], [3], [4]])
    y = np.array([[2], [8], [18], [32]])

    y_pred = individual_multiply.transform(X)

    assert (y == y_pred).all()


def test_single_sample_data(individual_multi):
    """ Should return transform each sample individually."""
    X = np.array([[1, 4]])
    y = np.array([[5]])

    y_pred = individual_multi.transform(X)

    assert (y == y_pred).all()

    X = np.array([[1, 4], [3,7]])
    y = np.array([[5], [10]])

    y_pred = individual_multi.transform(X)

    assert (y == y_pred).all()
    

def test_1d_input_into_transform(individual_multiply):
    X = np.array([1, 2, 3, 4])
    
    try:
        y_pred = individual_multiply.transform(X)
        assert False, "should throw error about dimensions"
    except ValueError:
        assert True, "should throw error about dimensions"



