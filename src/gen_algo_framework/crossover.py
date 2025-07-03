'''Module with functions that implement crossover operators
for the genetic algorithm.'''

from typing import Any, List, Tuple, Callable, Hashable
from random import randint
from collections import deque
from src.gen_algo_framework.genetic_algorithm import Population, T
from src.gen_algo_framework.selection import roulette_wheel_toss


def order_crossover_ox1(parent1: Tuple[float, List[Hashable]],
                        parent2: Tuple[float, List[Hashable]],
                        _: dict) -> Tuple[List[Hashable], List[Hashable]]:
    '''
    Performs Order Crossover 1 (OX1) between two parents to produce two childs.
    Args:
        parent1 (Tuple[float, List[Hashable]]):
            First parent, represented by its fitness and chromosome.
        parent2 (Tuple[float, List[Hashable]]):
            Second parent, represented by its fitness and chromosome.
    Returns:
        Tuple[List[Hashable], List[Hashable]]: The resulting children (individuals).
    '''

    p1_genes = parent1[1]
    p2_genes = parent2[1]
    chromosome_size = len(p1_genes)
    assert chromosome_size == len(p2_genes)

    inheritance_p1 = chromosome_size // 2

    child1 = [None] * chromosome_size
    child2 = [None] * chromosome_size

    intervals = __full_random_subintervals(chromosome_size - 1, inheritance_p1)
    missing_for_child1 = set()
    missing_indexes_child1 = deque()
    missing_indexes_child2 = deque()

    for a, b, for_child1 in intervals:
        for i in range(a, b + 1):
            if for_child1:
                child1[i] = p1_genes[i]
                missing_indexes_child2.append(i)
            else:
                child2[i] = p1_genes[i]
                missing_indexes_child1.append(i)
                missing_for_child1.add(p1_genes[i])

    for p2_gen in p2_genes:
        if p2_gen in missing_for_child1:
            child1[missing_indexes_child1.popleft()] = p2_gen
        else:
            child2[missing_indexes_child2.popleft()] = p2_gen

    return child1, child2


def __random_subinterval(_range: int, size: int) -> Tuple[int, int]:
    '''
    Generates a random subinterval within the interval [0, _range].
    Args:
        _range (int): The maximum range of the interval.
        size (int): The size of the subinterval.
    Returns:
        Tuple[int, int]: The generated random subinterval.
    '''
    #assert size > 0
    #assert size <= _range + 1
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
    #assert size > 0
    a, b = sub_interval
    #assert a <= b
    #assert size <= a or size <= _range - b # check for enough space

    fst, snd = None, None

    if size <= a:
        fst = randint(0, a - size)
    else:
        fst = randint(b + 1, (_range - size) + 1)
    snd = fst + (size - 1)

    return (fst, snd)


def __two_random_subintervals(_range: int,
                              size: int) -> List[Tuple[int, int]]:
    '''
    Generates two random subintervals within a given range that does not overlap,
    summing to a specific size.
    Args:
        _range (int): The maximum range of the interval.
        size (int): The total size of the two combined subintervals.
    Returns:
        List[Tuple[int, int]]: The two generated random subintervals.
    '''
    #assert size <= _range + 1
    size1 = randint(1, size - 1)
    size2 = size - size1
    interval1 = __random_subinterval(_range, size1)
    interval2 = __random_snd_subinterval(_range, interval1, size2)
    if interval2[0] < interval1[0]:
        return [interval2, interval1]
    return [interval1, interval2]


def __full_random_subintervals(_range: int,
                               overall_size_for_one: int) -> List[Tuple[int, int, bool]]:
    '''
    Returns a list of non overlaping intervals that cover the whole
    [0, _range] interval. Two intervals have True value as their
    third entry in the tuple, and the sum of their distance is
    overall_size_for_one.
    Returns:
        List[Tuple[int, int, bool]]: list of tuples modeling
            intervals, with a third entry just for the crossover
            operator.
    '''
    intervals_for_one = __two_random_subintervals(_range, overall_size_for_one)
    curr = 0
    all_intervals = []
    for i, j in intervals_for_one:
        if curr < i:
            all_intervals.append((curr, i - 1, False))
        curr = j + 1
        all_intervals.append((i, j, True))
    if curr <= _range:
        all_intervals.append((curr, _range, False))
    return all_intervals


def gen_n_points(num_points: int, size: int) -> List[int]:
    '''
    Generates a list of random points within a given range.
    Args:
        num_points (int): The number of points to generate.
        size (int): The size of the range in which the
            points will be generated.

    Returns:
        List[int]: A list of random points generated within
            the range from 1 to 'size-1'.
    '''
    assert 0 < num_points, f'{num_points}'
    assert num_points < size, f'{num_points}, {size}'
    i = 0
    points = []
    points_left = num_points
    while points_left > 0:
        new_point = randint(i + 1, size - points_left)
        i = new_point
        points.append(new_point)
        points_left -= 1
    return points


def n_points_crossover_parents(parent1: Tuple[float, List],
                               parent2: Tuple[float, List],
                               points: List[int]) -> Tuple[List, List]:
    '''
    Performs an n-point crossover between two parents,
    swapping segments of the parents chromosomes
    at the specified points to generate two children.

    Args:
        parent1 (Tuple[float, List]): The first parent,
            where the first element is the fitness and
            the second element is the chromosome (list of genes).
        parent2 (Tuple[float, List]): The second parent,
            in the same format as 'parent1'.
        points (List[int]): A list of crossover points
            where segments will be swapped between the parents.
    Returns:
        Tuple[List, List]: Two children generated from
            the crossover operation, each represented
            as a list of genes.
    '''
    size = len(parent1[1])
    assert size == len(parent2[1])

    child1 = [None] * size
    child2 = [None] * size
    index_p = 0
    c1_inherits_p1 = True

    for i, (bit_p1, bit_p2) in enumerate(zip(parent1[1], parent2[1])):

        if index_p < len(points) and i == points[index_p]:
            c1_inherits_p1 ^= True
            index_p += 1

        if c1_inherits_p1:
            child1[i] = bit_p1
            child2[i] = bit_p2
        else:
            child1[i] = bit_p2
            child2[i] = bit_p1

    return child1, child2


def population_n_points_crossover_roulettew_s(population: Population[List],
                                  new_gen_size: int,
                                  options: dict) -> Population[List]:
    '''
    Applies n-point crossover to generate a new population using roulette
    wheel selection.
    Args:
        population (List[Tuple[float, List]]): The current
            population, where each individual is represented as a tuple
            containing its fitness (float) and a list of genes (List).
        new_gen_size (int): The desired size of the new generation.
        options (dict): A dictionary containing options for the crossover:
            - 'c_fitness_l' (List[float]): A cumulative fitness list used
                for roulette wheel selection.
            - 'n_points' (int): The number of crossover points to generate
                during the n-point crossover.
    Returns:
        List[List]: A list representing the new generation, where
        each individual is represented by a list of genes resulting from
        the crossover operation.
    '''
    cumulative_fitness_list = options['c_fitness_l']
    n_points = options['n_points']
    new_gen = []
    while len(new_gen) < new_gen_size:
        p1_index = roulette_wheel_toss(cumulative_fitness_list)
        p2_index = roulette_wheel_toss(cumulative_fitness_list)
        points = gen_n_points(n_points, len(population[p1_index][1]))
        child1, child2 = n_points_crossover_parents(population[p1_index],
                                                    population[p2_index],
                                                    points)
        new_gen.append(child1)
        new_gen.append(child2)
    return new_gen
