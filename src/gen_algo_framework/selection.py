from typing import List, Tuple
from genetic_algorithm import T
from functools import reduce
from random import random
from bisect import bisect_left


def cumulative_list(population: List[Tuple[float, T]]) -> List[float]:
    '''
    Calculate the cumulative probability list for a given population.
    Args:
        population (List[Tuple[float, T]]): A list of tuples where each tuple
                                            contains a fitness value (float)
                                            and an individual (of generic type T).
    Returns:
        List[float]:    A list of cumulative probabilities, where each value
                        represents the cumulative sum of fitness
                        probabilities up to that point in the population.
    '''
    total_fitness = reduce(lambda acc, x: acc + x[0], population, 0)
    cumulative_probabilities = []
    accumulated = 0
    for fitness_i, _ in population:
        accumulated += fitness_i / total_fitness
        cumulative_probabilities.append(accumulated)
    return cumulative_probabilities


def roulette_wheel_toss(cumulative_probabilities: List[float]) -> int:
    '''
    Perform a roulette wheel selection toss to get an index based
    on cumulative probability list.
    Args:
        cumulative_probabilities (List[float]): A list of cumulative
        probabilities.
    Returns:
        int: The index selected based on the random toss within the
        cumulative probability list.
    '''
    return bisect_left(cumulative_probabilities, random())


def roulette_wheel_selection_two_parents(cumulative_probabilities: List[float]) -> Tuple[int, int]:
    '''
    Select two distinct parents from the population using roulette wheel selection.
    Args:
        cumulative_probabilities (List[float]): A list of cumulative
        probabilities generated from a population.
    Returns:
        Tuple[int, int]: A tuple containing the indices of the two selected parents.
    '''
    fst_parent_index = snd_parent_index = roulette_wheel_toss(cumulative_probabilities)
    while fst_parent_index == snd_parent_index:
        snd_parent_index = roulette_wheel_toss(cumulative_probabilities)
    return (fst_parent_index, snd_parent_index)
