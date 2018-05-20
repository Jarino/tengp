import tensorflow as tf
import numpy as np

from node import Node  
from utils import map_to_phenotype, active_paths
from parameters import Parameters, FunctionSet
from genotype_factory import GenotypeFactory
from individual import Individual

X = [
    np.array([1, 2, 3], dtype=np.float32),
    np.array([4, 5, 6], dtype=np.float32), 
    np.array([7, 8, 9], dtype=np.float32)
]

nodes = []
genes = [0, 0, 1, 0, 0, 0, 1, 3, 2, 5, 4]

funset = FunctionSet()
funset.add(tf.add, 2)
funset.add(tf.multiply, 2)
funset.add(tf.sigmoid, 1)

params = Parameters(3, 2, 1, 3, funset)

g_factory = GenotypeFactory(params)

genes, bounds = g_factory.create()

individual = Individual(genes, bounds, params)

output = individual.transform(X)
print(output)
        

    

