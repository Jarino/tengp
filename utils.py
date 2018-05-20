import tensorflow as tf

from node import Node

def map_to_phenotype(genes, params):
    nodes = []
    for _ in range(params.n_inputs):
        nodes.append(Node(tf.constant, []))

    chunk_size = params.function_set.max_arity + 1

    for i in range(params.n_nodes):
        node_genes = genes[i * chunk_size : (i * chunk_size) + chunk_size]

        function, arity = params.function_set[node_genes[0]]

        nodes.append(Node(function, node_genes[1:], arity))

    for gene in genes[-params.n_outputs:]:
        nodes.append(Node(tf.Variable, [gene]))

    return nodes

def active_paths(nodes):
    stack = []
    paths = []
    path  = []

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

        not_first_output_node = len(path) != 0

        if current_node.fun.__name__ == 'Variable' and not_first_output_node:
           paths.append(list(reversed(path)))
           path = []

        path.append(index)

        for input_index in reversed(current_node.inputs):
            stack.append((input_index, nodes[input_index]))

    if len(path) != 0:
        paths.append(list(reversed(path)))

    return paths 


def join_lists(x, y):
    # this abhorent method is used in individual comparison, so the 
    # reduce would run few ms faster
    return x + y
