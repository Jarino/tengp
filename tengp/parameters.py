from .individual import NPIndividual, TFIndividual

class Parameters():
    def __init__(self,
                 n_inputs,
                 n_outputs,
                 n_rows,
                 n_columns,
                 function_set,
                 fitness_of_invalid=float('inf'),
                 real_valued=False,
                 smoothing_fn=None,
                 use_tensorflow=False,
                 max_back=None):

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
        self.real_valued = real_valued
        if smoothing_fn:
            self.sfn = smoothing_fn
        else:
            self.sfn = lambda x: x

        if max_back is None:
            self.max_back = self.n_nodes + self.n_inputs + self.n_outputs
        else:
            self.max_back = max_back

class FunctionSet():
    def __init__(self):
        self.functions = []
        self.max_arity = 0

    def add(self, function, arity):
        self.functions.append((function, arity))
        self.max_arity = max(self.functions, key=lambda x: x[1])[1]

    def __getitem__(self, index):
        return self.functions[index]

    def __len__(self):
        return len(self.functions)

