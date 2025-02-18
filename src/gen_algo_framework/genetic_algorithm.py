'''Module with functions for the genetic algorithm.'''

from math import inf
from typing import Callable, MutableSequence, MutableSet, Tuple
from typing import TypeVar, List


T = TypeVar('T', MutableSequence, MutableSet)   # type of the Genotype
Population = List[Tuple[float, T]] | List[T]


def genetic_algorithm(population: Population[T],
                      crossover: Callable[[Population[T], int, dict], Population[T]],
                      mutation: Callable[[Population[T], dict], Population[T]],
                      get_fitness: Callable[[Population[T], dict], Population[T]],
                      replacement: Callable[[Population[T], Population[T], int, dict], Population[T]],
                      term_cond: Callable[[int, Population[T]], bool],
                      options_handler: Callable[[Population[T], dict], dict],
                      options: dict
                      ) -> List[Population[T]]:
    '''
    Applies a genetic algorithm to evolve a population of genotypes.
    Very likely to add or change items of the options dictionary.
    Returns:
        List[Population]: List of best solutions found in each generation.
    '''

    current_population = population
    best_solutions: List[T] = []
    generation = 0
    while term_cond(generation, best_solutions):
        options = options_handler(current_population, options)

        best_solutions.append(options['current_best'])

        offspring_size, next_gen_pop_size = options['offspring_s'], options['next_gen_pop_s']
        #indexes_selected_parents = selection(current_population, offspring_size, options)
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


def standard_fitness_computing(population: Population[T],
                               options: dict) -> Population[T]:
    '''
    Computes the fitness of each individual in the population.
    Args:
        population (Population[T]): The current population.
        options (dict): A dictionary containing the following keys:
            - 'f' (Callable[[T, dict], float]): The fitness function
                to evaluate each individual in the population.
            - 'current_best' (Tuple[float, T]): A tuple representing
                the best fitness and individual seen so far.
            - 'population_fit_avgs' (list[float]): A list that will store
                the average population fitness for each generation.
            - 'gen_fittest_fitness' (list[float]): A list that will store
                the best fitness in each generation.
    Returns:
        Population[T]: The population where each individual is now
        paired with its corresponding fitness value.
    '''

    population_fitness_sum = 0
    f: Callable[[T, dict], float] = options['f']
    gen_best_fitness = inf

    for i, individual in enumerate(population):
        individuals_fitness = f(individual, options) # pyright: ignore
        population_fitness_sum += individuals_fitness
        population[i] = individuals_fitness, individual # pyright: ignore

        if individuals_fitness < gen_best_fitness:
            gen_best_fitness = individuals_fitness

    options['population_fit_avgs'].append(population_fitness_sum / len(population))
    options['gen_fittest_fitness'].append(gen_best_fitness)
    return population
