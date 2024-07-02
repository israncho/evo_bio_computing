from functools import reduce
from heapq import nsmallest
from random import sample
from typing import Callable, Collection, List, Set, Tuple
from typing import Any, Collection, TypeVar

T = TypeVar('T', Collection, Any)   # type of the Genotype
geneType = TypeVar('geneType')      # type of the genes

def genetic_algorithm(population: Collection[Tuple[float, T]],
                      crossover: Callable[[Collection[Tuple[float, T]], int], Collection[T]],
                      mutation: Callable[[Collection[T]], Collection[T]],
                      fitness: Callable[[T], float],
                      selection: Callable[[Collection[Tuple[float, T]], Collection[Tuple[float, T]]], Collection[Tuple[float, T]]],
                      term_cond: Callable[[int, Collection[Tuple[float, T]]], bool],
                      offspring_expansion_factor: float = 2.0
                      ) -> Collection[Collection[Tuple[float, T]]]:
    '''
    Applies a genetic algorithm to evolve a population of genotypes.
    Returns:
        Collection[Collection[Tuple[float, T]]]: List of best solutions found in each generation.
    '''

    current_population = population
    best_solutions = []
    generation = 0
    while term_cond(generation, best_solutions):
        offspring_size = int(offspring_expansion_factor * len(current_population))
        offspring = crossover(current_population, offspring_size)
        offspring = mutation(offspring)   # Apply mutation to the next generation
        offspring = list(map(lambda x : (fitness(x), x), offspring))
        next_gen_population = selection(current_population, offspring)   # calculate next_population

        best_of_gen = nsmallest(7, next_gen_population)
        best_solutions.append(best_of_gen)

        generation += 1
        current_population = next_gen_population

    return best_solutions


def population(size: int, genes: Set[geneType]) -> List[List[geneType]]:
    '''
    Generates a population of individuals, where each individual is a list
    representing a chromosome composed of randomly sampled genes from a given set.
    Args:
        size (int): The number of individuals (chromosomes) in the population.
        genes (Set[geneType]): The set of genes to sample from for each individual.
    Returns:
        List[List[geneType]]: A list of lists, where each inner list represents
        an individual (chromosome) in the population. Each individual's chromosome
        contains genes sampled randomly from the provided set.
    '''
    gene_count = len(genes)
    genes_list = list(genes)
    _population = []
    for _ in range(size):
        individual = sample(genes_list, gene_count)
        _population.append(individual)
    return _population


def transform_to_min(population: Collection[Tuple[float, T]]) -> Collection[Tuple[float, T]]:
    '''
    Transforms a population's fitness values from a maximization problem to a minimization problem.
    This transformation ensures that higher fitness values become lower fitness values,
    facilitating the use of algorithms designed for minimization.
    Args:
        population (Collection[Tuple[float, T]]): A collection of individuals in the population,
                                                  where each individual is represented as a tuple
                                                  containing a fitness value and a genotype.
    Returns:
        Collection[Tuple[float, T]]: The transformed population with adjusted fitness values.
    '''
    max_fit = reduce(lambda _max, x: _max if _max > x[0] else x[0], population, -1)
    return list(map(lambda x: (max_fit - x[0] + 1e-6, x[1]), population))
