class Node():

    def __init__(self, fun, inputs, arity = 0):
        self.fun = fun
        self.inputs = inputs
        self.value = None
        self.arity = arity

    def __repr__(self):
        return f'{self.fun.__name__}, {self.inputs}'

def active_path(nodes):
    stack = []
    path = []

    # get all the output nodes
    index = len(nodes) - 1

    for node in reversed(nodes):
        if node.fun.__name__ == 'Variable':
            stack.append((index, node))
            index -= 1
        else: # output nodes should be only at the end of nodes list
            break

    while len(stack) > 0:
        index, current_node = stack.pop()

        path.append(index)

        for input_index in reversed(current_node.inputs):
            stack.append((input_index, nodes[input_index]))

    return reversed(path)



