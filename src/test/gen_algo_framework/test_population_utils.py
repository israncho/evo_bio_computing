from random import randint, uniform
from typing import Set
from src.gen_algo_framework.population_utils import generate_population_of_bit_vectors, generate_population_of_permutations, transform_to_max


def test_gen_pop_of_permutations():
    for _ in range(500):
        gene_set: Set[int] = set()
        for _ in range(20):
            gene_set.add(randint(0, 1000))

        rand_population = generate_population_of_permutations(10, gene_set)

        for individual in rand_population:
            assert set(individual) == gene_set, 'individual does not contain the same gene set.'

        for i in range(len(rand_population)):
            curr = rand_population[i]
            diff_count = 0
            for j in range(len(rand_population)):
                if j == i: continue
                if curr != rand_population[j]:
                    diff_count += 1
            assert diff_count >= 1, 'The population has at least two identical individuals.'


def test_gen_pop_of_bit_vectors():
    for _ in range(500):
        pop_size = randint(15, 30)
        dimension = randint(2, 10)
        bits_per_entry = randint(10, 20)
        v_n_bits = [bits_per_entry] * dimension

        population = generate_population_of_bit_vectors(pop_size, v_n_bits)

        bits_counted = 0
        for vec_of_bits in population:
            assert type(vec_of_bits) == list
            for bit in vec_of_bits:
                bits_counted += 1
                assert bit in (0, 1)

        assert bits_counted == pop_size * dimension * bits_per_entry


def test_transform_to_max():
    for _ in range(1000):
        rand_population = list(map(lambda x : (0.0, x), range(randint(20, 40))))
        prev_fitness = 0
        for i in range(len(rand_population)):
            fitness = prev_fitness + uniform(2.0, 20.0)
            rand_population[i] = fitness, rand_population[i][1]
            prev_fitness = fitness
        to_max_popu = transform_to_max(rand_population)

        assert to_max_popu[0][0] > 0
        for i in range(1, len(to_max_popu)):
            assert to_max_popu[i - 1][0] > to_max_popu[i][0]
            assert to_max_popu[i][0] > 0
