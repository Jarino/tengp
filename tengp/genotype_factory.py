from random import randint
from random import uniform

from .utils import clamp_bottom

class GenotypeFactory():

    def __init__(self, parameters):
        """
        Initialize a genotype factory.

        Parameters
        ----------
        parameters: Parameters object
            object holding info about individuals
        """
        self.n_ins = parameters.n_inputs
        self.n_outs = parameters.n_outputs
        self.n_cols = parameters.n_columns
        self.n_rows = parameters.n_rows
        self.max_back = parameters.max_back
        self.arity = parameters.function_set.max_arity
        self.funset = parameters.function_set
        self.n_fun_nodes = self.n_cols * self.n_rows
        self.n_funs = len(self.funset)
        self.constants = parameters.constants

    def create(self):
        """
        Create an individual primitives

        Returns
        -------
        tuple
            tuple holding list of genes and list of bounds
        """
        genes = []
        u_bounds = []
        l_bounds = []
        for i in range(self.n_ins, self.n_ins + self.n_fun_nodes):
            # upper and lower bound for function gene
            upper_bound = self.n_funs - 1
            lower_bound = 0
            function_gene = randint(0, upper_bound)

            genes.append(function_gene)
            u_bounds.append(upper_bound)
            l_bounds.append(lower_bound)

            current_column = (i - self.n_ins) // self.n_rows

            # upper and lower bound for input gene
            upper_bound = self.n_ins + current_column * self.n_rows - 1
            lower_bound = clamp_bottom(upper_bound - self.max_back + 1, 0)

            for _ in range(self.arity):
                u_bounds.append(upper_bound)
                l_bounds.append(lower_bound)
                genes.append(randint(lower_bound, upper_bound))

            if self.constants:
                l_bounds.append(0)
                u_bounds.append(self.constants)
                genes.append(1)

        output_gene_upper_bound = self.n_ins + self.n_fun_nodes - 1
        output_gene_lower_bound = clamp_bottom(
            output_gene_upper_bound - self.max_back + 1, 0
        )
        for i in range(self.n_outs):
            u_bounds.append(output_gene_upper_bound)
            l_bounds.append(output_gene_lower_bound)
            genes.append(randint(output_gene_lower_bound, output_gene_upper_bound))

        return genes, (l_bounds, u_bounds)
