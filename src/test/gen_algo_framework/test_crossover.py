from random import randint, sample
from typing import Set, Tuple, List
from src.gen_algo_framework.crossover import gen_n_points, n_points_crossover_parents, parents_crossover_ox1, pop_crossover_ox1_roulettew_s
from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.gen_algo_framework.selection import cumulative_fitness


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

        clone = parents_crossover_ox1((2, p1), (2, p1))
        assert clone == p1


def test_pop_crossover_ox1_roulettew_s():
    for _ in range(1000):
        genes = set(sample(range(100), 10))
        _population = generate_population_of_permutations(50, genes)
        _population = list(map(lambda x: (float(randint(0,100)), x), _population))
        options = {'c_fitness_l': cumulative_fitness(_population)}
        new_gen = pop_crossover_ox1_roulettew_s(_population, 50, options)
        for individual in new_gen:
            assert set(individual) == genes, 'Individual has not the same genes'


def test_gen_n_points():
    for _ in range(10000):
        size = randint(11, 30)

        points = gen_n_points(randint(1, 10), size)

        set_points = set(points)
        assert len(points) == len(set_points)

        assert 0 not in set_points

        for e in points:
            assert e < size


def test_n_points_crossover_parents():
    for _ in range(10000):
        parents_size = randint(10, 20)
        p1 = [randint(0, 1) for _ in range(parents_size)]
        p2 = [randint(0, 1) for _ in range(parents_size)]

        n_points = randint(1, parents_size - 1)

        points = gen_n_points(n_points, parents_size)

        c1, c2 = n_points_crossover_parents((None, p1), (None, p2), points) # pyright: ignore

        c1_inherits_p1 = True
        index_p = 0

        for i, (b_c1, b_c2, b_p1, b_p2) in enumerate(zip(c1, c2, p1, p2)):
            if index_p < len(points) and i == points[index_p]:
                c1_inherits_p1 ^= True
                index_p += 1

            if c1_inherits_p1:
                assert b_c1 == b_p1
                assert b_c2 == b_p2
            else:
                assert b_c1 == b_p2
                assert b_c2 == b_p1
