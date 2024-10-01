'''Module with functions to encode and decode
vectors of real numbers to vectors of bits.'''

from typing import List, Tuple
from math import log2
from random import randint


def encode_aux(n_to_encode: int, n_bits: int) -> List[int]:
    """
    Encode a natural number into a list of bits.
    Args:
        n_to_encode (int): The integer to encode.
        n_bits (int): Number of bits for encoding.
    Returns:
        List[int]: List of bits representing the encoded integer,
            least significant bit at start of the list.
    """
    assert n_to_encode >= 0, 'Only natural numbers.'
    if n_to_encode == 0:
        return [0] * n_bits

    assert int(log2(n_to_encode) + 1) <= n_bits, 'Not enough bits to encode.'

    encoded_num = []
    while n_to_encode > 0:
        bit = n_to_encode & 1 # bit menos significativo
        encoded_num.append(bit)
        n_to_encode >>= 1     # corrimiento de bits a la derecha

    while len(encoded_num) < n_bits:
        encoded_num.append(0)

    return encoded_num


def decode_aux(bits: List[int], n_bits: int,
               initial_bit_index: int = 0) -> int:
    """
    Decode a list of bits into an integer.
    Args:
        bits (List[int]): List of bits to decode, least significant
            bit must be at the start of the list
        n_bits (int): Number of bits used for decoding.
        initial_bit_index (int): Starting index for decoding, only
            in case of decoding a vector.
    Returns:
        int: The decoded natural number.
    """
    decoded_num = 0
    i = 0
    for j in range(initial_bit_index, initial_bit_index + n_bits):
        decoded_num += bits[j] * 2**i
        i += 1
    return decoded_num


def encode(x: float, n_bits: int, a: float, b: float) -> List[int]:
    """
    Encode a real number into a list of bits.
    Args:
        x (float): The number to encode (must be within the interval [a, b]).
        n_bits (int): Number of bits for encoding.
        a (float): Minimum value of the interval.
        b (float): Maximum value of the interval.
    Returns:
        List[int]: List of bits representing the encoded number.
    """
    assert a < b, f'Wrong input interval, {a} must be lower than {b}.'
    assert a <= x <= b, f'{x} must be in the interval [{a}, {b}].'

    delta = (b - a) / (2**n_bits - 1)
    n = int((x - a) / delta)
    return encode_aux(n, n_bits)


def decode(x_cod: List[int], n_bits: int, a: float, b: float,
           initial_bit_index: int = 0) -> float:
    """
    Decode a list of bits into a floating-point number.
    Args:
        x_cod (List[int]): List of bits containing the bit to decode.
        n_bits (int): Number of bits used for encoding.
        a (float): Minimum value of the interval.
        b (float): Maximum value of the interval.
        initial_bit_index (int): Starting index for decoding, only
            in case of decoding a vector.
    Returns:
        float: The decoded number.
    """
    assert a < b, f'Wrong input interval, {a} must be lower than {b}.'

    delta = (b - a) / (2**n_bits - 1)
    n = decode_aux(x_cod, n_bits, initial_bit_index)
    return a + delta * n


def encode_vector(v: List[float], v_n_bits: List[int],
                  v_intervals: List[Tuple[float, float]]) -> List[int]:
    """
    Encode a vector of real numbers into a vector of bits.

    Args:
        v (List[float]): Vector of numbers to encode. Each number must
            be within the corresponding interval in `v_intervals`.
        v_n_bits (List[int]): Vector of integers representing the number of
            bits to use for encoding each number in `v`.
        v_intervals (List[Tuple[float, float]]): List of tuples where each
            tuple contains the minimum and maximum values of the interval
            to encode each number in `v`.
    Returns:
        List[int]: Vector of bits representing the encoded vector.
    """
    assert len(v) == len(v_n_bits) == len(v_intervals), 'Lengths of `v`,\
        `v_n_bits`, and `v_intervals` must match.'

    encoded_vector = []
    for num, n_bits, (a, b) in zip(v, v_n_bits, v_intervals):
        encoded_vector.extend(encode(num, n_bits, a, b))
    return encoded_vector


def decode_vector(v: List[int], v_n_bits: List[int],
                  v_intervals: List[Tuple[float, float]]) -> List[float]:
    """
    Decode a vector of bits into a vector of real numbers.
    Args:
        v (List[int]): Vector of bits to decode.
        v_n_bits (List[int]): List of integers where each integer
            specifies the number of bits used for encoding each number.
        v_intervals (List[Tuple[float, float]]): List of tuples where
            each tuple specifies the minimum and maximum values of the
            interval to decode each number.
    Returns:
        List[float]: Vector of decoded real numbers.
    """
    decoded_vector = []
    i = 0
    for n_bits, (a, b) in zip(v_n_bits, v_intervals):
        decoded_vector.append(decode(v, n_bits, a, b, i))
        i += n_bits
    return decoded_vector


def generate_random_vector(v_n_bits: List[int]) -> List[int]:
    """
    Generate a random vector of bits.
    Args:
        v_n_bits (List[int]): List of integers where each integer
            specifies the number of bits for each component in the vector.

    Returns:
        List[int]: List of randomly generated bits, where the
            total number of bits equals the sum of the integers
            in `v_n_bits`.
    """
    return [randint(0,1) for _ in range(sum(v_n_bits))]
