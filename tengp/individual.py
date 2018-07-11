from abc import ABC, abstractmethod
from functools import reduce

#import tensorflow as tf
import numpy as np

from .genotype_factory import GenotypeFactory
from .utils import map_to_tf_phenotype, map_to_np_phenotype, active_paths, join_lists

class Individual(ABC):

    def __init__(self, genes, bounds, params):
        self.fitness = None
        self.genes = genes
        self.bounds = bounds
        self.paths = active_paths(self.nodes)
        self.active_nodes = set(reduce(join_lists, self.paths))
        self.params = params

    @abstractmethod
    def transform(self, X):
        pass

    def __eq__(self, other):
        for me, them in zip(self.active_nodes, other.active_nodes):
            if self.nodes[me].fun != other.nodes[them].fun:
                return False
            
            if self.nodes[me].inputs != other.nodes[them].inputs:
                return False

        return True

    def __repr__(self):
        return f'Program, f:{self.fitness}'

    def apply(self, move):
        genes = self.genes[:]

        for index, value in zip(move.indicies, move.changes):
            genes[index] = value

        return self.params.individual_class(genes, self.bounds, self.params)


class NPIndividual(Individual):

    def __init__(self, genes, bounds, params):
        self.nodes = map_to_np_phenotype(genes, params)
        Individual.__init__(self, genes, bounds, params)

    def transform(self, X):
        for path in self.paths:
            for index in path:
                current_node = self.nodes[index]

                if current_node.is_input: # is input node 
                    current_node.value = X[:, index]
                elif current_node.is_output:
                    input_index = current_node.inputs[0]
                    current_node.value = self.nodes[input_index].value
                else:
                    values = [self.nodes[i].value for i in current_node.inputs[:current_node.arity]]
                    current_node.value = current_node.fun(*values)

        output = []
        for i in range(1, self.params.n_outputs + 1):
            output.append(self.nodes[-i].value)

        return np.array(output).T

class TFIndividual(Individual):

    def __init__(self, genes, bounds, params):
        self.nodes = map_to_tf_phenotype(genes, params)
        Individual.__init__(self, genes, bounds, params)

    def transform(self, X):
        for path in self.paths:
            for index in path:
                current_node = self.nodes[index]
                
                if current_node.fun.__name__ == 'constant': # quite shitty way to check
                    current_node.value = current_node.fun(X[:, index])
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


class IndividualBuilder():
    def __init__(self, params):
        self.params = params
        self.g_factory = GenotypeFactory(params)

    def create(self):
        genes, bounds = self.g_factory.create()

        return self.params.individual_class(genes, bounds, self.params)


