'''Module with continuous objective functions.'''

from typing import List, Tuple
from math import cos, inf, pi, exp, sqrt, e, sin

from src.continuous.binary_representation import decode_vector
from src.gen_algo_framework.genetic_algorithm import Population
from src.gen_algo_framework.population_utils import transform_to_max
from src.gen_algo_framework.selection import cumulative_fitness
from src.gen_algo_framework.diversity import diversity_avg_distance_bit_seq, entropy_bit_seq_population


def rastrigin(x: List[float], a: float = 10) -> float:
    # Optimal x = [0, ... , 0] ; f(x) = 0
    _sum = a * len(x)  # A * n
    for x_i in x:
        _sum += x_i**2 - a * cos(2 * pi * x_i)
    return _sum


def rosenbrock(x: List[float]) -> float:
    # Optimal x = [1, ... , 1] ; f(x) = 0
    n = len(x)
    _sum = 0
    for i in range(n - 1):
        _sum += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
    return _sum


def sphere(x: List[float]) -> float:
    # Optimal x = [0, ... , 0] ; f(x) = 0
    value = 0
    for v in x:
        value += v**2
    return value


def ackley(x: List[float], a=20, b=0.2, c=2 * pi) -> float:
    # Optimal x = [0, ... , 0] ; f(x) = 0
    squares = 0
    sumCosines = 0
    dimension = len(x)

    for v in x:
        squares += v**2
        sumCosines += cos(c * v)

    return (
        -a * exp(-b * sqrt(1 / dimension * squares))
        - exp(1 / dimension * sumCosines)
        + a
        + e
    )


def easom(x: List[float]) -> float:
    # Optimal x = [π, π] ; f(x) = -1
    return -cos(x[0]) * cos(x[1]) * exp(-(x[0] - pi) - (x[1] - pi))


def zakharov(x: List[float]) -> float:
    # Optimal x = [0, ... , 0] ; f(x) = 0
    squares = 0
    lineal = 0
    for i, xi in enumerate(x, start=1):
        squares += xi**2
        lineal += 0.5 * i * xi

    return squares + lineal**2 + lineal**4


def michalewicz(x: List[float], steepness=10) -> float:
    # Optimal at d = 2; x = [2.20, 1.57] ; f(x) = -1.8013
    # Optimal at d = 5 ; f(x) = -4.687658
    # Optimal at d = 10 ; f(x) = -9.66015
    summation = 0
    for i, xi in enumerate(x, start=1):
        summation += sin(xi) * sin((i * xi**2) / pi) ** (2 * steepness)

    return -summation


def hyper_ellipsoid(x: List[float]) -> float:
    # Optimal x = [0, ... , 0] ; f(x) = 0
    dimension = len(x)
    summation = 0

    for i in range(dimension):
        for j in range(i):
            summation += x[j]**2

    return summation


def griewank(x: List[float]) -> float:
    _sum = 0
    prod = 1
    for i, x_i in enumerate(x, start=1):
        _sum += x_i**2
        prod *= cos(x_i / sqrt(i))
    return 1 + (_sum / 4000) - prod


all_funcs = {"rastrigin": rastrigin, "rosenbrock": rosenbrock,
             "zakharov": zakharov, "michalewicz": michalewicz,
             "sphere": sphere, "hyper_ellipsoid": hyper_ellipsoid,
             "ackley": ackley, "easom": easom,
             "griewank": griewank}


def compute_vectors_fitness(population: Population[List[int]],
                             options: dict) -> Population[List[int]]:

    f = options['f']
    v_n_bits = options['v_n_bits']
    v_intervals = options['v_intervals']
    population_fitness_sum = 0

    gen_best_fitness = inf

    for i, individual in enumerate(population):
        decoded_individual = decode_vector(individual, v_n_bits, v_intervals)
        individual_fitness = f(decoded_individual)
        population[i] = individual_fitness, individual # pyright: ignore
        population_fitness_sum += individual_fitness

        if individual_fitness < gen_best_fitness:
            gen_best_fitness = individual_fitness

        if individual_fitness < options['current_best'][0]:
            options['current_best'] = individual_fitness, individual

    options['gen_fittest_fitness'] = gen_best_fitness

    return population # pyright: ignore


def simple_c_f_options_handler(population: Population[List[int]],
                               options: dict,
                               init: bool = False,
                               offspring_s: int = 100,
                               next_gen_pop_s: int = 100,
                               mutation_proba = 0.01,
                               f = sphere,
                               n_crossover_points: int = 1,
                               v_n_bits = None,
                               v_intervals = None,
                               minimization = True,
                               calc_generational_entropy = False,
                               distance_measure = None
                               ) -> dict:
    if init:
        options['population_fit_avgs'] = []
        options['offspring_s'] = offspring_s
        options['next_gen_pop_s'] = next_gen_pop_s
        options['mutation_proba'] = mutation_proba
        options['current_best'] = inf, None
        options['gen_fittest_fitness'] = []
        options['f'] = f
        options['n_points'] = n_crossover_points
        if v_n_bits is None:
            v_n_bits = [20, 20]
            v_intervals = [(-15.0, 15.0), (-15.0, 15.0)]
        options['v_n_bits'] = v_n_bits
        options['v_intervals'] = v_intervals
        options['minimization'] = minimization
        population = compute_vectors_fitness(population, options) # pyright: ignore

        if calc_generational_entropy:
            options['pop_entropy'] = []
        else:
            options['pop_entropy'] = None

        if distance_measure is not None:
            options['pop_diversity'] = []
            options['distance_measure'] = distance_measure
        else:
            options['pop_diversity'] = None


    if options['pop_diversity'] is not None:
        options['pop_diversity'].append(
            diversity_avg_distance_bit_seq(population,
                                           options['distance_measure']))

    if options['pop_entropy'] is not None:
        options['pop_entropy'].append(entropy_bit_seq_population(population))

    pop_only_fitness_values = list(map(lambda x: (x[0], None), population))
    pop_only_fitness_values = transform_to_max(pop_only_fitness_values)
    options['c_fitness_l'] = cumulative_fitness(pop_only_fitness_values) # pyright: ignore
    return options
