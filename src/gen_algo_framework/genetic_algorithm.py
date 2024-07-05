from functools import reduce
from heapq import nsmallest
from random import sample
from typing import Callable, Collection, List, Set, Tuple, Union
from typing import Any, Collection, TypeVar


T = TypeVar('T', Collection, Any)   # type of the Genotype
geneType = TypeVar('geneType')      # type of the genes
Population = Union[Collection[Tuple[float, T]], Collection[T]]


def genetic_algorithm(population: Population,
                      crossover: Callable[[Population, int, Tuple], Tuple[Population, Tuple]],
                      mutation: Callable[[Population, Tuple], Tuple[Population, Tuple]],
                      get_fitness: Callable[[Population, Tuple], Tuple[Population, Tuple]],
                      selection: Callable[[Population, Population, Tuple], Tuple[Population, Tuple]],
                      term_cond: Callable[[int, Population], bool],
                      options_handler: Callable[[Population], Tuple],
                      offspring_expansion_factor: float = 2.0
                      ) -> Collection[Population]:
    '''
    Applies a genetic algorithm to evolve a population of genotypes.
    Returns:
        Collection[Population]: List of best solutions found in each generation.
    '''

    current_population = population
    options = options_handler(current_population)
    best_solutions = []
    generation = 0
    while term_cond(generation, best_solutions):
        offspring_size = int(offspring_expansion_factor * len(current_population))
        offspring, options = crossover(current_population, offspring_size, options)
        offspring, options = mutation(offspring, options)   # Apply mutation to the next generation
        offspring, options = get_fitness(offspring, options)
        next_gen_population, options = selection(current_population, offspring, options)   # calculate next_population

        best_of_gen = nsmallest(7, next_gen_population)
        best_solutions.extend(best_of_gen)

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
