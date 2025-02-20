'''Module with functions that implement replacement operators
for the genetic algorithm.'''

from typing import List, Tuple
from heapq import nsmallest, nlargest
from src.gen_algo_framework.genetic_algorithm import T, Population
from src.gen_algo_framework.selection import roulette_wheel_toss, remove_from_fitness_list
from src.gen_algo_framework.selection import cumulative_fitness

def full_generational_replacement(_: Population[T],
                                  offspring: Population[T],
                                  __: int,
                                  ___: dict) -> Population[T]:
    return offspring


def full_gen_replacement_elitist(_: Population[T],
                                 offspring: Population[T],
                                 __: int,
                                 options: dict) -> Population[T]:

    # ensure best is in the population
    if options['current_best'][0] < options['gen_fittest_fitness']:
        offspring.pop()
        offspring.append(options['current_best'])
        options['gen_fittest_fitness'] = options['current_best']

    return offspring


def replacement_of_the_worst(current_pop: Population[T],
                             offspring: Population[T],
                             new_pop_size: int,
                             options: dict) -> Population[T]:

    assert new_pop_size < len(current_pop) + len(offspring)

    current_pop.extend(offspring)

    options['gen_fittest_fitness'] = options['current_best'][0]

    next_gen = nsmallest(new_pop_size, current_pop)

    return next_gen


all_replacement_funcs = {'full_generational_replacement': full_generational_replacement,
                         'full_gen_replacement_elitist': full_gen_replacement_elitist,
                         'replacement_of_the_worst': replacement_of_the_worst}
