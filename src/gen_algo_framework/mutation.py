from random import sample, random
from typing import List
from src.gen_algo_framework.genetic_algorithm import geneType


def swap_mutation(individual: List[geneType]) -> List[geneType]:
    '''
    Applies a swap mutation to a given individual. This mutation involves
    selecting two random positions in the individual's genome and swapping
    their values.

    Args:
        individual (List[geneType]): The individual genome to be mutated.

    Returns:
        List[geneType]: The mutated individual genome with two genes swapped.
    '''
    [i, j] = sample(list(range(len(individual))), 2)
    tmp = individual[i]
    individual[i] = individual[j]
    individual[j] = tmp
    return individual


def swap_mutation_population(population: List[List[geneType]],
                             options: dict) -> List[List[geneType]]:
    '''
    Applies swap mutations to a population of individuals. Each individual
    has a probability of being mutated. If mutated, the mutation may apply
    additional swaps depending on a secondary probability.

    Args:
        population (List[List[geneType]]): The population of individuals,
            where each individual is represented as a list of genes.
        options (dict): A dictionary containing mutation-related options:
            - 'mutation_proba': Probability of applying the mutation to an individual.
            - 'another_swap_p': Probability of applying additional swaps to the same individual.

    Returns:
        List[List[geneType]]: The population with mutations applied to some of the individuals.
    '''
    mutation_proba: float = options['mutation_proba']
    another_swap_proba: float = options['another_swap_p']

    for i in range(len(population)):
        if random() < mutation_proba:
            population[i] = swap_mutation(population[i])
            while random() < another_swap_proba:
                population[i] = swap_mutation(population[i])
    return population
