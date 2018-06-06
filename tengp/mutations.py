from collections import deque
from random import choice, random

from .individual import Individual

class Move():
    """
    class holding a change 
    contains two lists:
        - list of affected indicies
        - list of values to apply
    """
    def __init__(self, indices, changes):
        self.indicies = indices
        self.changes = changes

    def __eq__(self, other):
        if self.indicies != other.indicies:
            return False
        if self.changes != other.changes:
            return False
        return True



def point_mutation(individual):
    """ 
    perform a point mutation on given individual 
    returns two lists:
        - list of indices to change
        - mutated values for given indices
    """
    # handle case, when there is only one possible value
    # of gene at certain position
    indices = [i for i, x in enumerate(individual.bounds) if x != 0]
    index = choice(indices)

    # construct the list of acceptable values
    possible_values = [x for x in range(
        0, individual.bounds[index] + 1) if x != individual.genes[index]]

    return Move([index], [choice(possible_values)])


def single_mutation(individual):
    """ perform a 'single' mutation - mutate until active gene is changed """

    active_changed = False
    genes = individual.genes[:]
    bounds = individual.bounds
    changed_indices = []

    while not active_changed:
        indices = [i for i, x in enumerate(bounds) if x != 0]

        index = choice(indices)

        changed_indices.append(index)

        possible_values = [x for x in range(0, bounds[index] + 1)
                           if x != genes[index]]

        genes[index] = choice(possible_values)

        if agenes[index] == 1:
            active_changed = True

    return Individual(genes, bounds, individual.params), changed_indices


#def active_mutation(individual, _=None):
#    """ Perform an active mutation - to-be mutated gene is chosen only
#    from active genes """
#
#    genes = individual.genes[:]
#    bounds = individual.bounds
#    agenes = individual.active_genes
#
#    # simultaneously handle genes with only one possible values
#    # and inactive genes
#    indices = [i for i, (b, a) in enumerate(
#        zip(bounds, agenes)) if b != 0 and a == 1]
#
#    index = choice(indices)
#
#    possible_values = [x for x in range(
#        0, bounds[index] + 1) if x != genes[index]]
#
#    genes[index] = choice(possible_values)
#
#    return Individual(genes, bounds, individual.params), index
#
#
#def probabilistic_mutation(individual, rate=0.25):
#    """ Perform a probabilistic mutation - at each gene position there is a
#    chance it will mutate """
#    
#    genes = individual.genes[:]
#    bounds = individual.bounds
#    changed_indices = []
#
#    for index in range(0, len(genes)):
#        chance = random()
#        if chance < rate:
#            possible_values = [x for x in range(0, bounds[index] + 1)
#                    if x != genes[index]]
#            if len(possible_values) == 0:
#                continue
#            changed_indices.append(index)
#            genes[index] = choice(possible_values)
#    return Individual(genes, bounds, individual.params), changed_indices
