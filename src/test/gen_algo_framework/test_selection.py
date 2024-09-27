from random import randint
from typing import List, Optional, Tuple
from src.gen_algo_framework.selection import cumulative_fitness, remove_from_fitness_list, roulette_wheel_toss


def __random_c_list():
    _population = [None] * randint(20, 60)
    _population = list(map(lambda x: (float(randint(1 , 1000)), x), _population))
    c_list  = cumulative_fitness(_population)
    total_f = c_list[-1]
    return c_list, total_f, _population


def test_cumulative_fitness(c_list_to_test: Optional[List[float]] = None):
    tests = 5000

    c_list: List[float] = []
    _pop : List[Tuple[float, None]] = []

    if c_list_to_test is not None:
        tests = 1
        c_list = c_list_to_test

    for _ in range(tests):
        if c_list_to_test is None:
            c_list, _, _pop = __random_c_list()

        for i in range(1, len(c_list)):
            assert c_list[i - 1] < c_list[i], f'List not strictly increasing at index {i}'
        assert 0 < c_list[0], f'First element out of range: {c_list[0]}'

        if c_list_to_test is None:
            assert c_list[-1] == sum(x[0] for x in _pop)


def test_roulette_wheel_toss():
    for _ in range(10000):
        c_list, _, _ = __random_c_list()
        i = roulette_wheel_toss(c_list)
        assert 0 <= i and i < len(c_list), f'Index out of range: {i}'

    index_tosses = {0: 0, 1: 0, 2: 0, 3: 0}
    fixed_c_list = [25.0, 50.0, 75.0, 100.0]
    tosses = 20000

    for _ in range(tosses):
        index_selected = roulette_wheel_toss(fixed_c_list)
        index_tosses[index_selected] += 1

    for val in index_tosses.values():
        election_rate = val / tosses
        assert 0.24 < election_rate and election_rate < 0.26, f'Election rate out of range: {election_rate}'


def test_remove_from_fitness_list():
    for _ in range(1000):
        c_list, _, _popu = __random_c_list()

        for _ in range(randint(0, len(c_list) // 2)):
            index = randint(0, len(c_list) - 1)
            individual_fitness = _popu[index][0]

            c_list = remove_from_fitness_list(index, individual_fitness, c_list)

            test_cumulative_fitness(c_list)

            _popu.pop(index)
            recalc_c_list = cumulative_fitness(_popu)
            recalc_f = recalc_c_list[-1]
            assert recalc_c_list == c_list
            assert recalc_c_list is not c_list
            assert recalc_f == c_list[-1]
