""" Module containing execution engine """
import math

from sympy import Symbol, lambdify

from .parameters import Parameters


class FixedFunctionRowEngine():
    def __init__(self, params: Parameters):
        self.params = params
        self.n_inputs = params.n_inputs
        self.arity = params.function_set.max_arity
        self.function_set = params.function_set


    # TODO
    # note, that this for now only works for only one input!
    # but since we dont have multiple outputs in the benchmark set
    # it is not currently important
    def execute(self, genotype, X):
        # genotype is a simple list of real values
        exec_stack = []
        exec_path = set()
        input_symbols = [Symbol(f'i{i}') for i in range(self.params.n_inputs)]
        expr_dict = {}

        # handle the output genes
        for gene in genotype[-self.params.n_outputs:]:
            lower = math.floor(gene)
            upper = math.ceil(gene)

            exec_stack.append(lower)
            exec_path.add(lower)

            if lower != upper:
                exec_stack.append(upper)
                exec_path.add(upper)

        while len(exec_stack) > 0:
            node_index = exec_stack.pop()

            if node_index < self.n_inputs:
                continue

            start_gene_index = (node_index - self.n_inputs)*self.arity
            node_genes = genotype[start_gene_index:start_gene_index+self.arity]

            for gene in reversed(node_genes):
                lower = math.floor(gene)
                upper = math.ceil(gene)
                
                if lower not in exec_path:
                    exec_stack.append(lower)
                    exec_path.add(lower)

                if lower != upper:
                    if upper not in exec_path:
                        exec_stack.append(upper)
                        exec_path.add(upper)


        for node_index in sorted(list(exec_path)):
            # input nodes
            if node_index < self.n_inputs:
                #expr_dict[node_index] = input_symbols[node_index]
                expr_dict[node_index] = X[:, node_index]
                continue

            # function nodes here
            start_gene_index = (node_index - self.n_inputs)*self.arity
            node_inputs = genotype[start_gene_index:start_gene_index+self.arity]
            # node function is determined by position in column
            node_function_index = (node_index - self.n_inputs)%len(self.function_set)
            node_function, function_arity = self.function_set[node_function_index]

            inputs = []
            for i in node_inputs[:function_arity]:
                coeff = i - int(i)
                L = (1-coeff)*expr_dict[math.floor(i)]
                R = coeff*expr_dict[math.ceil(i)]

                inputs.append(L + R)

            expr_dict[node_index] = node_function(*inputs)

        coeff = genotype[-1] - int(genotype[-1])
        L = (1-coeff)*expr_dict[math.floor(genotype[-1])]
        R = coeff*expr_dict[math.ceil(genotype[-1])]
        final_exp = L + R
        return final_exp
        #f = lambdify(*input_symbols, final_exp, "numpy")
        
        #return f(X)



