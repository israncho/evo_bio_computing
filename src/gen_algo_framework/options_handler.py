'''Module with handler functions for the options of
the genetic algorithm..'''

from typing import List, Tuple
from src.gen_algo_framework.genetic_algorithm import T, Population
from src.gen_algo_framework.selection import cumulative_fitness


def minimum_options_handler(current_population: Population,
                            options: dict) -> dict:
    '''
    Configures the minimum required options for the genetic
    algorithm. This function ensures that all essential options
    are set to their appropriate default values if they were
    not provided.
    Args:
        current_population (Population): The current population
            of genotypes.
        options (dict): A dictionary containing options for the
            algorithm, where some values may initially be `None`.
    Returns:
        dict: The updated dictionary of options with default
            values set for any missing options.
    '''
    if options['initial_population'] == None:   # first gen/iteration
        options['initial_population'] = len(current_population)

    if options['mutation_proba'] == None:
        options['mutation_proba'] = 1 / options['initial_population']

    if options['another_swap_p'] == None:
        options['another_swap_p'] = options['mutation_proba']

    if options['offspring_s'] == None:
        options['offspring_s'] = options['initial_population']

    if options['next_gen_pop_s'] == None:
        options['next_gen_pop_s'] = options['initial_population']

    return options


def roulette_wheel_based_options(current_population: List[Tuple[float, T]],
                                 options: dict) -> dict:
    '''
    Prepares options for a genetic algorithm that specifically uses a
    roulette wheel selection algorithm. This function handles setting
    up default values for options and calculates the cumulative fitness
    of the current population.
    Args:
        current_population (List[Tuple[float, T]]): The current population,
            where each element is a tuple containing the fitness value and the
            genotype.
        options (dict): A dictionary containing options for the algorithm.

    Returns:
        dict: The updated dictionary of options with cumulative fitness
            calculated and added.
    Notes:
        - This function calls `minimum_options_handler` to set the minimum
            required options.
        - 'c_fitness_l': A list representing the cumulative fitness of the
            current population, which is essential for the roulette wheel
            selection process.
    '''
    options = minimum_options_handler(current_population, options)
    options['c_fitness_l'] = cumulative_fitness(current_population)
    return options
