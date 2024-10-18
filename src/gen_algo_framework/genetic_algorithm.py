'''Module with functions for the genetic algorithm.'''

from typing import Callable, MutableSequence, MutableSet, Tuple
from typing import TypeVar, List


T = TypeVar('T', MutableSequence, MutableSet)   # type of the Genotype
GeneType = TypeVar('GeneType')      # type of the genes
Population = MutableSequence[Tuple[float, T]] | MutableSequence[T]


def genetic_algorithm(population: Population,
                      crossover: Callable[[Population, int, dict], Population],
                      mutation: Callable[[Population, dict], Population],
                      get_fitness: Callable[[Population, dict], Population],
                      replacement: Callable[[Population, Population, int, dict], Population],
                      term_cond: Callable[[int, Population], bool],
                      options_handler: Callable[[Population, dict], dict],
                      options: dict
                      ) -> List[Population]:
    '''
    Applies a genetic algorithm to evolve a population of genotypes.
    This function is intended for maximization problems.
    Returns:
        Collection[Population]: List of best solutions found in each generation.
    '''

    current_population = population
    best_solutions: Population = []
    generation = 0
    while term_cond(generation, best_solutions):
        options = options_handler(current_population, options)

        best_solutions.append(options['current_best'])

        offspring_size, next_gen_pop_size = options['offspring_s'], options['next_gen_pop_s']
        offspring = crossover(current_population, offspring_size, options)
        offspring = mutation(offspring, options)   # Apply mutation to the next generation
        offspring = get_fitness(offspring, options)
        next_gen_population = replacement(current_population,
                                        offspring,
                                        next_gen_pop_size,
                                        options)   # calculate next_population


        generation += 1
        current_population = next_gen_population
    
    best_solutions.append(options['current_best'])

    return best_solutions
