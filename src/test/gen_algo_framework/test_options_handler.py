from collections import defaultdict
from random import randint
from src.gen_algo_framework.options_handler import minimum_options_handler, roulette_wheel_based_options
from src.gen_algo_framework.selection import cumulative_fitness


rand_pop = lambda : list(map(lambda x: (float(randint(1 , 100)), x), [None] * randint(20, 60)))


def test_minimum_options_handler(options = None):
    if options is not None:
        assert options['initial_population'] is not None and type(options['initial_population']) == int
        assert options['offspring_s'] is not None and type(options['offspring_s']) == int
        assert options['next_gen_pop_s'] is not None and type(options['next_gen_pop_s']) == int
        assert options['mutation_proba'] is not None and type(options['mutation_proba']) == float
        assert options['another_swap_p'] is not None and type(options['another_swap_p']) == float
        return

    for _ in range(10):
        population = rand_pop()
        pop_size = len(population)
        options = defaultdict(lambda : None)
        for _ in range(10):
            options = minimum_options_handler(population, options)
            assert options['initial_population'] is not None and options['initial_population'] == pop_size
            assert options['offspring_s'] is not None and options['offspring_s'] == pop_size
            assert options['next_gen_pop_s'] is not None and options['next_gen_pop_s'] == pop_size
            assert options['mutation_proba'] is not None and options['mutation_proba'] == 1 / pop_size
            assert options['another_swap_p'] is not None and options['another_swap_p'] == 1 / pop_size


def test_roulette_wheel_based_options():
    for _ in range(100):
        population = rand_pop()
        options = defaultdict(lambda : None)
        for _ in range(10):
            options = roulette_wheel_based_options(population, options)
            assert cumulative_fitness(population) == options['c_fitness_l']
            assert options['c_fitness_l'] is not None
            test_minimum_options_handler(options)
            population.pop(randint(0, len(population) - 1))

