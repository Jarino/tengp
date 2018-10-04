#import tensorflow as tf
from decorator import decorator

from .node import Node

class UnknownMutationException(Exception):
    pass

def map_to_np_phenotype(genes, params):
    nodes = []
    for _ in range(params.n_inputs):
        nodes.append(Node(None, [], is_input=True))

    chunk_size = params.function_set.max_arity + 1

    for i in range(params.n_nodes):
        node_genes = genes[i * chunk_size : (i * chunk_size) + chunk_size]

        function, arity = params.function_set[node_genes[0]]

        nodes.append(Node(function, node_genes[1:], arity))

    for gene in genes[-params.n_outputs:]:
        nodes.append(Node(None, [gene], is_output=True))

    return nodes


def active_paths(nodes):
    stack = []
    paths = []
    path = []

    # get all the output nodes
    index = len(nodes) - 1

    for node in reversed(nodes):
        if node.is_output:
            stack.append((index, node))
            index -= 1
        else: # output nodes should be only at the end of nodes list
            break

    while len(stack) > 0:
        index, current_node = stack.pop()

        not_first_output_node = len(path) != 0

        if current_node.is_output and not_first_output_node:
            paths.append(list(reversed(path)))
            path = []

        path.append(index)

        if not current_node.is_output and not current_node.is_input:
            inputs = current_node.inputs[:current_node.arity]
        else:
            inputs = current_node.inputs

        for input_index in reversed(inputs):
            stack.append((input_index, nodes[input_index]))

    if len(path) != 0:
        paths.append(list(reversed(path)))

    return paths


def join_lists(x, y):
    # this abhorent method is used in individual comparison, so the
    # reduce would run few ms faster
    return x + y


@decorator
def handle_invalid_decorator(fun, *args, **kwargs):
    """ Decorates the inner cost_function, so it returns fitness_of_invalid value
    defined in parameters in case of ValueError """
    new_args = list(args)
    cost_function = args[2]
    params = args[3]

    def wrapped_cost_function(*args, **kwargs):
        try:
            return cost_function(*args, **kwargs)
        except ValueError as e:
            return params.fitness_of_invalid

    new_args[2] = wrapped_cost_function
    return fun(*new_args, **kwargs)


def clamp_bottom(number, minimum):
    if number < minimum:
        return minimum
    return number

