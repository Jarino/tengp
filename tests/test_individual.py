""" Tests for individual abstract class and its derivatives """

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
