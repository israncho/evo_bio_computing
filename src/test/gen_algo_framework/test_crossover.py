from typing import Set, Tuple, List
from src.gen_algo_framework.crossover import parents_crossover_ox1
from random import sample, choice


def different_random_parents(size: int, range_gene_size: int) -> Tuple[Set, List[int], List[int]]:
    genes = sample(range(range_gene_size), size)
    parent1 = [0] * size
    p1_indexes = list(range(size))
    parent2 = [0] * size
    p2_indexes = list(range(size))
    while parent1 == parent2:
        for x in genes:
            index_p1 = choice(p1_indexes)
            parent1[index_p1] = x
            p1_indexes.remove(index_p1)

            index_p2 = choice(p2_indexes)
            parent2[index_p2] = x
            p2_indexes.remove(index_p2)

        if parent1 == parent2:  # reset indexes if parents are equal
            p1_indexes = list(range(size))
            p2_indexes = list(range(size))
    return set(genes), parent1, parent2


def test_parents_crossover_ox1():
    for _ in range(1000):
        genes, p1, p2 = different_random_parents(20, 100)
        print(genes, p1, p2)
        child = parents_crossover_ox1((1, p1), (2, p2))
        assert set(child) == genes, 'Child genes do not match parent genes.'
        assert child != p1 or child != p2, 'Child should not be identical to both parents'
