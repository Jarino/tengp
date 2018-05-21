from time import time
import random

import tensorflow as tf
import numpy as np

from parameters import Parameters, FunctionSet
from search import evolution_strategy
from sklearn.metrics import mean_squared_error

X = [
    np.array([1, 2, 3], dtype=np.float32),
]

y = np.array([3, 6, 9])

tf_funset = FunctionSet()
tf_funset.add(tf.add, 2)
tf_funset.add(tf.multiply, 2)
tf_funset.add(tf.log, 1)

funset = FunctionSet()
funset.add(np.add, 2)
funset.add(np.multiply, 2)
funset.add(np.log, 1)

params = Parameters(1, 1, 1, 3, funset, use_tensorflow=False)

random.seed(0)
start = time()
result = evolution_strategy(X, y, mean_squared_error, params)

print(f'Numpy result: {result}, time: {time() - start}')

params = Parameters(1, 1, 1, 3, tf_funset, use_tensorflow=True)

random.seed(0)

start = time()
result = evolution_strategy(X, y, mean_squared_error, params)

print(f'Tensorflow result: {result}, time: {time() - start}')
