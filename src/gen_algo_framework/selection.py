'''Module with functions that implement selection operators
for the genetic algorithm.'''

from random import uniform
from bisect import bisect_left
from typing import List, Tuple
from math import ceil
from src.gen_algo_framework.genetic_algorithm import T, Population


def cumulative_fitness(population: Population[T],
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


def roulette_wheel_selection(population: Population[T],
                             offspring_size: int,
                             options: dict) -> List[Tuple[int, int]]:
    '''
    Returns a list with the indexes of the selected parents as couples
    (tuple) of the given population. The selection is done by the
    roulette wheel selection method.
    Args:
        population (Population[T]):
            The current population, where each element is a tuple containing
            the fitness value and the chromosome.
        offspring_size (int):
            The desired size of the new generation.
        options (dict): A dictionary with the cumulative fitness list
            from the population argument, associated with the
            key \'c_fitness_l\' .
    Returns:
        List[Tuple[int, int]]: List of tuples with the indices of the selected
            individuals.
    '''

    cumulative_fitness_list = options['c_fitness_l']
    number_couples = ceil(offspring_size / 2)
    indexes_selected_parents = []
    for _ in range(number_couples):
        couple = (roulette_wheel_toss(cumulative_fitness_list),
                  roulette_wheel_toss(cumulative_fitness_list))
        indexes_selected_parents.append(couple)
    return indexes_selected_parents


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
