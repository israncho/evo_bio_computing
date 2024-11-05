
from math import inf, sqrt, isclose
from random import randint, uniform
from src.gen_algo_framework.genetic_algorithm import standard_fitness_computing
from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.tsp.euclidean_tsp import build_weight_dict, euclidean_distance, tour_distance
from src.utils.input_output import parse_tsp_data, read_file


def __random_4d_point():
    return (uniform(-100, 100),
            uniform(-100, 100),
            uniform(-100, 100),
            uniform(-100, 100))


def test_euclidean_distance():
    for _ in range(100):
        u, v = __random_4d_point(), __random_4d_point()
        eucd = sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2
                    + (u[2] - v[2])**2 + (u[3] - v[3])**2)
        assert eucd == euclidean_distance(u, v)


def test_tour_distance():
    for _ in range(50):
        # generate rectangular tour
        tour = [(0.0, 0.0)]
        # build base
        for _ in range(randint(15, 50)):
            tour.append((tour[-1][0] + uniform(5, 40), 0.0))

        base = tour[-1][0]
        # build ceiling
        height = uniform(20, 50)
        ceil = list(map(lambda x : (x[0], x[1] + height), tour))
        ceil = reversed(ceil)
        tour.extend(ceil)

        fst_city = tour.pop(0)

        weights = build_weight_dict(fst_city, tour)
        tour_distance_f = tour_distance(tour, {'fst_city': fst_city, 'weights': weights})
        rectangular_tour_perimeter = 2 * height + 2 * base
        assert isclose(tour_distance_f, rectangular_tour_perimeter, rel_tol=1e-7)


def test_standard_fitness_computing_for_euc_tsp():
    berlin52 = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))
    berlin52['population_fit_avgs'] = []
    berlin52['current_best'] = inf, None
    berlin52['gen_fittest_fitness'] = []
    berlin52['f'] = tour_distance

    for _ in range(100):
        population = generate_population_of_permutations(20, berlin52['rest_of_cities'])
        population = standard_fitness_computing(population, berlin52) # pyright: ignore

        pop_untransformed_f_sum = 0
        for fitness, tour in population:
            recalc_f = tour_distance(tour, berlin52) # pyright: ignore
            pop_untransformed_f_sum += recalc_f
            assert fitness == recalc_f

        assert berlin52['population_fit_avgs'][-1] == pop_untransformed_f_sum / len(population)


def test_build_weight_dict():
    berlin52 = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))
    cities = berlin52['rest_of_cities'].copy()
    cities.append(berlin52['fst_city'])
    size = len(cities)
    for i in range(size):
        for j in range(i + 1, size):
            u, v = cities[i], cities[j]
            eucd = euclidean_distance(u, v)
            assert berlin52['weights'][(u, v)] == eucd
            assert berlin52['weights'][(v, u)] == eucd

    cities.pop()
