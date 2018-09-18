#import tensorflow as tf
import math

from .node import Node, RealValuedNode

class UnknownMutationException(Exception):
    pass

def map_to_np_phenotype(genes, params, real_valued=False):

    nodes = []
    for _ in range(params.n_inputs):
        nodes.append(Node(None, [], is_input=True))

    chunk_size = params.function_set.max_arity + 1

    if real_valued and params.constants:
        chunk_size += 1

    for i in range(params.n_nodes):
        node_genes = genes[i * chunk_size : (i * chunk_size) + chunk_size]


        if real_valued:
            new_node = RealValuedNode(node_genes[0], node_genes[1:1+params.function_set.max_arity], 2)
            if params.constants:
                new_node.constant = node_genes[-1]
            nodes.append(new_node)
        else:
            function, arity = params.function_set[node_genes[0]]
            nodes.append(Node(function, node_genes[1:], arity))

    for gene in genes[-params.n_outputs:]:
        nodes.append(Node(None, [gene], is_output=True))

    return nodes

def map_to_tf_phenotype(genes, params):
    nodes = []
    for _ in range(params.n_inputs):
        nodes.append(Node(tf.constant, [], is_input=True))

    chunk_size = params.function_set.max_arity + 1


    for i in range(params.n_nodes):
        node_genes = genes[i * chunk_size : (i * chunk_size) + chunk_size]

        function, arity = params.function_set[node_genes[0]]

        nodes.append(Node(function, node_genes[1:1+params.function_set.max_arity], arity))


    for gene in genes[-params.n_outputs:]:
        nodes.append(Node(tf.Variable, [gene], is_output=True))

    return nodes

def active_paths(nodes, real_valued=False):
    stack = []
    paths = []
    path = []

    # get all the output nodes
    index = len(nodes) - 1

    for node in reversed(nodes):
        if node.is_output:
            stack.append((index, node))
            node.visited = True
            index -= 1
        else: # output nodes should be only at the end of nodes list
            break

    while len(stack) > 0:
        index, current_node = stack.pop()
        current_node.visited = True

        not_first_output_node = len(path) != 0

        if current_node.is_output and not_first_output_node:
            paths.append(list(reversed(path)))
            path = []

        path.append(index)

        if not current_node.is_output and not current_node.is_input:
            if real_valued:
                nested = [[math.floor(i), math.ceil(i)] for i in current_node.inputs[:current_node.arity]]
                inputs = [x for y in nested for x in y]
            else:
                inputs = current_node.inputs[:current_node.arity]
        else:
            inputs = current_node.inputs

        inputs_to_stack = []
        for input_index in reversed(inputs):
            if real_valued:
                lower = math.floor(input_index)
                upper = math.ceil(input_index)

                inputs_to_stack.append(lower)
                inputs_to_stack.append(upper)
            else:
                inputs_to_stack.append(input_index)

        stack_keys = [x for x, y in stack]
        for index in set(inputs_to_stack):
            if nodes[index].visited:
               continue
            stack.append((index, nodes[index]))

    if len(path) != 0:
        paths.append(list(reversed(path)))

    return paths


def join_lists(x, y):
    # this abhorent method is used in individual comparison, so the
    # reduce would run few ms faster
    return x + y

def round_cma_vector(cma_vector, bounds):
    """ convert float vector from CMA-ES to valid genes vector """
    processed_genes = []
    for number, bound in zip(cma_vector, bounds):
        gene = int(round(number))
        if gene > bound:
            gene = bound
        if gene < 0:
            gene = 0
        processed_genes.append(gene)
    return processed_genes

def handle_invalid_decorator(fun):
    """ Decorates the inner cost_function, so it returns fitness_of_invalid value
    defined in parameters in case of ValueError """
    def wrapper(*args, **kwargs):
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
    return wrapper

def clamp_bottom(number, minimum):
    if number < minimum:
        return minimum
    return number

