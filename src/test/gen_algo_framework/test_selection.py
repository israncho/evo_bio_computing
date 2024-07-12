from random import randint, sample
from typing import List, Optional
from src.gen_algo_framework.selection import cumulative_fitness, remove_from_fitness_list, roulette_next_gen_selection, roulette_wheel_selection_two_parents, roulette_wheel_toss


def __random_c_list():
    _population = [None] * randint(20, 60)
    _population = list(map(lambda x: (float(randint(1 , 1000)), x), _population))
    c_list, total_f = cumulative_fitness(_population)
    return c_list, total_f, _population


def test_cumulative_fitness(c_list_to_test: Optional[List[float]] = None):
    tests = 5000

    c_list: List[float] = []
    total_f = 0

    if c_list_to_test != None:
        tests = 1
        c_list = c_list_to_test

    for _ in range(tests):
        if c_list_to_test == None:
            c_list, total_f, _ = __random_c_list()

        for i in range(1, len(c_list)):
            assert c_list[i - 1] < c_list[i], f'List not strictly increasing at index {i}'
        assert 0 < c_list[0], f'First element out of range: {c_list[0]}'

        if c_list_to_test == None:
            assert c_list[-1] == total_f


def test_roulette_wheel_toss():
    for _ in range(10000):
        c_list, total_f, _ = __random_c_list()
        i = roulette_wheel_toss(c_list, total_f)
        assert 0 <= i and i < len(c_list), f'Index out of range: {i}'

    index_tosses = {0: 0, 1: 0, 2: 0, 3: 0}
    fixed_c_list = [25.0, 50.0, 75.0, 100.0]
    tosses = 20000

    for _ in range(tosses):
        index_selected = roulette_wheel_toss(fixed_c_list, 100.0)
        index_tosses[index_selected] += 1

    for val in index_tosses.values():
        election_rate = val / tosses
        assert 0.24 < election_rate and election_rate < 0.26, f'Election rate out of range: {election_rate}'


def test_roulette_wheel_selection_two_parents():
    for _ in range(5000):
        c_list, total_f, _ = __random_c_list()
        i, j = roulette_wheel_selection_two_parents(c_list, total_f)
        assert i != j, f'Selected same index for both parents: {i}'
        assert 0 <= i and i < len(c_list), f'Index i out of range: {i}'
        assert 0 <= j and j < len(c_list), f'Index j out of range: {j}'


def test_remove_from_fitness_list():
    for _ in range(1000):
        c_list, total_f, _popu = __random_c_list()

        for _ in range(randint(0, len(c_list) // 2)):
            index = randint(0, len(c_list) - 1)
            individual_fitness = _popu[index][0]

            c_list, total_f = remove_from_fitness_list(index, individual_fitness, c_list, total_f)

            test_cumulative_fitness(c_list)

            _popu.pop(index)
            recalc_c_list, recalc_f = cumulative_fitness(_popu)
            assert recalc_c_list == c_list
            assert recalc_f == total_f


def test_roulette_next_gen_selection():
    for _ in range(1000):
        fittest_individuals = [None] * randint(10, 15)
        fittest_individuals = list(map(lambda x: (float(randint(10000 , 100000)), x), fittest_individuals))

        unfit_individuals = [None] * randint(35, 60)
        unfit_individuals = list(map(lambda x: (float(randint(10 , 50)), x), unfit_individuals))

        _population = sample(fittest_individuals + unfit_individuals,
                             len(fittest_individuals) + len(unfit_individuals))

        curr_population = _population[:len(_population) // 2]
        offspring = _population[len(_population) // 2:]

        cumulative_f_l, total_f = cumulative_fitness(curr_population)
        next_gen = roulette_next_gen_selection(curr_population, offspring,
                                               int(len(fittest_individuals) * 1.75),
                                               (cumulative_f_l, total_f))

        next_gen_set = set(next_gen)
        for x in fittest_individuals:
            assert x in next_gen_set

