"""
Various helper stuff for results interpretation
"""
import sys
import json

import numpy as np

def load(f):
    res = []
    with open(f, 'r') as fi:
        for line in fi:
            res.append(json.loads(line))

    max_length = max([len(x) for x in res])
    for x in res:    
        x += [x[-1]]*(max_length-len(x)) 
    return res

def stats(d):
    print(f'min: {np.min(d):.3e}')
    print(f'mean: {np.mean(np.min(d, axis=1)):.3e}')
    print(f'median: {np.median(np.min(d, axis=1)):.3e}')
    print(f'std: {np.std(np.min(d, axis=1)):.3e}')
    print(f'{np.min(d):.3e} | {np.mean(np.min(d, axis=1)):.3e} | {np.median(np.min(d, axis=1)):.3e} | {np.std(np.min(d, axis=1)):.3e}|')


def main(files):
    for f in files:
        print()
        print(f)
        stats(load(f))


if __name__ == '__main__':
    main(sys.argv[1:])
    


