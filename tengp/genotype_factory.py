from random import randint

class GenotypeFactory():

    def __init__(self, parameters):
        self.n_ins = parameters.n_inputs
        self.n_outs = parameters.n_outputs
        self.n_cols = parameters.n_columns
        self.n_rows = parameters.n_rows
        self.arity = parameters.function_set.max_arity 
        self.funset = parameters.function_set
        self.n_fun_nodes = self.n_cols * self.n_rows
        self.n_funs = len(self.funset)

    def create(self):
        genes = []
        bounds = []
        for i in range(self.n_ins, self.n_ins + self.n_fun_nodes):
            function_gene = randint(0, self.n_funs - 1)

            genes.append(function_gene)
            bounds.append(self.n_funs - 1)

            current_column = (i - self.n_ins) // self.n_rows

            upper_bound = self.n_ins + current_column * self.n_rows - 1

            for _ in range(self.arity):
                genes.append(randint(0, upper_bound))
                bounds.append(upper_bound)

        output_gene_upper_bound = self.n_ins + self.n_fun_nodes - 1
        for i in range(self.n_outs):
            genes.append(randint(0, output_gene_upper_bound))
            bounds.append(output_gene_upper_bound)

        return genes, bounds
