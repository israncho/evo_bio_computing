from random import randint, sample
from typing import Set, Tuple, List
from src.gen_algo_framework.crossover import gen_n_points, n_points_crossover_parents, population_n_points_crossover_roulettew_s
from src.gen_algo_framework.crossover import __full_random_subintervals, order_crossover_ox1
from src.gen_algo_framework.genetic_algorithm import population_crossover
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


def test___full_random_subintervals():
    for _ in range(1000):
        size = randint(100, 101)
        half = size // 2
        target_set = set(range(size)) # [0, 99] or [0, 100]
        intervals = __full_random_subintervals(size - 1, half)
        curr_elems_found = []
        true_count = 0
        for i, j, bool_val in intervals:
            if bool_val:
                true_count += 1
            curr_elems_found.extend(list(range(i, j + 1)))

        assert true_count == 2
        assert set(curr_elems_found) == target_set


def test_order_crossover_ox1():
    for _ in range(2000):
        genes, p1, p2 = different_random_parents(41, 200)
        child1, child2 = order_crossover_ox1((0, p1), (0, p2), None)
        assert set(child1) == genes
        assert set(child2) == genes
        assert child1 != p1 or child1 != p2
        assert child2 != p1 or child2 != p2

        for gen_p1, gen_c1, gen_c2 in zip(p1, child1, child2):
            assert gen_p1 == gen_c1 or gen_p1 == gen_c2

        for gen_p2 in p2:
            assert gen_p2 in child1 or gen_p2 in child2


def test_population_crossover():
    for _ in range(1000):
        genes = set(sample(range(100), 50))
        population = generate_population_of_permutations(11, genes)
        population = list(map(lambda x : (0, x), population))
        indexes_selected_parents = list(zip(sample(range(11), 6), sample(range(11), 6)))
        new_gen = population_crossover(population, indexes_selected_parents, 11, order_crossover_ox1, {})
        for child in new_gen:
            assert set(child) == genes
            for adult in population:
                assert child != adult


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


def test_population_n_points_crossover_roulettew_s():
    for _ in range(250):
        individual_size = randint(5, 10)
        population = [(1, [randint(0, 1)] * individual_size) for _ in range(1000)]
        population_size = len(population)

        options = {'c_fitness_l': cumulative_fitness(population),
                   'n_points': randint(1, individual_size - 1)}
        offspring = population_n_points_crossover_roulettew_s(population,
                                                              population_size * 2,
                                                              options)


        mixed_children = 0
        for child in offspring:
            if set(child) == {1, 0}:
                mixed_children += 1

        assert population_size - 200 < mixed_children
        assert mixed_children < population_size + 200
