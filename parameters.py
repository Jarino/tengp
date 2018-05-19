class Parameters():
    def __init__(self, 
            n_inputs,
            n_outputs,
            n_rows,
            n_columns,
            function_set):

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_nodes = n_rows * n_columns
        self.function_set = function_set

class FunctionSet():
    def __init__(self):
        self.functions = []

    def add(self, function, arity):
        self.functions.append((function, arity))

    def __getitem__(self, index):
        return self.functions[index]
    
    @property
    def max_arity(self):
        return max(self.functions, key=lambda x: x[1])[1]
