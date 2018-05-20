import tensorflow as tf
import numpy as np

from parameters import Parameters, FunctionSet
from search import evolution_strategy
from sklearn.metrics import mean_squared_error

X = [
    np.array([1, 2, 3], dtype=np.float32),
]

y = np.array([3, 6, 9])

funset = FunctionSet()

funset.add(tf.add, 2)
funset.add(tf.multiply, 2)
funset.add(tf.sigmoid, 1)

params = Parameters(1, 1, 1, 3, funset)

result = evolution_strategy(X, y, mean_squared_error, params)

print(result)

#ib = IndividualBuilder(params)
#
#individual = ib.create()
#
#output = individual.transform(X)
#
#print(output)
#        
#individual = point_mutation(individual)
#
#print(individual.transform(X))

    

