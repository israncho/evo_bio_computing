from sys import argv
from ast import literal_eval
from src.utils.input_output import read_file, to_number, write_file, tsp_solution_to_lines

if __name__ == "__main__":
    print()
    INSTANCE_FILE_PATH = argv[1]
    print(INSTANCE_FILE_PATH)
    OUTPUT_FILE_PATH = argv[2]
    print('output path:', OUTPUT_FILE_PATH)
    new_instance = literal_eval(argv[3])

    assert new_instance['NAME'] is not None
    assert new_instance['TYPE'] is not None
    assert new_instance['COMMENT'] is not None
    assert new_instance['EDGE_WEIGHT_TYPE'] is not None

    lines_of_coords = read_file(INSTANCE_FILE_PATH)
    new_instance['DIMENSION'] = len(lines_of_coords)

    fst_city = tuple(map(to_number, lines_of_coords.pop().split()))
    new_instance['ids'] = {fst_city: 1}

    ids_count = 2
    rest_of_cities = []


    print(new_instance)
    for line in lines_of_coords:
        vertex = tuple(map(to_number, line.split()))
        new_instance['ids'][vertex] = ids_count
        ids_count += 1
        rest_of_cities.append(vertex)

    write_file(OUTPUT_FILE_PATH, tsp_solution_to_lines(fst_city, rest_of_cities, new_instance))