import math
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
        self.paths = active_paths(self.nodes, params.real_valued)
        self.active_nodes = set(reduce(join_lists, self.paths))
        self.params = params

    def __eq__(self, other):
        if len(self.active_nodes) != len(other.active_nodes):
            return False

        for me, them in zip(self.active_nodes, other.active_nodes):
            if self.nodes[me].fun != other.nodes[them].fun:
                return False

            if self.nodes[me].inputs != other.nodes[them].inputs:
                return False

        return True

    def __repr__(self):
        return f'Program, f:{self.fitness}'

    @abstractmethod
    def transform(self, X):
        pass

    def active_gene(self, gene_index):
        """ Checks, whether given index is index of a active gene """
        arity = self.params.function_set.max_arity
        if gene_index >= self.params.n_nodes*(arity + 1):
            return True
        node_id = (gene_index//(arity + 1))+self.params.n_inputs
        if node_id in self.active_nodes:
            return True
        return False

    def get_active_genes(self):
        """ Return all active genes. """
        active_genes = []
        arity = self.params.function_set.max_arity
        for node in self.active_nodes:
            if self.nodes[node].is_input:
                continue

            if self.nodes[node].is_output:
                gindex = self.params.n_nodes * arity + node - self.params.n_inputs
                active_genes.append(gindex)
                continue

            start_index = (arity+1)*(node-self.params.n_inputs)
            active_genes += range(start_index, start_index + arity + 1)
        return active_genes

    def get_expression(self):
        """ Return string representation of expression (phenotype)."""
        stack = []
        result = []

        for path in self.paths:
            for node in path:
                current_node = self.nodes[node]

                if current_node.is_output:
                    result.append(stack.pop())
                elif current_node.is_input:
                    stack.append(f'x{node}')
                else:
                    operands = reversed([stack.pop() for _ in range(0, current_node.arity)])
                    stack.append('{}({})'.format(current_node.fun.__name__, ','.join(operands)))

        return result


    def apply(self, move):
        """ Return new individual, as a result of applying given move to current individual."""
        genes = self.genes[:]

        for index, value in zip(move.indicies, move.changes):
            genes[index] = value

        return self.params.individual_class(genes, self.bounds, self.params)


class NPIndividual(Individual):
    def __init__(self, genes, bounds, params):
        self.nodes = map_to_np_phenotype(genes, params, params.real_valued)
        Individual.__init__(self, genes, bounds, params)

    def transform(self, X):
        funset = self.params.function_set
        for path in self.paths:
            for index in path:
                current_node = self.nodes[index]

                if current_node.is_input: # is input node 
                    current_node.value = X[:, index]
                elif current_node.is_output:
                    input_index = current_node.inputs[0]
                    current_node.value = self.nodes[input_index].value
                else:
                    if self.params.real_valued:
                        a = current_node.fun
                        fun_lower, _ = funset[math.floor(current_node.fun)]
                        fun_upper, _ = funset[math.ceil(current_node.fun)]
                        b = current_node.inputs[0]
                        c = current_node.inputs[1]

                        # actual indices
                        b_lower = math.floor(b)
                        b_upper = math.ceil(b)

                        # actual indices
                        c_lower = math.floor(c)
                        c_upper = math.ceil(b)
                        values = self.nodes
                        lower_function = (1-a)*( fun_lower((1-b) * values[b_lower].value, b*values[b_upper].value))

                        upper_function = a*( fun_upper((1-c) * values[c_lower].value, c * values[c_upper].value))

                        current_node.value = lower_function + upper_function
                        print('evaluation', values[b_lower].value, current_node.value)
                        pass
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


