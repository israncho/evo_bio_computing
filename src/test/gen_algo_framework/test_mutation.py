

from random import randint, sample
from src.gen_algo_framework.genetic_algorithm import population
from src.gen_algo_framework.mutation import swap_mutation, swap_mutation_population
from copy import deepcopy


def test_swap_mutation():
    for _ in range(500):
        individual = sample(range(200), randint(10, 20))
        individual_ = individual.copy()
        individual = swap_mutation(individual)
        assert individual != individual_


def test_swap_mutation_population():
    for _ in range(250):
        gene_set = set(sample(range(100), randint(5, 15)))
        _population = population(2000, gene_set)
        _population_copy = deepcopy(_population)

        options = {'mutation_proba': 0.1, 'another_swap_p': 0.1}
        _population = swap_mutation_population(_population, options)

        changed_count = 0
        for i in range(len(_population)):
            if _population[i] != _population_copy[i]:
                changed_count += 1

        assert 125 <= changed_count and changed_count <= 275

