from random import randint, sample

from src.gen_algo_framework.genetic_algorithm import generate_population
from src.gen_algo_framework.replacement import full_generational_replacement, roulette_gen_replacement
from src.gen_algo_framework.selection import cumulative_fitness


def test_full_generational_replacement():
    for _ in range(500):
        genes = set([randint(0, 50) for _ in range(randint(20, 50))])
        parents = generate_population(randint(20, 50), genes)
        children = generate_population(randint(20, 50), genes)
        assert full_generational_replacement(parents, children, 0, {}) == children


def test_roulette_gen_replacement():
    for _ in range(1000):
        fittest_individuals = [None] * randint(10, 15)
        fittest_individuals = list(map(lambda x: (float(randint(10000 , 100000)), x), fittest_individuals))

        unfit_individuals = [None] * randint(35, 60)
        unfit_individuals = list(map(lambda x: (float(randint(10 , 50)), x), unfit_individuals))

        _population = sample(fittest_individuals + unfit_individuals,
                             len(fittest_individuals) + len(unfit_individuals))

        curr_population = _population[:len(_population) // 2]
        offspring = _population[len(_population) // 2:]

        options = {'c_fitness_l': cumulative_fitness(curr_population)}
        next_gen = roulette_gen_replacement(curr_population, offspring,
                                               int(len(fittest_individuals) * 1.75),
                                               options)

        next_gen_set = set(next_gen)
        for x in fittest_individuals:
            assert x in next_gen_set
