'''Module with continuous objective functions.'''

from typing import List, Tuple
from math import cos, inf, pi, exp, sqrt, e, sin

from src.continuous.binary_representation import decode_vector
from src.gen_algo_framework.genetic_algorithm import Population
from src.gen_algo_framework.population_utils import transform_to_max
from src.gen_algo_framework.selection import cumulative_fitness


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


def c_f_fitness_maximization(population: List[List[int]],
                             options: dict) -> List[Tuple[float, List[int]]]:

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

    options['population_fit_avgs'].append(population_fitness_sum / len(population))
    options['gen_best'].append(gen_best_fitness)
    population = transform_to_max(population) # pyright: ignore

    return population # pyright: ignore


def simple_c_f_options_handler(population: Population,
                               options: dict,
                               init: bool = False,
                               offspring_s: int = 100,
                               next_gen_pop_s: int = 100,
                               mutation_proba = 0.01,
                               f = sphere,
                               n_crossover_points: int = 1,
                               v_n_bits = None,
                               v_intervals = None
                               ) -> dict:
    if init:
        options['population_fit_avgs'] = []
        options['offspring_s'] = offspring_s
        options['next_gen_pop_s'] = next_gen_pop_s
        options['mutation_proba'] = mutation_proba
        options['current_best'] = inf, None
        options['gen_best'] = []
        options['f'] = f
        options['n_points'] = n_crossover_points
        if v_n_bits is None:
            v_n_bits = [20, 20]
            v_intervals = [(-15.0, 15.0), (-15.0, 15.0)]
        options['v_n_bits'] = v_n_bits
        options['v_intervals'] = v_intervals
        population = c_f_fitness_maximization(population, options) # pyright: ignore

    options['c_fitness_l'] = cumulative_fitness(population) # pyright: ignore
    return options
