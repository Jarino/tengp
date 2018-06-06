import random

import numpy as np
import tengp

funset = tengp.FunctionSet()

funset.add(np.add, 2)
funset.add(np.multiply, 2)
funset.add(np.subtract, 2)

params = tengp.Parameters(
        16,1,
        n_rows=1,
        n_columns=20,
        function_set=funset,
        use_tensorflow=False)


ib = tengp.individual.IndividualBuilder(params)


individual = ib.create() 

from collections import deque

memory = deque(maxlen=50)
same = 0

for i in range(5001):
    move = tengp.mutations.point_mutation(individual)

    for old_move in memory:
        if move == old_move:
            same += 1

    memory.append(move)

    individual = individual.apply(move)

print(f'hotovo, rovnakych pohybov bolo: {same}')







