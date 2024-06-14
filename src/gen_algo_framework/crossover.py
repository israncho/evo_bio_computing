from typing import Any, List, Tuple
from random import randint
from collections import deque

def parents_crossover_ox1(parent1: Tuple[float, List[Any]], parent2: Tuple[float, List[Any]]) -> List[Any]:
    p1_size = len(parent1[1])
    p2_size = len(parent2[1])
    assert p1_size == p2_size

    chromosome_size = p1_size

    fitest = None
    lessfit = None
    if parent1[0] >= parent2[0]:
        fitest = parent1[1]
        lessfit = parent2[1]
    else:
        fitest = parent2[1]
        lessfit = parent1[1]

    child = [None for _ in range(chromosome_size)]

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
        if child[i] == None:
            child[i] = remaining_genes.popleft()

    return child


def __random_subinterval(_range: int, size: int) -> Tuple[int, int]:
    assert size > 0
    assert size <= _range + 1
    fst = randint(0, _range - size + 1)
    snd = fst + size - 1
    return (fst, snd)


def __random_snd_subinterval(_range: int, sub_interval: Tuple[int, int], size: int) -> Tuple[int, int]:
    assert size > 0
    a, b = sub_interval
    assert a <= b
    assert size <= a or size <= _range - b # check for enough space

    fst, snd = None, None

    if size <= a:
        fst = randint(0, a - size)
    else:
        fst = randint(b + 1, _range - size + 1)
    snd = fst + size - 1

    return (fst, snd)


def __two_random_subintervals(_range: int, size: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    assert size <= _range + 1
    size1 = randint(1, size - 1)
    size2 = size - size1
    interval1 = __random_subinterval(_range, size1)
    interval2 = __random_snd_subinterval(_range, interval1, size2)
    return (interval1, interval2)

