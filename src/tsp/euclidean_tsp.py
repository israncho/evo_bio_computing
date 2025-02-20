'''Module to model the euclidean TSP and its functions
to be used in the genetic algorithm.'''

from typing import List, Tuple
from math import sqrt, inf

from src.gen_algo_framework.genetic_algorithm import Population, population_fitness_computing
from src.gen_algo_framework.population_utils import transform_to_max
from src.gen_algo_framework.selection import cumulative_fitness
from src.local_search.permutation import local_search_2_opt


EucCity = Tuple[float | int, ...]
'''Type for cities.'''

EucTSPPermutation = List[EucCity]
'''Type for solutions. Does not
include de first city.'''


def euclidean_distance(u: EucCity, v: EucCity) -> float:
    '''
    Calculate the Euclidean distance between two vectors.
    Args:
        u (EucCity): First city (vector in R^n).
        v (EucCity): Second city (vector in R^n).
    Returns:
        float: The Euclidean distance between u and v.
    '''
    assert len(u) == len(v), f'Different dimension: {u}, {v}'
    _sum = 0
    for u_i, v_i in zip(u, v):
        _sum += (u_i - v_i)**2

    return sqrt(_sum)


def tour_distance(seq_of_cities: EucTSPPermutation,
                  options: dict) -> float:
    '''
    Calculate the total distance of a TSP tour.
    Args:
        seq_of_cities (EucTSPPermutation): A sequence representing
        the order of cities in the tour, excluding the starting city.
        options (dict): A dictionary containing the following keys:
            - 'fst_city' (EucCity): The first city in the tour.
            - 'weights' (dict): A dictionary where keys are tuples of
                city pairs (u, v) and values are the Euclidean
                distances between those cities.
    Returns:
        float: The total distance of the tour, including the return to
        the starting city.
    '''
    options['f_execs'] += 1
    fst_city = options['fst_city']
    weights = options['weights']

    distance = weights[(fst_city, seq_of_cities[0])]
    distance += weights[(seq_of_cities[-1], fst_city)]

    for i in range(1, len(seq_of_cities)):
        distance += weights[(seq_of_cities[i - 1], seq_of_cities[i])]

    if distance < options['current_best'][0]:
        options['current_best'] = distance, seq_of_cities

    options['best_fitness_found_history'].append(options['current_best'][0])

    return distance


def build_weight_dict(fst_city: EucCity,
                      rest_of_cities: EucTSPPermutation) -> dict:
    '''
    Build a dictionary of weights representing the distances between
    each pair of cities in a TSP instance.
    Args:
        fst_city (EucCity): The first city in the tour.
        rest_of_cities (EucTSPPermutation): A list of the
            remaining cities in the tour.
    Returns:
        dict: A dictionary where each key is a tuple of two cities
            (u, v) and the corresponding value is the Euclidean
            distance between them.
    '''
    weights = {}

    rest_of_cities.append(fst_city) # adding fst city
    size = len(rest_of_cities)

    for i in range(size):
        for j in range(i + 1, size):
            u, v = rest_of_cities[i], rest_of_cities[j]
            weights[(u, v)] = euclidean_distance(u, v)
            weights[(v, u)] = weights[(u, v)]

    rest_of_cities.pop()    # removing fst city

    return weights


def simple_euc_tsp_options_handler(population: Population[EucTSPPermutation],
                                   options: dict,
                                   init: bool = False) -> dict:
    if init:
        options['population_fit_avgs'] = []
        options['current_best'] = inf, None
        options['f_execs'] = 0
        options['gen_fittest_fitness'] = None
        options['best_fitness_found_history'] = []
        options['offspring_s'] = options['pop_size']
        options['next_gen_pop_s'] = options['pop_size']

        if options['local_s_iters'] > 0:
            options['target_f'] = tour_distance
        return options

    pop_only_fitness_values = list(map(lambda x: (x[0], None), population))
    pop_only_fitness_values = transform_to_max(pop_only_fitness_values) # pyright: ignore
    options['c_fitness_l'] = cumulative_fitness(pop_only_fitness_values) # pyright: ignore
    return options
