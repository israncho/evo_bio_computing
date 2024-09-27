'''Module with functions that implement selection operators
for the genetic algorithm.'''

from random import uniform
from bisect import bisect_left
from typing import List, Tuple
from src.gen_algo_framework.genetic_algorithm import T


def cumulative_fitness(population: List[Tuple[float, T]],
                       extra_fitness: float = 0) -> List[float]:
    '''
    Calculate the cumulative fitness list for a given population.
    This function is intended for maximization problems.
    Args:
        population (List[Tuple[float, T]]):
            A list of tuples where each tuple contains a fitness
            value (float) and an individual (of generic type T).

        extra_fitness (float):
            fitness to be added to the total fitness of
            the population
    Returns:
        List[float]:
            A list of cumulative fitness, where each value
            represents the cumulative sum of fitness up to that
            point in the population.
    '''
    cumulative_fitness_list = []
    accumulated = extra_fitness
    for fitness_i, _ in population:
        accumulated += fitness_i
        cumulative_fitness_list.append(accumulated)
    return cumulative_fitness_list


def roulette_wheel_toss(cumulative_fitness_list: List[float]) -> int:
    '''
    Perform a roulette wheel selection toss to get an index based
    on cumulative probability list.
    Args:
        cumulative_fitness_list (List[float]):
            A list of cumulative fitness.

    Returns:
        int: The index selected based on the random toss within the
        cumulative fitness list.
    '''
    return bisect_left(cumulative_fitness_list,
                       uniform(0, cumulative_fitness_list[-1]))


def remove_from_fitness_list(index: int,
                             individual_fitness: float,
                             cumulative_fitness_list: List[float]
                             ) -> List[float]:
    '''
    Remove an individual from the cumulative fitness list based on its index
    and update the total fitness.
    Args:
        index (int): The index of the individual to be removed from
            the fitness list.
        individual_fitness (float): Fitness of the individual which
            is being removed from the cumulative fitness list.
        cumulative_fitness_list (List[float]): A list of cumulative
            fitness values where each value represents the cumulative
            sum of fitness up to that point in the population.
    Returns:
        List[float]: the updated cumulative fitness list.
    '''
    cumulative_fitness_list.pop(index)
    for i in range(index, len(cumulative_fitness_list)):
        cumulative_fitness_list[i] -= individual_fitness

    return cumulative_fitness_list
