from random import randint

import numpy as np

from .utils import clamp_bottom

class FixedFunctionRowGenotypeFactory():
    
    def __init__(self, parameters):
        self.n_ins = parameters.n_inputs
        self.n_outs = parameters.n_outputs
        self.n_cols = parameters.n_columns
        self.n_rows = len(parameters.function_set)
        self.n_fun_nodes = self.n_cols * self.n_rows
        self.arity = parameters.function_set.max_arity
        self.max_back = parameters.max_back

        self.l_bounds = None
        self.u_bounds = None

        self._compute_bounds()

    def _compute_bounds(self):
        """
        Compute the lower and upper bounds
        """
        self.l_bounds = []
        self.u_bounds = []
        for i in range(self.n_cols):
            # first column is a special case
            if i == 0:
                self.l_bounds += [0]*self.n_rows*self.arity 
                self.u_bounds += [self.n_ins - 1]*self.n_rows*self.arity
                continue
            
            self.l_bounds += [self.n_ins + (i - self.max_back) * self.n_rows]*self.n_rows*self.arity
            self.u_bounds += [self.n_ins - 1 + i*self.n_rows]*self.n_rows*self.arity

        # then add them output genes
        i += 1
        self.l_bounds += [self.n_ins + (i - self.max_back) * self.n_rows]*self.n_outs
        self.u_bounds += [self.n_ins - 1 + i*self.n_rows]*self.n_outs

        self.l_bounds = [0 if x < 0 else x for x in self.l_bounds]

    def get_random_genes(self):
    # (np.random.rand(10) * (u-l)) + l
        u = np.array(self.u_bounds)
        l = np.array(self.l_bounds)
        return (np.random.rand(len(u)) * (u-l)) + l


class FFRCoeffGenotypeFactory():
    """ Fixed function row with coefficients """
    
    def __init__(self, parameters, coeff_min: int, coeff_max: int):
        self.n_ins = parameters.n_inputs
        self.n_outs = parameters.n_outputs
        self.n_cols = parameters.n_columns
        self.n_rows = len(parameters.function_set)
        self.n_fun_nodes = self.n_cols * self.n_rows
        self.arity = parameters.function_set.max_arity
        self.max_back = parameters.max_back
        self.c_min = coeff_min
        self.c_max = coeff_max

        self.l_bounds = None
        self.u_bounds = None

        self._compute_bounds()

    def _compute_bounds(self):
        """
        Compute the lower and upper bounds
        """
        self.l_bounds = []
        self.u_bounds = []
        for i in range(self.n_cols):
            # first column is a special case
            if i == 0:
                for _ in range(self.n_rows):
                    self.l_bounds += [self.c_min] + [0]*self.arity 
                    self.u_bounds += [self.c_max] + [self.n_ins - 1]*self.arity
                continue
            
            for _ in range(self.n_rows):
                self.l_bounds += [self.c_min] + [self.n_ins + (i - self.max_back) * self.n_rows]*self.arity
                self.u_bounds += [self.c_max] + [self.n_ins - 1 + i*self.n_rows]*self.arity

        # then add them output genes
        i += 1
        self.l_bounds += [self.n_ins + (i - self.max_back) * self.n_rows]*self.n_outs
        self.u_bounds += [self.n_ins - 1 + i*self.n_rows]*self.n_outs

        self.l_bounds = [0 if x < 0 else x for x in self.l_bounds]

    def get_random_genes(self):
    # (np.random.rand(10) * (u-l)) + l
        u = np.array(self.u_bounds)
        l = np.array(self.l_bounds)
        return (np.random.rand(len(u)) * (u-l)) + l


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
        self.l_bounds = None
        self.u_bounds = None

        self._compute_bounds()

    def _compute_bounds(self):
        """
        Create an individual primitives

        Returns
        -------
        tuple
            tuple holding list of genes and list of bounds
        """
        u_bounds = []
        l_bounds = []
        for i in range(self.n_ins, self.n_ins + self.n_fun_nodes):
            # upper and lower bound for function gene
            upper_bound = self.n_funs - 1
            lower_bound = 0

            u_bounds.append(upper_bound)
            l_bounds.append(lower_bound)

            current_column = (i - self.n_ins) // self.n_rows

            # upper and lower bound for input gene
            upper_bound = self.n_ins + current_column * self.n_rows - 1
            lower_bound = clamp_bottom(upper_bound - (self.max_back*self.n_rows) + 1, 0)

            for _ in range(self.arity):
                u_bounds.append(upper_bound)
                l_bounds.append(lower_bound)

        output_gene_upper_bound = self.n_ins + self.n_fun_nodes - 1
        output_gene_lower_bound = clamp_bottom(
            output_gene_upper_bound - self.max_back + 1, 0
        )
        for i in range(self.n_outs):
            u_bounds.append(output_gene_upper_bound)
            l_bounds.append(output_gene_lower_bound)

        self.l_bounds = l_bounds
        self.u_bounds = u_bounds

    def get_bounds(self):
        return self.l_bounds, self.u_bounds

    def get_random_genes(self):
        """
        Create an individual primitives

        Returns
        -------
        tuple
            tuple holding list of genes and list of bounds
        """
        genes = []
        for i in range(self.n_ins, self.n_ins + self.n_fun_nodes):
            # upper and lower bound for function gene
            upper_bound = self.n_funs - 1
            lower_bound = 0
            function_gene = randint(0, upper_bound)

            genes.append(function_gene)

            current_column = (i - self.n_ins) // self.n_rows

            # upper and lower bound for input gene
            upper_bound = self.n_ins + current_column * self.n_rows - 1
            lower_bound = clamp_bottom(upper_bound - (self.max_back*self.n_rows) + 1, 0)

            for _ in range(self.arity):
                genes.append(randint(lower_bound, upper_bound))

        output_gene_upper_bound = self.n_ins + self.n_fun_nodes - 1
        output_gene_lower_bound = clamp_bottom(
            output_gene_upper_bound - self.max_back + 1, 0
        )
        for i in range(self.n_outs):
            genes.append(randint(output_gene_lower_bound, output_gene_upper_bound))

        return genes



class CoeffGenotypeFactory():

    def __init__(self, parameters, c_min, c_max):
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
        self.l_bounds = None
        self.u_bounds = None
        self.c_min = c_min
        self.c_max = c_max

        self._compute_bounds()

    def _compute_bounds(self):
        """
        Create an individual primitives

        Returns
        -------
        tuple
            tuple holding list of genes and list of bounds
        """
        u_bounds = []
        l_bounds = []
        for i in range(self.n_ins, self.n_ins + self.n_fun_nodes):
            # upper and lower bound for coeff gene
            u_bounds.append(self.c_max)
            l_bounds.append(self.c_min)


            # upper and lower bound for function gene
            upper_bound = self.n_funs - 1
            lower_bound = 0

            
            u_bounds.append(upper_bound)
            l_bounds.append(lower_bound)

            current_column = (i - self.n_ins) // self.n_rows


            # upper and lower bound for input gene
            upper_bound = self.n_ins + current_column * self.n_rows - 1
            lower_bound = clamp_bottom(upper_bound - (self.max_back*self.n_rows) + 1, 0)

            for _ in range(self.arity):
                u_bounds.append(upper_bound)
                l_bounds.append(lower_bound)

        output_gene_upper_bound = self.n_ins + self.n_fun_nodes - 1
        output_gene_lower_bound = clamp_bottom(
            output_gene_upper_bound - self.max_back + 1, 0
        )
        for i in range(self.n_outs):
            u_bounds.append(output_gene_upper_bound)
            l_bounds.append(output_gene_lower_bound)

        self.l_bounds = l_bounds
        self.u_bounds = u_bounds

    def get_bounds(self):
        return self.l_bounds, self.u_bounds

    def get_random_genes(self):
        """
        Create an individual primitives

        Returns
        -------
        tuple
            tuple holding list of genes and list of bounds
        """
        genes = []
        for i in range(self.n_ins, self.n_ins + self.n_fun_nodes):
            # upper and lower bound for function gene
            upper_bound = self.n_funs - 1
            lower_bound = 0
            function_gene = randint(0, upper_bound)

            genes.append(function_gene)

            current_column = (i - self.n_ins) // self.n_rows

            # upper and lower bound for input gene
            upper_bound = self.n_ins + current_column * self.n_rows - 1
            lower_bound = clamp_bottom(upper_bound - (self.max_back*self.n_rows) + 1, 0)

            for _ in range(self.arity):
                genes.append(randint(lower_bound, upper_bound))

        output_gene_upper_bound = self.n_ins + self.n_fun_nodes - 1
        output_gene_lower_bound = clamp_bottom(
            output_gene_upper_bound - self.max_back + 1, 0
        )
        for i in range(self.n_outs):
            genes.append(randint(output_gene_lower_bound, output_gene_upper_bound))

        return genes
