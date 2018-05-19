import tensorflow as tf

import numpy as np

from node import Node, active_path 

X = [
        np.array([1, 2, 3], dtype=np.float32),
        np.array([4, 5, 6], dtype=np.float32), 
        np.array([7, 8, 9], dtype=np.float32)
]

nodes = []

nodes.append(Node(tf.constant, []))
nodes.append(Node(tf.constant, []))
nodes.append(Node(tf.constant, []))
nodes.append(Node(tf.add, [0, 1], 2))
nodes.append(Node(tf.add, [0, 0], 2)) 
nodes.append(Node(tf.sigmoid, [3, 2], 1))
nodes.append(Node(tf.Variable, [5]))

stack = []

for index in active_path(nodes):
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
    output = nodes[-1].value.eval()
    print(output)
        

    

