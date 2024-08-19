from typing import List, Set, Tuple
from math import sqrt


VectorRn = Tuple[float, ...]

TSPInstance = Set[VectorRn]

TSPSolution = Tuple[VectorRn, List[VectorRn]]


def euclidean_distance(u: VectorRn, v: VectorRn) -> float:
    '''
    Calculate the Euclidean distance between two vectors.

    Args:
        u (VectorRn): First vector in R^n.
        v (VectorRn): Second vector in R^n.

    Returns:
        float: The Euclidean distance between u and v.
    '''
    assert len(u) == len(v), 'The given vectors don\'t have the same dimension.'
    _sum = 0
    for i in range(len(u)):
        _sum += (u[i] - v[i])**2

    return sqrt(_sum)


def tour_distance(solution: TSPSolution) -> float:
    '''
    Calculate the total distance of a TSP tour.

    Args:
        solution (TSPSolution): A TSP solution, which is a tuple containing the first city
                                and a list of the remaining cities in the tour.

    Returns:
        float: The total distance of the tour, including the distance between the last city
               and the first city to complete the tour.
    '''
    fst_city, rest_of_cities = solution

    distance = euclidean_distance(fst_city, rest_of_cities[0])
    distance += euclidean_distance(rest_of_cities[-1], fst_city)

    for i in range(1, len(rest_of_cities)):
        distance += euclidean_distance(rest_of_cities[i - 1], rest_of_cities[i])

    return distance
