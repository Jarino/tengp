import tensorflow as tf

from utils import map_to_phenotype, active_paths

class Individual():

    def __init__(self, genes, bounds, params):
        self.nodes = map_to_phenotype(genes, params)

        self.paths = active_paths(self.nodes)

        self.params = params

    def transform(self, X):
        for path in self.paths:
            for index in path:
                current_node = self.nodes[index]
                
                if current_node.fun.__name__ == 'constant': # quite shitty way to check
                    current_node.value = current_node.fun(X[index])
                elif current_node.fun.__name__ == 'Variable':
                    input_index = current_node.inputs[0]
                    initial_value = self.nodes[input_index].value 
                    current_node.value = current_node.fun(initial_value)
                else:
                    values = [self.nodes[i].value for i in current_node.inputs[:current_node.arity]]
                    current_node.value = current_node.fun(*values)


        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            output = []
            for i in range(1, self.params.n_outputs + 1):
                output.append(self.nodes[-i].value.eval())

        return output
