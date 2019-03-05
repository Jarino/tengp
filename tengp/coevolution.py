import numpy as np
import random
import copy

class Predictor():

    def __init__(self, values, length):
        self.fitness = None
        self.values = values
        self.length = length

    def __str__(self):
        return "Values array: {}\nLength: {}\nFitness: {}".format(self.values, self.length, self.fitness)

    def mutate(self, data_length, gene_mutation_probability=None):
        prob = gene_mutation_probability if gene_mutation_probability else 1 / len(self.values)
        for idx in range(len(self.values)):
            rnd = random.random()
            if rnd <= prob:
                while True:
                    new_value = random.randint(0, data_length - 1)
                    if new_value not in self.values:
                        self.values[idx] = new_value
                        break

    @staticmethod
    def generate_sample(data_size, sample_size):
        sample = random.sample(range(0, data_size), sample_size)
        return sample


class Population():

    def __init__(self):
        self.predictors = []

    def add(self, predictor):
        self.predictors.append(predictor)

    def create_initial_population(self, data_size, population_size, individual_size):
        for _ in range(population_size):
            sample = Predictor.generate_sample(data_size, individual_size)
            self.predictors.append(Predictor(sample, individual_size))

    def tournament_selection(self, amount_of_selected):
        if amount_of_selected > len(self.predictors):
            raise ValueError('Amount of selected exceeded population size')
        winners = []
        for _ in range(2):
            best_ind = None
            selected_idcs = random.sample(range(0, len(self.predictors)), amount_of_selected)
            for idx in selected_idcs:
                if (best_ind is None) or self.predictors[idx].fitness > best_ind.fitness:
                    best_ind = self.predictors[idx]
            winners.append(best_ind)
            # prevent duplicit selection
            # del self.predictors[best_ind_idx]
        return Population.one_point_crossover(copy.deepcopy(winners))

    @staticmethod
    def one_point_crossover(parents):
        if len(parents) != 2:
            raise ValueError('Parents list must be size 2')
        if parents[0].length != parents[1].length:
            raise ValueError('Parents are not the same length')
        pivot = random.randint(1, parents[0].length - 1)
        parents[0].values[0:pivot], parents[1].values[0:pivot] = parents[1].values[0:pivot], parents[0].values[0:pivot]
        return parents  # as children

# this should be later nested to class probably


def reproduction(population, selection_amount, data_size, individual_mutation_probability,
                 gene_mutation_probability=None):
    for pred in population.predictors:
        if pred.fitness is None:
            raise ValueError('All predictors must have fitness value assigned')
    population.predictors.sort(key=lambda x: x.fitness, reverse=True)
    # 30% of best individuals selected to new population
    new_population_size = len(population.predictors)
    new_population = Population()
    new_population.predictors = copy.deepcopy(population.predictors[0:(len(population.predictors) // 3)])
    # parent selection
    parents_children_amount = int(len(population.predictors) * 0.7)
    while len(new_population.predictors) < parents_children_amount:
        children = population.tournament_selection(selection_amount)
        for child in children:
            if random.random() <= individual_mutation_probability:
                child.mutate(data_size, gene_mutation_probability)
        new_population.predictors.extend(children)
    # rest of offspring will be generated randomly
    new_population.predictors.extend([Predictor(Predictor.generate_sample(data_size, new_population.predictors[0].length)
                                                ,new_population.predictors[0].length)
                                      for _ in range(new_population_size - len(new_population.predictors))])
    return new_population
