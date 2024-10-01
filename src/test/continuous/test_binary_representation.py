from random import randint, uniform
from math import isclose

from src.continuous.binary_representation import decode_vector, encode_vector, generate_random_vector


def test_encode_decode_vector():
    for _ in range(1000):
        vector_size = randint(5, 20)
        random_vector = [uniform(-500.0, 500.0) for _ in range(vector_size)]
        v_n_bits = [27 for _ in range(vector_size)]
        v_intervals = [(-500.0, 500.0) for _ in range(vector_size)]

        encoded_vec = encode_vector(random_vector, v_n_bits, v_intervals)

        for e in encoded_vec:
            assert e in (0, 1), f'{e} is not binary'

        decoded_vec = decode_vector(encoded_vec, v_n_bits, v_intervals)

        for original, decoded in zip(random_vector, decoded_vec):
            assert isclose(original, decoded, abs_tol=1e-5), f'{original}, {decoded} are not similar'


def test_generate_random_vector():
    for _ in range(1000):
        vector_size = randint(5, 20)
        v_n_bits = [27 for _ in range(vector_size)]
        v_intervals = [(-500.0, 500.0) for _ in range(vector_size)]
        random_vec_bits = generate_random_vector(v_n_bits)

        for bit in random_vec_bits:
            assert bit in (0, 1)

        real_val_vec = decode_vector(random_vec_bits, v_n_bits, v_intervals)
        #print(real_val_vec)

        for e in real_val_vec:
            assert type(e) == float, f'{e} is not float.'
            assert -500 <= e <= 500, f'{e} is out of range.'

        re_encoded = encode_vector(real_val_vec, v_n_bits, v_intervals)
        re_decoded = decode_vector(re_encoded, v_n_bits, v_intervals)

        for original, decoded in zip(real_val_vec, re_decoded):
            assert isclose(original, decoded, abs_tol=1e-5), f'{original}, {decoded} are not similar'
