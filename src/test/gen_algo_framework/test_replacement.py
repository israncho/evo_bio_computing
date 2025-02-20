from random import randint, sample

from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.gen_algo_framework.replacement import full_generational_replacement
from src.gen_algo_framework.selection import cumulative_fitness


def test_full_generational_replacement():
    for _ in range(500):
        genes = set([randint(0, 50) for _ in range(randint(20, 50))])
        parents = generate_population_of_permutations(randint(20, 50), genes)
        children = generate_population_of_permutations(randint(20, 50), genes)
        assert full_generational_replacement(parents, children, 0, {}) == children