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
