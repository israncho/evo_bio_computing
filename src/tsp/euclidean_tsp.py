'''Module to model the euclidean TSP and its functions
to be used in the genetic algorithm.'''

from typing import List, Tuple
from math import sqrt

from src.gen_algo_framework.genetic_algorithm import transform_to_max


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


def tour_distance(fst_city: EucCity,
                  rest_of_cities: EucTSPPermutation,
                  weights: dict) -> float:
    '''
    Calculate the total distance of a TSP tour.
    Args:
        fst_city (EucCity): The first city in the tour.
        rest_of_cities (EucTSPPermutation): A list of the
            remaining cities in the tour.
        weights (dict): A dictionary where keys are tuples
            of city pairs (u, v) and values are the
            Euclidean distances between those cities.
    Returns:
        float: The total distance of the tour.
    '''
    distance = weights[(fst_city, rest_of_cities[0])]
    distance += weights[(rest_of_cities[-1], fst_city)]

    for i in range(1, len(rest_of_cities)):
        distance += weights[(rest_of_cities[i - 1], rest_of_cities[i])]

    return distance


def euc_tsp_fitness_maximization(population: List[EucTSPPermutation],
                    options: dict) -> List[Tuple[float, EucTSPPermutation]]:
    '''
    Evaluate the fitness of a population of TSP solutions in a maximization
    context by transforming the fitness scores.

    This function calculates the fitness (tour distance) of each individual
    in the population. It then transforms the fitness scores to a maximization
    problem. The shorter the tour, the higher the fitness.

    Args:
        population (List[EucTSPPermutation]): A list of TSP permutations,
            where each permutation represents a potential solution (tour).
        options (dict): A dictionary containing:
            - 'fst_city' (EucCity): The first city in the TSP tour.
            - 'weights' (dict): A dictionary with the distances between
              city pairs, where keys are tuples of two cities (u, v), and
              values are the Euclidean distances between them.
            - 'population_fit_avgs' (List[float]): A list where the
              average fitness of each population over generations is
              appended.
    Returns:
        List[Tuple[float, EucTSPPermutation]]: A list of tuples where each
        tuple contains:
            - The fitness score of the individual after being transformed
              to a maximization problem (higher score for better fitness).
            - The corresponding TSP permutation (solution).
    '''
    fst_c = options['fst_city']
    weights = options['weights']
    population_fitness_sum = 0
    pop_with_fitness = []
    for individual in population:
        individual_fitness = tour_distance(fst_c,
                                           individual,
                                           weights)
        population_fitness_sum += individual_fitness
        pop_with_fitness.append((individual_fitness, individual))

    options['population_fit_avgs'].append(population_fitness_sum / len(population))

    pop_with_fitness = transform_to_max(pop_with_fitness)

    return pop_with_fitness


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
