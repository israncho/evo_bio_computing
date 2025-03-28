'''Module with functions to handle population
generation and others.'''

from math import inf
from random import sample
from typing import Set, List, Tuple
from src.continuous.binary_representation import generate_random_bit_vector
from src.gen_algo_framework.genetic_algorithm import T, Population

def generate_population_of_permutations(size: int,
                                        genes: Set) -> List[List]:
    '''
    Generates a population of individuals, where each individual
    is a listrepresenting a chromosome composed of randomly
    sampled genes from a given set.
    Args:
        size (int):
            The number of individuals (chromosomes) in the population.
        genes (Set):
            The set of genes to sample from for each individual.
    Returns:
        List[List]:
            A list of lists, where each inner list represents an
            individual (chromosome) in the population. Each
            individual's chromosome contains genes sampled randomly
            from the provided set.
    '''
    gene_count = len(genes)
    genes_list = list(genes)
    _population = []
    for _ in range(size):
        individual = sample(genes_list, gene_count)
        _population.append(individual)
    return _population


def generate_population_of_bit_vectors(size: int,
                                       v_n_bits: List[int]) -> List[List[int]]:
    return [generate_random_bit_vector(v_n_bits) for _ in range(size)]


def transform_to_max(population: Population[T]) -> Population[T]:
    '''
    Transforms a population's fitness values from a minimization
    problem to a maximization problem. This transformation ensures that
    lower fitness values become higher fitness values, facilitating the
    use of algorithms designed for maximization.
    Args:
        population (List[Tuple[float, T]]): A list of
            individuals in the population, where each individual is
            represented as a tuple containing a fitness value and a genotype.
    Returns:
        Collection[Tuple[float, T]]: The transformed population with adjusted
        fitness values (modifies the population given as argument and returns it).
    '''
    max_fit = -inf
    for fitness, _ in population:
        if fitness > max_fit:
            max_fit = fitness

    for i, (fitness, individual) in enumerate(population):
        population[i] = (max_fit - fitness + 1e-6, individual)

    return population
