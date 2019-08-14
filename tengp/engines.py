""" Module containing execution engine """
from .parameters import Parameters
from sympy import Symbol, lambdify


# TODO
# note, that this for now only works for only one input!
# but since we dont have multiple outputs in the benchmark set
# it is not currently important
class FixedFunctionRowEngine():
    def __init__(self, params: Parameters):
        self.params = params
        self.n_inputs = params.n_inputs
        self.arity = params.function_set.max_arity
        self.function_set = params.function_set


    def execute(self, genotype, X):
        # genotype is a simple list of real values
        exec_stack = []
        exec_path = set()
        input_symbols = [Symbol(f'i{i}') for i in range(self.params.n_inputs)]
        expr_dict = {}

        # handle the output genes
        for gene in genotype[-self.params.n_outputs:]:
            exec_stack.append(gene)
            exec_path.add(gene)

        while len(exec_stack) > 0:
            node_index = exec_stack.pop()

            start_gene_index = (node_index - self.n_inputs)*self.arity
            node_genes = genotype[start_gene_index:start_gene_index+self.arity]

            for gene in reversed(node_genes):
                exec_stack.append(gene)
                exec_path.add(gene)

        for node_index in sorted(list(exec_path)):
            # input nodes
            if node_index < self.n_inputs:
                expr_dict[node_index] = input_symbols[node_index]
                continue

            # function nodes here
            start_gene_index = (node_index - self.n_inputs)*self.arity
            node_inputs = genotype[start_gene_index:start_gene_index+self.arity]
            # node function is determined by position in column
            node_function_index = (node_index - self.n_inputs)%len(self.function_set)
            node_function, function_arity = self.function_set[node_function_index]

            inputs = []
            for i in node_inputs[:function_arity]:
                inputs.append(expr_dict[i])

            expr_dict[node_index] = node_function(*inputs)

        final_exp = expr_dict[genotype[-1]]
        f = lambdify(*input_symbols, final_exp, "numpy")
        
        return f(X)



