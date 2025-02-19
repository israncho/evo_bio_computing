'''Module with functions that implement mutation operators
for the genetic algorithm.'''

from random import randint, sample, random
from typing import Callable, List
from src.gen_algo_framework.genetic_algorithm import Population, T, mutate_population


def swap_mutation(individual: List) -> List:
    '''
    Applies a swap mutation to a given individual. This mutation involves
    selecting two random positions in the individual's genome and swapping
    their values.
    Args:
        individual (List): The individual genome to be mutated.
    Returns:
        List: The mutated individual genome with two genes swapped.
    '''
    [i, j] = sample(list(range(len(individual))), 2)
    tmp = individual[i]
    individual[i] = individual[j]
    individual[j] = tmp
    return individual


def bit_flip_mutation(individual: List[int]) -> List[int]:
    '''
    Applies a bit flip mutation to the given individual.
    Args:
        individual (List): The individual genome to be mutated.
    Returns:
        List: The mutated individual genome with one bit flipped.
    '''
    i = randint(0, len(individual) - 1)
    individual[i] = individual[i] ^ 1
    return individual