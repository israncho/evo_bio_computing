
from math import sqrt, isclose
from random import randint, uniform
from src.tsp.euclidean_tsp import build_weight_dict, euc_tsp_fitness, euclidean_distance, tour_distance
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
        tour_distance_f = tour_distance(fst_city, tour, weights)
        rectangular_tour_perimeter = 2 * height + 2 * base
        assert isclose(tour_distance_f, rectangular_tour_perimeter, rel_tol=1e-7)


def test_euc_tsp_fitness():
    berlin52 = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))
    population = []
    for _ in range(randint(25, 50)):
        population.append(berlin52['rest_of_cities'].copy())

    population_w_fitness = euc_tsp_fitness(population, berlin52)


    for i in range(1, len(population_w_fitness)):
        curr_f, curr_perm = population_w_fitness[i]
        prev_f, prev_perm = population_w_fitness[i - 1]
        assert curr_f == prev_f
        assert curr_perm == prev_perm


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
