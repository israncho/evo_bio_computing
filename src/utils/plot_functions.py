'''Module with functions to plot
the performance of a GA execution'''

from typing import List, Tuple
import matplotlib.pyplot as plt

def generate_line_from_data(data: List) -> Tuple[List, List]:
    x_values = list(range(len(data)))
    y_values = data
    return x_values, y_values


def plot_evolution(lines: List[Tuple[List, List]],
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
