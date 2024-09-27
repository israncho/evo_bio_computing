'''Module with functions for the genetic algorithm.'''

from collections import defaultdict
from functools import reduce
from heapq import nlargest
from random import sample
from typing import Callable, List, Set, Tuple
from typing import Any, Collection, TypeVar


T = TypeVar('T', Collection, Any)   # type of the Genotype
GeneType = TypeVar('GeneType')      # type of the genes
Population = Collection[Tuple[float, T]] | Collection[T]


def genetic_algorithm(population: Population,
                      crossover: Callable[[Population, int, dict], Population],
                      mutation: Callable[[Population, dict], Population],
                      get_fitness: Callable[[Population, dict], Population],
                      replacement: Callable[[Population, Population, int, dict], Population],
                      term_cond: Callable[[int, Population], bool],
                      options_handler: Callable[[Population, dict], dict]
                      ) -> Collection[Population]:
    '''
    Applies a genetic algorithm to evolve a population of genotypes.
    This function is intended for maximization problems.
    Returns:
        Collection[Population]: List of best solutions found in each generation.
    '''

    current_population = population
    best_solutions: List[Population] = []
    generation = 0
    options = defaultdict(lambda : None)
    while term_cond(generation, best_solutions):
        options = options_handler(current_population, options)
        offspring_size, next_gen_pop_size = options['offspring_s'], options['next_gen_pop_s']
        offspring = crossover(current_population, offspring_size, options)
        offspring = mutation(offspring, options)   # Apply mutation to the next generation
        offspring = get_fitness(offspring, options)
        next_gen_population = replacement(current_population,
                                        offspring,
                                        next_gen_pop_size,
                                        options)   # calculate next_population

        best_of_gen = nlargest(7, next_gen_population)
        best_solutions.extend(best_of_gen)

        generation += 1
        current_population = next_gen_population

    return best_solutions


def generate_population(size: int, genes: Set[GeneType]) -> List[List[GeneType]]:
    '''
    Generates a population of individuals, where each individual is a list
    representing a chromosome composed of randomly sampled genes from a given set.
    Args:
        size (int):
            The number of individuals (chromosomes) in the population.

        genes (Set[GeneType]):
            The set of genes to sample from for each individual.

    Returns:
        List[List[GeneType]]:
            A list of lists, where each inner list represents an individual
            (chromosome) in the population. Each individual's chromosome
            contains genes sampled randomly from the provided set.
    '''
    gene_count = len(genes)
    genes_list = list(genes)
    _population = []
    for _ in range(size):
        individual = sample(genes_list, gene_count)
        _population.append(individual)
    return _population


def transform_to_max(population: Collection[Tuple[float, T]]) -> List[Tuple[float, T]]:
    '''
    Transforms a population's fitness values from a minimization problem to a maximization problem.
    This transformation ensures that lower fitness values become higher fitness values,
    facilitating the use of algorithms designed for maximization.
    Args:
        population (Collection[Tuple[float, T]]): A collection of individuals in the population,
                                                  where each individual is represented as a tuple
                                                  containing a fitness value and a genotype.
    Returns:
        Collection[Tuple[float, T]]: The transformed population with adjusted fitness values.
    '''
    max_fit = reduce(lambda _max, x: _max if _max > x[0] else x[0], population, -1)
    return list(map(lambda x: (max_fit - x[0] + 1e-6, x[1]), population))
