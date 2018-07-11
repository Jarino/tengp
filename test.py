import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

import tengp

# load data
X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# define function set
def pdivide(a, b):
    return np.divide(a, b, out=np.zeros_like(a), where=b!=0)

def plog(a):
    return np.log(a, out=np.zeros_like(a), where=a>0)

funset = tengp.FunctionSet()
funset.add(tf.add, 2)
funset.add(tf.multiply, 2)
#funset.add(pdivide, 2)
#funset.add(plog, 1)

# define cost function
def cost_function(y, y_pred):
    labels = np.array(y_pred).argmax(axis=0)
    return -accuracy_score(y, labels)

# tie everything together
params = tengp.Parameters(4, 3, n_columns=25, n_rows=1, function_set=funset, use_tensorflow=True)

res = tengp.evolution_strategy(X_train, y_train, cost_function, params, target_fitness=-1, random_state=42)

# evaluate the best individual
y_pred = res[0].transform(X_test)
labels = np.array(y_pred).argmax(axis=0)
print('Accuracy on test: {:.2}'.format(accuracy_score(y_test, labels)))
