from random import sample, random
from typing import List
from src.gen_algo_framework.genetic_algorithm import geneType


def swap_mutation(individual: List[geneType]) -> List[geneType]:
    [i, j] = sample(list(range(len(individual))), 2)
    tmp = individual[i]
    individual[i] = individual[j]
    individual[j] = tmp
    return individual


def swap_mutation_population(population: List[List[geneType]],
                             options: dict) -> List[List[geneType]]:
    mutation_proba: float = options['mutation_proba']
    another_swap_proba: float = options['another_swap_p']

    for i in range(len(population)):
        if random() < mutation_proba:
            population[i] = swap_mutation(population[i])
            while random() < another_swap_proba:
                population[i] = swap_mutation(population[i])
    return population
