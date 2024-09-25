'''Module with functions for reading and writing files'''

from typing import Callable, List
from traceback import print_exc

from src.tsp.euclidean_tsp import EucCity, EucTSPPermutation, build_weight_dict


def read_file(file_path: str) -> List[str]:
    '''Reads a file using utf-8 encongind
    and returns its contents as a list of lines.'''

    list_of_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                list_of_lines.append(line.strip())

        print(f"Successful reading of file '{file_path}'")
    except FileNotFoundError as e:
        print(f"The file '{file_path}' was not found:\n{e}")
    except PermissionError as e:
        print(f"You do not have permission to open this file:\n{e}")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")
        print_exc()

    return list_of_lines


def write_file(file_path: str, lines_of_the_file: List[str]) -> None:
    '''Writes a list of lines to a file.'''

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines_of_the_file:
                file.write(line)

        print(f"Written in the file '{file_path}'")
    except PermissionError as e:
        print(f"You do not have permission to open this file:\n{e}")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")
        print_exc()


def is_number(str_test: str, transform_func: Callable) -> bool:
    '''Checks if a given string can be converted to a number using
    the specified transformation function.'''
    try:
        transform_func(str_test)
        return True
    except ValueError:
        return False


def to_number(num_as_str: str) -> float | int:
    '''Converts a string to either an integer or a float. '''
    if is_number(num_as_str, int):
        return int(num_as_str)
    if is_number(num_as_str, float):
        return float(num_as_str)
    raise ValueError(f"'{num_as_str}' is not a valid number")


def parse_tsp_data(lines_of_the_file: List[str]) -> dict:
    '''Extracts and parses the tsp instance details from
    a list of lines.'''

    instance_details = {'SOLUTION': False, 'NAME': None,
        'TYPE': None, 'COMMENT': None, 'DIMENSION': None,
        'EDGE_WEIGHT_TYPE': None, 'ids': {}, 'fst_city' : None,
        'rest_of_cities' : []}

    reading_vertices = False
    reading_fst_c = True

    for line in lines_of_the_file:

        if not reading_vertices:
            line = line.replace(':', '')

        line_elems = line.split()

        if line_elems[0] == 'SOLUTION':
            instance_details['SOLUTION'] = True
            continue

        if line_elems[0] == 'EOF':
            break

        if line_elems[0] == 'NODE_COORD_SECTION':
            reading_vertices = True
            continue

        if not reading_vertices:
            instance_details[line_elems[0]] = " ".join(line_elems[1:])

        if reading_vertices:
            vertex = tuple(map(to_number, line_elems[1:]))
            instance_details['ids'][vertex] = int(line_elems[0])
            if reading_fst_c:
                instance_details['fst_city'] = vertex
                reading_fst_c = False
            else:
                instance_details['rest_of_cities'].append(vertex)

    instance_details['DIMENSION'] = int(instance_details['DIMENSION'])
    assert instance_details['DIMENSION'] == (
        len(instance_details['rest_of_cities']) + 1)

    instance_details['weights'] = build_weight_dict(
        instance_details['fst_city'],
        instance_details['rest_of_cities'])

    return instance_details


def tsp_solution_to_lines(fst_city: EucCity,
                          rest_of_cities: EucTSPPermutation,
                          instance: dict) -> List[str]:
    '''Converts a solution to a list of strings, each representing
    a line in a file.'''
    vertex_id = instance['vertex_to_id']

    list_of_lines = ['SOLUTION\n']
    list_of_lines.append(f"NAME: {instance['NAME']}\n")
    list_of_lines.append(f"TYPE: {instance['TYPE']}\n")
    list_of_lines.append(f"COMMENT: {instance['COMMENT']}\n")
    list_of_lines.append(f"DIMENSION: {instance['DIMENSION']}\n")
    list_of_lines.append(f"EDGE_WEIGHT_TYPE: {instance['EDGE_WEIGHT_TYPE']}\n")
    list_of_lines.append('NODE_COORD_SECTION\n')

    list_of_lines.append(f'{vertex_id[fst_city]} {fst_city[0]} {fst_city[1]}\n')
    for u, v in rest_of_cities:
        list_of_lines.append(f'{vertex_id[(u, v)]} {u} {v}\n')

    return list_of_lines
