from heapq import nsmallest
from typing import Callable, Collection, Tuple
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

