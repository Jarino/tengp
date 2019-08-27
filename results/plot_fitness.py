import sys
import json

import numpy as np
import matplotlib.pyplot as plt

def load(f):
    res = []
    with open(f, 'r') as fi:
        for line in fi:
            res.append(json.loads(line))

    max_length = max([len(x) for x in res])
    for x in res:    
        x += [x[-1]]*(max_length-len(x)) 
    return res

def plot_fitness(arr, name):
    plt.title(name)
    plt.plot(np.mean(arr, axis=0))
    plt.plot(np.min(arr, axis=0))
    plt.show()


def main(files):
    for f in files:
        plot_fitness(np.array(load(f)), f)




if __name__ == '__main__':
    main(sys.argv[1:])
