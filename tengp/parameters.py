from .individual import NPIndividual, TFIndividual

class Parameters():
    def __init__(self,
                 n_inputs,
                 n_outputs,
                 n_rows,
                 n_columns,
                 function_set,
                 fitness_of_invalid=float('inf'),
                 use_tensorflow=False):

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_nodes = n_rows * n_columns
        self.n_columns = n_columns
        self.n_rows = n_rows
        self.function_set = function_set
        self.fitness_of_invalid = fitness_of_invalid
        if use_tensorflow:
            self.individual_class = TFIndividual
        else:
            self.individual_class = NPIndividual

class FunctionSet():
    def __init__(self):
        self.functions = []

    def add(self, function, arity):
        self.functions.append((function, arity))

    def __getitem__(self, index):
        return self.functions[index]

    def __len__(self):
        return len(self.functions)
    
    @property
    def max_arity(self):
        return max(self.functions, key=lambda x: x[1])[1]
