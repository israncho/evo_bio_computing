from random import randint
from src.gen_algo_framework.selection import cumulative_list


def test_cumulative_list():
    for _ in range(1000):
        _population = [None] * randint(20, 60)
        _population = list(map(lambda x: (float(randint(1 ,300)), x), _population))
        c_list = cumulative_list(_population)
        for i in range(1, len(c_list)):
            assert c_list[i - 1] < c_list[i]
        assert 0.99 <= c_list[-1] and c_list[-1] <= 1.00001


def test_roulette_wheel_toss():
    pass


def test_roulette_wheel_selection_two_parents():
    pass
