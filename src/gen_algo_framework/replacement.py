'''Module with functions that implement replacement operators
for the genetic algorithm.'''

from typing import List, Tuple
from src.gen_algo_framework.genetic_algorithm import T, Population
from src.gen_algo_framework.selection import cumulative_fitness, roulette_wheel_toss, remove_from_fitness_list


def full_generational_replacement(_: Population,
                                  offspring: Population,
                                  __: int,
                                  ___: dict) -> Population:
    return offspring


def full_gen_replacement_elitist(_: List[Tuple[float, T]],
                                 offspring: List[Tuple[float, T]],
                                 __: int,
                                 options: dict) -> List[Tuple[float, T]]:

    if options['current_best'][0] != options['gen_best']:
        offspring.pop()
        offspring.append(options['current_best'])
        options['gen_best'].pop()
        options['gen_best'].append(options['current_best'][0])

    return offspring


def roulette_gen_replacement(current_population: List[Tuple[float, T]],
                                offspring: List[Tuple[float, T]],
                                next_gen_size: int,
                                options: dict) -> List[Tuple[float, T]]:
    '''
    Performs the next generation selection using a roulette wheel mechanism.
    This functions modifies the current_population and the options argument.
    This function is intended for maximization problems.
    Args:
        current_population (List[Tuple[float, T]]): The current population,
            where each individual is a tuple of fitness score and individual.
        offspring (List[Tuple[float, T]]): The new offspring generated from
            the current population.
        next_gen_size (int): The desired size of the next generation.
        options (dict): A dictionary with the cumulative fitness list
            from the current_population argument, associated with the
            key \'c_fitness_l\' .
    Returns:
        List[Tuple[float, T]]: The selected next generation population.
    '''

    cumulative_fitness_l = options['c_fitness_l']
    curr_total_f = cumulative_fitness_l[-1]
    current_population.extend(offspring)

    # calculate offspring cumulative list and total fitness
    offspring_c_list  = cumulative_fitness(offspring, curr_total_f)
    cumulative_fitness_l.extend(offspring_c_list)

    next_gen: List[Tuple[float, T]] = []
    for _ in range(next_gen_size):
        index = roulette_wheel_toss(cumulative_fitness_l)
        individual = current_population[index]
        next_gen.append(individual)

        # remove from pop and cumulative list
        current_population.pop(index)
        cumulative_fitness_l = remove_from_fitness_list(index,
                                                        individual[0],
                                                        cumulative_fitness_l)

    return next_gen

all_replacement_funcs = {'full_generational_replacement': full_generational_replacement,
                         'full_gen_replacement_elitist': full_gen_replacement_elitist}