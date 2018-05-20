class Node():

    def __init__(self, fun, inputs, arity = 0):
        self.fun = fun
        self.inputs = inputs
        self.value = None
        self.arity = arity

    def __repr__(self):
        return f'{self.fun.__name__}, {self.inputs}'




