from typing import Set, Tuple, List
from src.gen_algo_framework.crossover import parents_crossover_ox1
from src.gen_algo_framework.genetic_algorithm import population
from random import sample


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
        child = parents_crossover_ox1((1, p1), (2, p2), lambda x, y: x <= y)
        assert set(child) == genes, 'Child genes do not match parent genes.'
        assert child != p1 or child != p2, 'Child should not be identical to both parents'

        # testing similarity with the fittest parent
        matches = 0
        for i in range(41):
            if child[i] == p1[i]: matches += 1

        assert matches >= 21, 'Child is not similar enough to the fittest parent'

def test_population_crossover_ox1():
    for _ in range(1000):
        genes = set(sample(range(100), 10))
        _population = population(50, genes)
        for individual in _population:
            assert set(individual) == genes, 'Individual has not the same genes'
