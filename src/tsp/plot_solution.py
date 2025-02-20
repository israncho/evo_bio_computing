from sys import argv
from math import inf
from src.utils.input_output import parse_tsp_data, read_file
from src.tsp.visualization import plot_tsp_solution

if __name__ == "__main__":
    print()
    SOLUTION_PATH = argv[1]
    OUTPUT_PATH = argv[2]

    solution_instance: dict = parse_tsp_data(read_file(SOLUTION_PATH))
    solution_instance['f_execs'] = 0
    solution_instance['current_best'] = inf, None
    solution_instance['best_fitness_found_history'] = []
    plot_tsp_solution(solution_instance, solution_instance['rest_of_cities'], OUTPUT_PATH) # pyright: ignore
