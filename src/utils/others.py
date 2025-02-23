'''
Module for various auxiliar and utils functions.
'''

from os import urandom
from math import ceil
from random import seed
from typing import List, Tuple

def seed_in_use(seed_to_use: int |
                float | str |
                bytes | bytearray |
                None = None) -> int | float | str | bytes | bytearray | None:
    '''
    Set a random seed for the random number generator.
    If no seed is provided, a random seed based on the current time is generated.

    Args:
        seed_to_use (int | float | str | bytes | bytearray | None, optional): Optional
        argument given by the user. Defaults to None.

    Returns:
        int | float | str | bytes | bytearray | None: The seed that is being used
        (either the provided or generated one).
    '''

    if seed_to_use is None:
        seed_to_use = int.from_bytes(urandom(4), 'big')
    seed(seed_to_use)
    return seed_to_use


def compute_generational_avgs(multiple_ga_execs_data: List[List[Tuple]]) -> List[List[float]]:
    n_executions = len(multiple_ga_execs_data)
    n_generations = len(multiple_ga_execs_data[0])
    number_measures = len(multiple_ga_execs_data[0][0])
    measures = [[0.0] * n_generations for _ in range(number_measures)]

    for execution_data in multiple_ga_execs_data:
        for generation_number, generation_data in enumerate(execution_data):
            for measure_i, measure_data in enumerate(generation_data):
                measures[measure_i][generation_number] += measure_data

    for i, row in enumerate(measures):
        for j in range(len(row)):
            measures[i][j] /= n_executions

    return measures