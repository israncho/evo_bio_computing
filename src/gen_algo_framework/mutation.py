'''Module with functions that implement mutation operators
for the genetic algorithm.'''

from random import randint, sample, random
from typing import Callable, List, TypeVar
from src.gen_algo_framework.genetic_algorithm import GeneType

A = TypeVar('A')

def mutate_population(mutation_func: Callable[[A], A],
                      population: List[A],
                      mutation_proba: float) -> List[A]:

    for i, individual in enumerate(population):
        if random() < mutation_proba:
            population[i] = mutation_func(individual)
    return population


def swap_mutation(individual: List[GeneType]) -> List[GeneType]:
    '''
    Applies a swap mutation to a given individual. This mutation involves
    selecting two random positions in the individual's genome and swapping
    their values.

    Args:
        individual (List[GeneType]): The individual genome to be mutated.

    Returns:
        List[GeneType]: The mutated individual genome with two genes swapped.
    '''
    [i, j] = sample(list(range(len(individual))), 2)
    tmp = individual[i]
    individual[i] = individual[j]
    individual[j] = tmp
    return individual


def swap_mutation_population(population: List[List[GeneType]],
                             options: dict) -> List[List[GeneType]]:
    '''
    Applies swap mutations to a population of individuals. Each individual
    has a probability of being mutated. If mutated, the mutation may apply
    additional swaps depending on a secondary probability.

    Args:
        population (List[List[GeneType]]): The population of individuals,
            where each individual is represented as a list of genes.
        options (dict): A dictionary containing mutation-related options:
            - 'mutation_proba': Probability of applying the mutation
                to an individual.
            - 'another_swap_p': Probability of applying additional swaps
                to the same individual.

    Returns:
        List[List[GeneType]]: The population with mutations applied to some
            of the individuals.
    '''
    mutation_proba: float = options['mutation_proba']
    return mutate_population(swap_mutation, population, mutation_proba)


def bit_flip_mutation(individual: List[int]) -> List[int]:
    i = randint(0, len(individual) - 1)
    individual[i] = individual[i] ^ 1
    return individual


def bit_flip_mutation_population(population: List[List[int]],
                                 options: dict) -> List[List[int]]:

    mutation_proba: float = options['mutation_proba']
    return mutate_population(bit_flip_mutation, population, mutation_proba)
