from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src.tsp.euclidean_tsp import EucTSPPermutation, tour_distance

def animate_tsp_evolution(instance: dict,
                          best_solutions: List[EucTSPPermutation],
                          output_file_path: str,
                          fps_to_use: int =10) -> None:
    fst_c = instance['fst_city']
    rest_of_cities = instance['rest_of_cities']
    output_file = f"{output_file_path}_{instance['NAME']}.gif"

    fig, ax = plt.subplots()

    # plot cities
    x_coords = [city[0] for city in rest_of_cities] + [fst_c[0]]
    y_coords = [city[1] for city in rest_of_cities] + [fst_c[1]]

    ax.scatter(x_coords, y_coords, color='red', s=15) # pyright: ignore

    # graph boundaries
    ax.set_xlim(min(x_coords) - 50, max(x_coords) + 50) # pyright: ignore
    ax.set_ylim(min(y_coords) - 50, max(y_coords) + 50) # pyright: ignore

    line, = ax.plot([], [], color='blue') # pyright: ignore

    generation_text = ax.text(0.01, 0.99, '', # pyright: ignore
                              transform=ax.transAxes, # pyright: ignore
                              fontsize=9,
                              ha='left', va='top')

    # create animation 
    ani = animation.FuncAnimation(fig, update_line,
                                  frames=len(best_solutions),
                                  fargs=(best_solutions, line, instance, generation_text),
                                  blit=True,
                                  interval=500)

    # save as GIF
    ani.save(output_file, writer='pillow', fps=fps_to_use)

    print(f"GIF saved as: '{output_file}'")


def update_line(frame: int,
                permutations: List[EucTSPPermutation],
                line,
                instance: dict,
                generation_text):

    current_permutation = permutations[frame]  # current perm 
    x_0, y_0 = instance['fst_city']

    x_permuted = [city[0] for city in current_permutation] + [x_0, current_permutation[0][0]]
    y_permuted = [city[1] for city in current_permutation] + [y_0, current_permutation[0][1]]

    line.set_data(x_permuted, y_permuted)

    tour_d = tour_distance((x_0, y_0),current_permutation, instance['weights'])

    generation_text.set_text(f'Gen: {frame + 1}\nCost:\n{tour_d}')
    return line,


def generate_line_from_data(data: List) -> Tuple[List, List]:
    x_values = list(range(len(data)))
    y_values = data
    return x_values, y_values


def plot_tsp_evolution(lines: List[Tuple[List, List]],
                       instance: dict,
                       output_file_path: str,
                       labels: List[str] = None) -> None: # pyright: ignore

    plt.figure(figsize=(10, 6))  # Crear una nueva figura

    # Graficar cada línea
    for idx, (x_values, y_values) in enumerate(lines):
        label = labels[idx] if labels else f"Line {idx + 1}"
        plt.plot(x_values, y_values, marker='.', linestyle='-', label=label)

    # Etiquetas y título del gráfico
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title(f"GA exec for the instance '{instance['NAME']}'")

    # Mostrar la leyenda
    plt.legend()

    # Mostrar la cuadrícula
    plt.grid(True)

    output_file = f"{output_file_path}_{instance['NAME']}_GA_plot.png"

    print(f"Plot of performance saved as: '{output_file}'")
    plt.savefig(output_file)
