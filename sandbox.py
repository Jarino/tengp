import numpy as np

X = np.array([[3,4,5],[2,1,7], [1,1,1]])
x0 = X[0,:]
x1 = X[1,:]
x2 = X[2,:]

def fadd(x, y):
    return x + y

def fmul(x, y):
    return x * y

def fsub(x, y):
    return x - y

def pdivide(x, y):
    return np.divide(x, y, out=np.copy(x), where=x!=0)

def p(c):
    return np.sin(np.pi*c)

import tengp

from gpbenchmarks import get_data

X, y = get_data('nguyenf12', 6, -1, 1)
X = np.c_[np.ones(len(X)), X]

funset = tengp.FunctionSet()
funset.add(np.add, 2)
funset.add(np.multiply, 2)
funset.add(np.subtract, 2)
funset.add(pdivide, 2)

params = tengp.Parameters(3, 1, 1, 2, funset, real_valued=True)

bounds = tengp.individual.IndividualBuilder(params).create().bounds
bounds

individual = params.individual_class([3, 2, 2,
                                      3, 3, 3,
                                      4], bounds, params)

print(individual.active_nodes)


y_pred = individual.transform(X)

from sklearn.metrics import mean_squared_error

print('first node')
print(individual.nodes[3].value, mean_squared_error(individual.nodes[3].value, y))

print('second node')
print(individual.nodes[4].value, mean_squared_error(individual.nodes[4].value, y))

print('final output')
print([x[0] for x in list(y_pred)], mean_squared_error(y_pred, y))

