from sys import argv
from src.utils.input_output import read_lines_from_csv_file, parse_tsp_data, read_file
from src.utils.plot_functions import box_plot, generate_line_from_data, plot_evolution

if __name__ == "__main__":
    print()
    DATA_PATH = argv[1]
    SOLUTION_PATH = argv[2]
    OUTPUT_PATH = argv[3]
    STEP = int(argv[4])

    line = None
    for data in read_lines_from_csv_file(DATA_PATH):
        line = generate_line_from_data(data, STEP)
        break

    solution_instance: dict = parse_tsp_data(read_file(SOLUTION_PATH))
    plot_evolution([line], solution_instance, OUTPUT_PATH, ['best_found'], x_logscale=True)