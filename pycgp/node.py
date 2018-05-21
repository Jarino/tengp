class Node():

    def __init__(self, fun, inputs, arity = 0, is_input=False, is_output = False):
        self.fun = fun
        self.inputs = inputs
        self.value = None
        self.arity = arity
        self.is_output = is_output 
        self.is_input = is_input

    def __repr__(self):
        return f'{self.fun.__name__}, {self.inputs}'




