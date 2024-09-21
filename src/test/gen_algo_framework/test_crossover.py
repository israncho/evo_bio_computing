from typing import Set, Tuple, List
from src.gen_algo_framework.crossover import parents_crossover_ox1, pop_crossover_ox1_roulettew_s
from src.gen_algo_framework.genetic_algorithm import generate_population
from src.gen_algo_framework.selection import cumulative_fitness
from random import randint, sample


def different_random_parents(size: int, range_gene_size: int) -> Tuple[Set[int], List[int], List[int]]:
    genes = sample(range(range_gene_size), size)
    parent1 = []
    parent2 = []
    while parent1 == parent2:
        parent1 = sample(genes, size)
        parent2 = sample(genes, size)

    return set(genes), parent1, parent2


def test_parents_crossover_ox1():
    for _ in range(2000):
        genes, p1, p2 = different_random_parents(41, 200)
        child = parents_crossover_ox1((2, p1), (1, p2))
        assert set(child) == genes, 'Child genes do not match parent genes.'
        assert child != p1 or child != p2, 'Child should not be identical to both parents'

        # testing similarity with the fittest parent
        matches = 0
        for i in range(41):
            if child[i] == p1[i]: matches += 1

        assert matches >= 21, 'Child is not similar enough to the fittest parent'


def test_pop_crossover_ox1_roulettew_s():
    for _ in range(1000):
        genes = set(sample(range(100), 10))
        _population = generate_population(50, genes)
        _population = list(map(lambda x: (float(randint(0,100)), x), _population))
        options = {'c_fitness_l': cumulative_fitness(_population)}
        new_gen = pop_crossover_ox1_roulettew_s(_population, 50, options)
        for individual in new_gen:
            assert set(individual) == genes, 'Individual has not the same genes'
