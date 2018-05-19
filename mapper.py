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


