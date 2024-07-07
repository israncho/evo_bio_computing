from typing import List, Tuple
from src.gen_algo_framework.genetic_algorithm import T
from functools import reduce
from random import uniform
from bisect import bisect_left


def cumulative_fitness(population: List[Tuple[float, T]],
                       extra_fitness: float = 0) -> Tuple[List[float], float]:
    '''
    Calculate the cumulative fitness list for a given population.
    This function is intended for maximization problems.
    Args:
        population (List[Tuple[float, T]]): A list of tuples where each tuple
                                            contains a fitness value (float)
                                            and an individual (of generic type T).
        extra_fitness (float): fitness to be added to the total fitness of
            the population
    Returns:
        Tuple[List[float], float]:  A list of cumulative fitness, where each value
                                    represents the cumulative sum of fitness up to
                                    that point in the population, sum of the fitness
                                    of the entire population.
    '''
    total_fitness = reduce(lambda acc, x: acc + x[0], population, 0) + extra_fitness
    cumulative_fitness_list = []
    accumulated = 0
    for fitness_i, _ in population:
        accumulated += fitness_i
        cumulative_fitness_list.append(accumulated)
    return cumulative_fitness_list, total_fitness


def roulette_wheel_toss(cumulative_fitness_list: List[float],
                        total_fitness: float) -> int:
    '''
    Perform a roulette wheel selection toss to get an index based
    on cumulative probability list.
    Args:
        cumulative_fitness_list (List[float]): A list of cumulative
            fitness.
        total_fitness (float): Sum of the fitness of the entire population
    Returns:
        int: The index selected based on the random toss within the
        cumulative fitness list.
    '''
    return bisect_left(cumulative_fitness_list, uniform(0, total_fitness))


def roulette_wheel_selection_two_parents(cumulative_fitness_list: List[float],
                                         total_fitness: float) -> Tuple[int, int]:
    '''
    Select two distinct parents from the population using roulette wheel selection.
    This function is intended for maximization problems.
    Args:
        cumulative_fitness_list (List[float]): A list of cumulative
            fitness generated from a population.
        total_fitness (float): Sum of the fitness of the entire population
    Returns:
        Tuple[int, int]: A tuple containing the indices of the two selected parents.
    '''
    assert len(cumulative_fitness_list) >= 2
    fst_parent_index = snd_parent_index = roulette_wheel_toss(cumulative_fitness_list, total_fitness)
    while fst_parent_index == snd_parent_index:
        snd_parent_index = roulette_wheel_toss(cumulative_fitness_list, total_fitness)
    return fst_parent_index, snd_parent_index


def remove_from_fitness_list(index: int,
                             individual_fitness: float,
                             cumulative_fitness_list: List[float],
                             total_fitness: float) -> Tuple[List[float], float]:
    '''
    Remove an individual from the cumulative fitness list based on its index
    and update the total fitness.

    Args:
        index (int): The index of the individual to be removed from the fitness list.
        individual_fitness (float): Fitness of the individual which is being removed from
                                    the cumulative fitness list.
        cumulative_fitness_list (List[float]): A list of cumulative fitness values
                                               where each value represents the cumulative
                                               sum of fitness up to that point in the population.
        total_fitness (float): The total fitness of the entire population before removal.

    Returns:
        Tuple[List[float], float]: A tuple containing the updated cumulative fitness list
                                   and the new total fitness value after removal.
    '''
    cumulative_fitness_list.pop(index)
    for i in range(index, len(cumulative_fitness_list)):
        cumulative_fitness_list[i] -= individual_fitness

    return cumulative_fitness_list, total_fitness - individual_fitness
