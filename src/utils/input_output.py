'''Module with functions for reading and writing files'''

from typing import List
from traceback import print_exc


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
    except Exception as e:
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
    except Exception as e:
        print(f"An error occurred: {e}")
        print_exc()
