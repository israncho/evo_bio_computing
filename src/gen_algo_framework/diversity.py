'''
Module with functions to measure the diversity of a
population.
'''

from math import log
from itertools import islice
from typing import List, Callable
from src.gen_algo_framework.genetic_algorithm import Population


def hamming_distance(bit_seq1: List[int],
                     bit_seq2: List[int]) -> int:

    '''
    Calculates the Hamming distance between two binary sequences
    of equal length.
    Args:
        bit_seq1 (List[int]): The first binary sequence.
        bit_seq2 (List[int]): The second binary sequence, must be
            of the same length as bit_seq1.
    Returns:
        int: The number of differing bits between the two sequences.
    Raises:
        AssertionError: If the two sequences are not of the
            same length.
    '''
    assert len(bit_seq1) == len(bit_seq2)

    diffs = 0
    for bit_from_seq1, bit_from_seq2 in zip(bit_seq1, bit_seq2):
        if bit_from_seq1 != bit_from_seq2:
            diffs += 1
    return diffs


def jaccard_distance(bit_seq1: List[int],
                     bit_seq2: List[int]) -> float:
    '''
    Computes the Jaccard distance between two binary sequences
    of equal length.
    Args:
        bit_seq1 (List[int]): The first binary sequence.
        bit_seq2 (List[int]): The second binary sequence, must have
            the same length as bit_seq1.
    Returns:
        float: The Jaccard distance, a measure of dissimilarity
            between the two sequences.
    Raises:
        AssertionError: If the two sequences are not of the same
            length or are empty.
    '''
    assert len(bit_seq1) == len(bit_seq2)
    assert len(bit_seq1) > 0

    set_a = set()
    set_b = set()

    for i, (bit_s_1, bit_s_2) in enumerate(zip(bit_seq1, bit_seq2)):
        if bit_s_1 == 1:
            set_a.add(i)
        if bit_s_2 == 1:
            set_b.add(i)

    a_union_b = set_a.union(set_b)
    a_intersect_b = set_a.intersection(set_b)
    return (len(a_union_b) - len(a_intersect_b)) / len(a_union_b)


def diversity_avg_distance_bit_seq(population: Population,
                                   distance: Callable) -> float:
    '''
    Computes the diversity by calculating the average distance
    between individuals in a population.
    Args:
        population (Population): A collection of binary sequences
            representing the individuals in the population.
        distance (Callable): A function that takes two binary
            sequences and returns a numerical distance measure
            between them.
    Returns:
        float: The average distance between all unique pairs of
            individuals in the population, indicating the diversity
            of the population.
    '''
    # Population = MutableSequence[Tuple[float, T]] | MutableSequence[T]

    n = len(population)
    if n <= 1:
        return 0

    total_distance = 0
    for i, (_, bit_seq_i) in enumerate(population):
        for (_, bit_seq_j) in islice(population, i + 1, None):
            total_distance += distance(bit_seq_i, bit_seq_j)

    total_distance /= (n *(n - 1)) * 0.5
    return total_distance


def entropy_bit_seq_population(population: Population) -> float:
    '''
    Calculate the average entropy of each gene in a population
    of binary sequences.
    Args:
        population (Population): A sequence of tuples, where
            each tuple contains a fitness value and a binary sequence.
    Returns:
        float: The average entropy across all genes in the population.
    '''
    # Population = MutableSequence[Tuple[float, T]] | MutableSequence[T]
    n = len(population)

    assert n >= 2

    n_genes = len(population[0][1])
    frequencies_ones = [0] * n_genes
    for _, bit_seq in population:
        for i, bit in enumerate(bit_seq):
            frequencies_ones[i] += bit

    entropy_of_gene = [0.0] * n_genes

    for i in range(n_genes):
        p_1 = frequencies_ones[i] / n
        p_0 = 1 - p_1
        if p_1 not in (0, 1): # checking p_1 is not 1 nor 0
            entropy_of_gene[i] = -(p_1 * log(p_1) + p_0 * log(p_0))

    return sum(entropy_of_gene) / n_genes

all_distance_measures = {'hamming_distance': hamming_distance,
                          'jaccard_distance': jaccard_distance}
