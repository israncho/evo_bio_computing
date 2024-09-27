'''Module with functions that implement crossover operators
for the genetic algorithm.'''

from typing import Any, List, Tuple
from random import randint
from collections import deque
from src.gen_algo_framework.genetic_algorithm import GeneType
from src.gen_algo_framework.selection import roulette_wheel_toss


def parents_crossover_ox1(parent1: Tuple[float, List[GeneType]],
                          parent2: Tuple[float, List[GeneType]]) -> List[GeneType]:
    '''
    Performs Order Crossover 1 (OX1) between two parents to produce a child.
    This function is intended for maximization problems.
    Args:

        parent1 (Tuple[float, List[GeneType]]):
            First parent, represented by its fitness and chromosome.

        parent2 (Tuple[float, List[GeneType]]):
            Second parent, represented by its fitness and chromosome.

    Returns:
        List[GeneType]: The resulting child (individual).
    '''

    assert len(parent1[1]) == len(parent2[1])

    chromosome_size = len(parent1[1])

    fitest = None
    lessfit = None
    if parent1[0] >= parent2[0]:
        fitest = parent1[1]
        lessfit = parent2[1]
    else:
        fitest = parent2[1]
        lessfit = parent1[1]

    child: List[Any] = [None] * chromosome_size

    genes_from_fit = chromosome_size // 2

    if genes_from_fit * 2 < chromosome_size:
        genes_from_fit += 1

    genes = set(parent1[1])

    intervals = __two_random_subintervals(chromosome_size - 1, genes_from_fit)
    for a, b in intervals:
        for i in range(a, b + 1):
            gene = fitest[i]
            genes.remove(gene)
            child[i] = gene

    remaining_genes = deque()
    for a in lessfit:
        if a in genes:
            remaining_genes.append(a)

    for i in range(chromosome_size):
        if child[i] is None:
            child[i] = remaining_genes.popleft()

    return child


def pop_crossover_ox1_roulettew_s(population: List[Tuple[float, List[GeneType]]],
                                  new_gen_size: int,
                                  options: dict) -> List[List[GeneType]]:
    '''
    Creates a new generation of offspring using the Order Crossover 1 (OX1) method.
    This function is intended for maximization problems.
    Args:
        population (List[Tuple[float, List[GeneType]]]):
            The current population, where each element is a tuple containing
            the fitness value and the chromosome.

        new_gen_size (int):
            The desired size of the new generation.

        options (dict): A dictionary with the cumulative fitness list
            from the population argument, associated with the
            key \'c_fitness_l\' .

    Returns:
        List[List[GeneType]]: A list of new individuals representing the offspring.
    '''
    cumulative_fitness_list = options['c_fitness_l']
    new_gen = []
    while len(new_gen) < new_gen_size:
        p1_index = roulette_wheel_toss(cumulative_fitness_list)
        p2_index = roulette_wheel_toss(cumulative_fitness_list)
        child = parents_crossover_ox1(population[p1_index],
                                      population[p2_index])
        new_gen.append(child)
    return new_gen


def __random_subinterval(_range: int, size: int) -> Tuple[int, int]:
    '''
    Generates a random subinterval within the interval [0, _range].
    Args:
        _range (int): The maximum range of the interval.

        size (int): The size of the subinterval.

    Returns:
        Tuple[int, int]: The generated random subinterval.
    '''
    assert size > 0
    assert size <= _range + 1
    fst = randint(0, (_range - size) + 1)
    snd = fst + (size - 1)
    return (fst, snd)


def __random_snd_subinterval(_range: int,
                             sub_interval: Tuple[int, int],
                             size: int) -> Tuple[int, int]:
    '''
    Generates a second random subinterval that does not overlap with
    the given first subinterval.
    Args:
        _range (int): The maximum range of the interval.

        sub_interval (Tuple[int, int]): The first already generated subinterval.

        size (int): The size of the second subinterval.

    Returns:
        Tuple[int, int]: The generated second random subinterval.
    '''
    assert size > 0
    a, b = sub_interval
    assert a <= b
    assert size <= a or size <= _range - b # check for enough space

    fst, snd = None, None

    if size <= a:
        fst = randint(0, a - size)
    else:
        fst = randint(b + 1, (_range - size) + 1)
    snd = fst + (size - 1)

    return (fst, snd)


def __two_random_subintervals(_range: int,
                              size: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    '''
    Generates two random subintervals within a given range that does not overlap,
    summing to a specific size.
    Args:
        _range (int): The maximum range of the interval.

        size (int): The total size of the two combined subintervals.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: The two generated random subintervals.
    '''
    assert size <= _range + 1
    size1 = randint(1, size - 1)
    size2 = size - size1
    interval1 = __random_subinterval(_range, size1)
    interval2 = __random_snd_subinterval(_range, interval1, size2)
    return (interval1, interval2)
