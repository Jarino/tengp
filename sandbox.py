import tensorflow as tf

import numpy as np

from node import Node, active_path 
from mapper import map_to_phenotype
from parameters import Parameters, FunctionSet

X = [
    np.array([1, 2, 3], dtype=np.float32),
    np.array([4, 5, 6], dtype=np.float32), 
    np.array([7, 8, 9], dtype=np.float32)
]

nodes = []
genes = [0, 0, 1, 0, 0, 0, 1, 3, 2, 5, 4]

funset = FunctionSet()
funset.add(tf.add, 2)
funset.add(tf.sigmoid, 1)

params = Parameters(3, 2, 1, 3, funset)

nodes = map_to_phenotype(genes, params)

paths = active_path(nodes)

for path in active_path(nodes):
    for index in path:
        current_node = nodes[index]
        
        if current_node.fun.__name__ == 'constant': # quite shitty way to check
            current_node.value = current_node.fun(X[index])
        elif current_node.fun.__name__ == 'Variable':
            input_index = current_node.inputs[0]
            initial_value = nodes[input_index].value 
            current_node.value = current_node.fun(initial_value)
        else:
            values = [nodes[i].value for i in current_node.inputs[:current_node.arity]]
            current_node.value = current_node.fun(*values)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(1, params.n_outputs + 1):
        print(nodes[-i].value.eval())
        

    

