""" Module containing execution engine """
import math

from sympy import Symbol, lambdify

from .parameters import Parameters


class RealValuedCoeffEngine():
    def __init__(self, params: Parameters):
        self.params = params
        self.n_inputs = params.n_inputs
        self.arity = params.function_set.max_arity
        self.function_set = params.function_set

    def execute(self, genotype, X):
        # genotype is a simple list of real values
        exec_stack = []
        exec_path = set()
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

            start_gene_index = (node_index - self.n_inputs)*(self.arity+2)
            node_genes = genotype[start_gene_index:start_gene_index+(self.arity+2)]

            # exclude the function gene and coeff node
            for gene in reversed(node_genes[2:]):
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
                expr_dict[node_index] = X[:, node_index]
                continue

            # function nodes here
            start_gene_index = (node_index - self.n_inputs)*(self.arity+2)
            node_inputs = genotype[start_gene_index+2:start_gene_index+2+self.arity]

            inputs = []
            for i in node_inputs:#[:function_arity]:
                coeff = i - int(i)
                L = (1-coeff)*expr_dict[math.floor(i)]
                R = coeff*expr_dict[math.ceil(i)]

                inputs.append(L + R)

            node_coeff = genotype[start_gene_index]
            fun_gene = genotype[start_gene_index+1]
            fun_coeff = fun_gene - int(fun_gene)
            
            l_fun, _ = self.function_set[math.floor(fun_gene)]
            u_fun, _ = self.function_set[math.ceil(fun_gene)]

            expr_dict[node_index] = node_coeff * ((1-fun_coeff)*l_fun(*inputs) + fun_coeff*u_fun(*inputs))

        coeff = genotype[-1] - int(genotype[-1])
        L = (1-coeff)*expr_dict[math.floor(genotype[-1])]
        R = coeff*expr_dict[math.ceil(genotype[-1])]
        final_exp = L + R
        return final_exp


class RealValuedWeightEngine():
    def __init__(self, params: Parameters):
        self.params = params
        self.n_inputs = params.n_inputs
        self.arity = params.function_set.max_arity
        self.function_set = params.function_set

    def execute(self, genotype, X):
        # genotype is a simple list of real values
        exec_stack = []
        exec_path = set()
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

            start_gene_index = (node_index - self.n_inputs)*(self.arity+2)
            node_genes = genotype[start_gene_index:start_gene_index+(self.arity+2)]

            # exclude the function gene and coeff node
            for gene in reversed(node_genes[2:]):
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
                expr_dict[node_index] = X[:, node_index]
                continue

            # function nodes here
            start_gene_index = (node_index - self.n_inputs)*(self.arity+2)
            node_inputs = genotype[start_gene_index+2:start_gene_index+2+self.arity]

            inputs = []
            for i in node_inputs:#[:function_arity]:
                coeff = i - int(i)
                L = (1-coeff)*expr_dict[math.floor(i)]
                R = coeff*expr_dict[math.ceil(i)]

                inputs.append(L + R)

            node_coeff = genotype[start_gene_index]
            fun_gene = genotype[start_gene_index+1]
            fun_coeff = fun_gene - int(fun_gene)
            
            l_fun, _ = self.function_set[math.floor(fun_gene)]
            u_fun, _ = self.function_set[math.ceil(fun_gene)]

            expr_dict[node_index] = (1-node_coeff)*inputs[0] + node_coeff * ((1-fun_coeff)*l_fun(*inputs) + fun_coeff*u_fun(*inputs))

        coeff = genotype[-1] - int(genotype[-1])
        L = (1-coeff)*expr_dict[math.floor(genotype[-1])]
        R = coeff*expr_dict[math.ceil(genotype[-1])]
        final_exp = L + R
        return final_exp

class RealValuedEngine():
    def __init__(self, params: Parameters):
        self.params = params
        self.n_inputs = params.n_inputs
        self.arity = params.function_set.max_arity
        self.function_set = params.function_set

    def execute(self, genotype, X):
        # genotype is a simple list of real values
        exec_stack = []
        exec_path = set()
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

            start_gene_index = (node_index - self.n_inputs)*(self.arity+1)
            node_genes = genotype[start_gene_index:start_gene_index+(self.arity+1)]

            # exclude the function gene
            for gene in reversed(node_genes[1:]):
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
                expr_dict[node_index] = X[:, node_index]
                continue

            # function nodes here
            start_gene_index = (node_index - self.n_inputs)*(self.arity+1)
            node_inputs = genotype[start_gene_index+1:start_gene_index+1+self.arity]

            inputs = []
            for i in node_inputs:#[:function_arity]:
                coeff = i - int(i)
                L = (1-coeff)*expr_dict[math.floor(i)]
                R = coeff*expr_dict[math.ceil(i)]

                inputs.append(L + R)

            fun_gene = genotype[start_gene_index]
            fun_coeff = fun_gene - int(fun_gene)
            
            l_fun, _ = self.function_set[math.floor(fun_gene)]
            u_fun, _ = self.function_set[math.ceil(fun_gene)]

            expr_dict[node_index] = (1-fun_coeff)*l_fun(*inputs) + fun_coeff*u_fun(*inputs)

        coeff = genotype[-1] - int(genotype[-1])
        L = (1-coeff)*expr_dict[math.floor(genotype[-1])]
        R = coeff*expr_dict[math.ceil(genotype[-1])]
        final_exp = L + R
        return final_exp


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



class FFRCoeffEngine():
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

            start_gene_index = (node_index - self.n_inputs)*(1+self.arity)
            node_genes = genotype[start_gene_index:start_gene_index+1+self.arity]

            for gene in reversed(node_genes[1:]):
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
            start_gene_index = (node_index - self.n_inputs)*(self.arity+1)
            node_inputs = genotype[start_gene_index+1:start_gene_index+1+self.arity]
            # node function is determined by position in column
            node_function_index = (node_index - self.n_inputs)%len(self.function_set)
            node_function, function_arity = self.function_set[node_function_index]
            node_coeff = genotype[start_gene_index]

            inputs = []
            for i in node_inputs[:function_arity]:
                coeff = i - int(i)
                L = (1-coeff)*expr_dict[math.floor(i)]
                R = coeff*expr_dict[math.ceil(i)]

                inputs.append(L + R)

            expr_dict[node_index] = node_coeff*node_function(*inputs)

        coeff = genotype[-1] - int(genotype[-1])
        L = (1-coeff)*expr_dict[math.floor(genotype[-1])]
        R = coeff*expr_dict[math.ceil(genotype[-1])]
        final_exp = L + R
        return final_exp

class FFRWeightEngine():
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

            start_gene_index = (node_index - self.n_inputs)*(1+self.arity)
            node_genes = genotype[start_gene_index:start_gene_index+1+self.arity]

            for gene in reversed(node_genes[1:]):
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
            start_gene_index = (node_index - self.n_inputs)*(self.arity+1)
            node_inputs = genotype[start_gene_index+1:start_gene_index+1+self.arity]
            # node function is determined by position in column
            node_function_index = (node_index - self.n_inputs)%len(self.function_set)
            node_function, function_arity = self.function_set[node_function_index]
            node_coeff = genotype[start_gene_index]

            inputs = []
            for i in node_inputs[:function_arity]:
                coeff = i - int(i)
                L = (1-coeff)*expr_dict[math.floor(i)]
                R = coeff*expr_dict[math.ceil(i)]

                inputs.append(L + R)

            expr_dict[node_index] = (1-node_coeff)*inputs[0] + node_coeff*node_function(*inputs)

        coeff = genotype[-1] - int(genotype[-1])
        L = (1-coeff)*expr_dict[math.floor(genotype[-1])]
        R = coeff*expr_dict[math.ceil(genotype[-1])]
        final_exp = L + R
        return final_exp
