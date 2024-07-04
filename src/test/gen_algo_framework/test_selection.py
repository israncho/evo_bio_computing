from random import randint
from src.gen_algo_framework.selection import cumulative_fitness, roulette_wheel_selection_two_parents, roulette_wheel_toss


def __random_c_list():
    _population = [None] * randint(20, 60)
    _population = list(map(lambda x: (float(randint(1 , 1000)), x), _population))
    return cumulative_fitness(_population)


def test_cumulative_fitness():
    for _ in range(5000):
        c_list, _ = __random_c_list()
        for i in range(1, len(c_list)):
            assert c_list[i - 1] < c_list[i], f'List not strictly increasing at index {i}'
        assert 0 < c_list[0], f'First element out of range: {c_list[0]}'


def test_roulette_wheel_toss():
    for _ in range(10000):
        c_list, total_f = __random_c_list()
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
        c_list, total_f = __random_c_list()
        i, j = roulette_wheel_selection_two_parents(c_list, total_f)
        assert i != j, f'Selected same index for both parents: {i}'
        assert 0 <= i and i < len(c_list), f'Index i out of range: {i}'
        assert 0 <= j and j < len(c_list), f'Index j out of range: {j}'
