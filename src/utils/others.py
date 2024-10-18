'''
Module for various auxiliar and utils functions.
'''

from os import urandom
from random import seed

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