

from random import randint, sample
from src.gen_algo_framework.population_utils import generate_population_of_bit_vectors, generate_population_of_permutations
from src.gen_algo_framework.mutation import bit_flip_mutation, bit_flip_mutation_population, swap_mutation, swap_mutation_population
from copy import deepcopy


def test_swap_mutation():
    for _ in range(500):
        individual = sample(range(200), randint(10, 20))
        individual_ = individual.copy()
        individual = swap_mutation(individual)
        assert individual != individual_


def test_swap_mutation_population():
    for _ in range(150):
        gene_set = set(sample(range(100), randint(5, 15)))
        _population = generate_population_of_permutations(2000, gene_set)
        _population_copy = deepcopy(_population)

        options = {'mutation_proba': 0.1}
        _population = swap_mutation_population(_population, options)

        changed_count = 0
        for i in range(len(_population)):
            if _population[i] != _population_copy[i]:
                changed_count += 1

        assert 150 <= changed_count and changed_count <= 250


def test_bit_flip_mutation():
    for _ in range(500):
        individual = [randint(0, 1) for _ in range(randint(20, 40))]
        individual_ = individual.copy()
        individual = bit_flip_mutation(individual)
        for e in individual:
            assert e in (0, 1)
        assert individual != individual_


def test_bit_flip_mutation_population():
    for _ in range(150):
        population = generate_population_of_bit_vectors(2000, [randint(5, 15)])
        population_copy = deepcopy(population)

        options = {'mutation_proba': 0.1}
        population = bit_flip_mutation_population(population, options)
        changed_count = 0
        for possibly_changed, unchanged in zip(population, population_copy):
            if possibly_changed != unchanged:
                changed_count += 1

        assert 150 <= changed_count and changed_count <= 250
