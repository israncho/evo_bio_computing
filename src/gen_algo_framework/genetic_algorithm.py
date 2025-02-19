'''Module with functions for the genetic algorithm.'''

from math import inf
from random import random
from typing import Callable, MutableSequence, MutableSet, Tuple
from typing import TypeVar, List


T = TypeVar('T', MutableSequence, MutableSet)   # type of the Genotype
Population = List[Tuple[float, T]] | List[T]


def genetic_algorithm(population: Population[T],
                      selection: Callable[[Population[T], int, dict], List[Tuple[int, int]]],
                      crossover: Callable[[T, T, dict], Tuple[T, T]],
                      mutation: Callable[[T], T],
                      fitness_f: Callable[[T, dict], float],
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

    current_population = population_fitness_computing(fitness_f, population, options)
    best_solutions: List[T] = []
    generation = 0
    while term_cond(generation, best_solutions):
        options = options_handler(current_population, options)

        best_solutions.append(options['current_best'])

        offspring_size, next_gen_pop_size = options['offspring_s'], options['next_gen_pop_s']
        #indexes_selected_parents = selection(current_population, offspring_size, options)
        #offspring = population_crossover(current_population, indexes_selected_parents, offspring_size, crossover, options)
        #offspring = mutate_population(mutation, offspring, options)
        #offspring = population_fitness_computing(fitness_f, offspring, options)
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


def population_fitness_computing(fitness_f: Callable[[T, dict], float],
                                 population: Population[T],
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
    gen_best_fitness = inf

    for i, individual in enumerate(population):
        individuals_fitness = fitness_f(individual, options) # pyright: ignore
        population_fitness_sum += individuals_fitness
        population[i] = individuals_fitness, individual # pyright: ignore

        if individuals_fitness < gen_best_fitness:
            gen_best_fitness = individuals_fitness

    options['population_fit_avgs'].append(population_fitness_sum / len(population))
    options['gen_fittest_fitness'].append(gen_best_fitness)
    return population


def population_crossover(population: Population[T],
                         indexes_selected_parents: List[Tuple[int, int]],
                         offspring_size: int,
                         crossover: Callable[[T, T, dict], Tuple[T, T]],
                         options: dict) -> Population[T]:
    '''
    Creates a new generation of offspring using the given crossover operator.
    Args:
        population (Population[T]):
            The current population, where each element is a tuple containing
            the fitness value and the chromosome.
        indexes_selected_parents (List[Tuple[int, int]]): indexes of the selected
            parents.
        crossover (Callable[[T, T, dict], Tuple[T, T]]): crossover operator as
            a function.
        offspring_size (int):
            The desired size of the new generation.
        options (dict): A dictionary with aditional arguments that
            the crossover operator may use.
    Returns:
        List[List]: A list of new individuals representing the offspring.
    '''
    new_gen = []
    for i, j in indexes_selected_parents:
        parent1 = population[i]
        parent2 = population[j]
        child1, child2 = crossover(parent1, parent2, options)
        new_gen.append(child1)
        if len(new_gen) < offspring_size:
            new_gen.append(child2)
    #assert len(new_gen) == offspring_size
    return new_gen


def mutate_population(mutation_func: Callable[[T], T],
                      population: Population[T],
                      options: dict) -> Population[T]:
    '''
    Applies mutation to the population using the given mutation function.
    Args:
        mutation_func (Callable[[T], T]):
            The mutation function that takes an individual and returns a mutated version of it.
        population (Population[T]):
            The current population, where each element is an individual.
        options (dict):
            A dictionary containing additional arguments for the mutation process.
            Expected to contain the key 'mutation_proba' which specifies the probability
            of mutation for each individual.
    Returns:
        Population[T]:
            The population after applying the mutation operator.
    '''
    mutation_proba = options['mutation_proba']
    for i, individual in enumerate(population):
        if random() < mutation_proba:
            population[i] = mutation_func(individual)
    return population