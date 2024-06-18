from typing import List, Tuple
from gen_algo_framework import T
from functools import reduce
from random import random
from bisect import bisect_left


def cumulative_list(population: List[Tuple[float, T]]) -> List[float]:
    total_fitness = reduce(lambda acc, x: acc + x[0], population, 0)
    cumulative_probabilities = []
    accumulated = 0
    for fitness_i, _ in population:
        accumulated += fitness_i / total_fitness
        cumulative_probabilities.append(accumulated)
    return cumulative_probabilities


def roulette_wheel_toss(cumulative_probabilities: List[float]) -> int:
    return bisect_left(cumulative_probabilities, random())


def roulette_wheel_selection_two_parents(population: List[Tuple[float, T]]) -> Tuple[int, int]:
    cumulative_probabilities = cumulative_list(population)
    fst_parent_index = snd_parent_index = roulette_wheel_toss(cumulative_probabilities)
    while fst_parent_index == snd_parent_index:
        snd_parent_index = roulette_wheel_toss(cumulative_probabilities)
    return (fst_parent_index, snd_parent_index)
