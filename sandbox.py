import tensorflow as tf
import numpy as np

from parameters import Parameters, FunctionSet
from individual import IndividualBuilder, Individual

X = [
    np.array([1, 2, 3], dtype=np.float32),
    np.array([4, 5, 6], dtype=np.float32), 
    np.array([7, 8, 9], dtype=np.float32)
]

funset = FunctionSet()

funset.add(tf.add, 2)
funset.add(tf.multiply, 2)
funset.add(tf.sigmoid, 1)

params = Parameters(3, 2, 1, 3, funset)

ib = IndividualBuilder(params)

individual = ib.create()

output = individual.transform(X)

print(output)
        

    

