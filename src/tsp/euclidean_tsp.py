'''Module to model the euclidean TSP and its functions
to be used in the genetic algorithm.'''

from typing import List, Set, Tuple
from math import sqrt


VectorRn = Tuple[float | int, ...]
'''Type for cities.'''

TSPInstance = Set[VectorRn]
'''Type for instances.'''

TSPPermutation = List[VectorRn]
'''Type for solutions. Does not
include de first city.'''


def euclidean_distance(u: VectorRn, v: VectorRn) -> float:
    '''
    Calculate the Euclidean distance between two vectors.
    Args:
        u (VectorRn): First vector in R^n.
        v (VectorRn): Second vector in R^n.
    Returns:
        float: The Euclidean distance between u and v.
    '''
    assert len(u) == len(v), f'Different dimension: {u}, {v}'
    _sum = 0
    for u_i, v_i in zip(u, v):
        _sum += (u_i - v_i)**2

    return sqrt(_sum)


def tour_distance(fst_v: VectorRn,
                  rest_of_v: TSPPermutation,
                  weights: dict) -> float:
    '''
    Calculate the total distance of a TSP tour.
    Args:
        solution (TSPSolution): A TSP solution,
            which is a tuple containing the first city
            and a list of the remaining cities in the tour.
    Returns:
        float: The total distance of the tour, including
            the distance between the last city and the
            first city to complete the tour.
    '''
    distance = weights[(fst_v, rest_of_v[0])]
    distance += weights[(rest_of_v[-1], fst_v)]

    for i in range(1, len(rest_of_v)):
        distance += weights[(rest_of_v[i - 1], rest_of_v[i])]

    return distance


def euc_tsp_fitness(population: List[TSPPermutation],
                    options: dict) -> List[Tuple[float, TSPPermutation]]:
    '''
    Calculate the fitness of each tour in the population for the TSP.
    Args:
        population (List[TSPPermutation]): A list of TSP tours, where
            each tour is a permutation of the cities.
        options (dict): A dictionary containing the following keys:
            - 'fst_city': The first city in the tour.
            - 'weights': A dictionary of weights representing distances
                between cities.
    Returns:
        List[Tuple[float, TSPPermutation]]: A list of tuples, each
            containing the total distance of the tour and the corresponding
            tour itself.
    '''
    fst_v = options['fst_city']
    weights = options['weights']
    pop_with_fitness = list(
        map(
            lambda x: (tour_distance(fst_v, x, weights), x),
            population
        )
    )
    return pop_with_fitness


def build_weight_dict(tsp_instance: TSPInstance) -> dict:
    '''
    Build a dictionary of weights representing the distances between
    each pair of cities in a TSP instance.
    Args:
        tsp_instance (TSPInstance): A set of vectors representing
            the coordinates of the cities in the TSP.
    Returns:
        dict: A dictionary where each key is a tuple of two cities
            (u, v) and the corresponding value is the Euclidean
            distance between them.
    '''
    weights = {}
    all_cities = list(tsp_instance)
    size = len(all_cities)

    for i in range(size):
        for j in range(i + 1, size):
            u, v = all_cities[i], all_cities[j]
            weights[(u, v)] = euclidean_distance(u, v)
            weights[(v, u)] = weights[(u, v)]

    return weights