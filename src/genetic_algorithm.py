from heapq import nsmallest
from typing import Callable, Iterable, TypeVar

T = TypeVar('T')    # type of the Genotype

def genetic_algorithm(population: Iterable[tuple[float, T]],
                      crossover: Callable[[Iterable[tuple[float, T]]], Iterable[T]],
                      mutation: Callable[[Iterable[T]], Iterable[T]],
                      fitness: Callable[[T], float],
                      selection: Callable[[Iterable[tuple[float, T]], Iterable[tuple[float, T]]], Iterable[tuple[float, T]]],
                      term_cond: Callable[[int, Iterable[tuple[float, T]]], bool]
                      ) -> Iterable[Iterable[tuple[float, T]]]:
    '''
    Applies a genetic algorithm to evolve a population of genotypes.
    Returns:
        Iterable[Iterable[tuple[float, T]]]: List of best solutions found in each generation.
    '''

    current_population = population
    best_solutions = []
    generation = 0
    while term_cond(generation, best_solutions):
        next_gen = crossover(current_population)
        next_gen = mutation(next_gen)   # Apply mutation to the next generation
        next_gen = list(map(lambda x : (fitness(x), x), next_gen))
        next_gen_population = selection(current_population, next_gen)   # calculate next_population

        best_of_gen = nsmallest(7, next_gen_population)
        best_solutions.append(best_of_gen)

        generation += 1
        current_population = next_gen_population

    return best_solutions
