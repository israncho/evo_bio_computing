'''Module with functions to plot
the performance of a GA execution'''

from typing import List, Tuple
import matplotlib.pyplot as plt

def generate_line_from_data(data: List, step: int = 1) -> Tuple[List, List]:
    x_values = list(map(lambda x : x * step, range(len(data))))
    y_values = data
    return x_values, y_values


def plot_evolution(lines: List[Tuple[List, List]],
                   instance: dict,
                   output_file_path: str,
                   labels: List[str] = None,
                   y_label: str = 'Fitness',
                   x_label: str = 'Generation',
                   y_logscale: bool = False,
                   x_logscale: bool = False) -> None: # pyright: ignore

    plt.figure(figsize=(10, 6))  # Crear una nueva figura

    # Graficar cada línea
    for idx, (x_values, y_values) in enumerate(lines):
        label = labels[idx] if labels else f"Line {idx + 1}"
        plt.plot(x_values, y_values, marker='.', linestyle='-', label=label)

    # Etiquetas y título del gráfico
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"GA - '{instance['NAME']}'")

    #plt.figtext(0.5, 0.008, f"\n\n{str(instance)}", wrap=True,
    #        horizontalalignment='center', fontsize=6)

    # Mostrar la leyenda
    plt.legend()

    if y_logscale:
        plt.yscale('log')
    if x_logscale:
        plt.xscale('log')

    # Mostrar la cuadrícula
    plt.grid(True)

    output_file = f"{output_file_path}_{instance['NAME']}_GA_plot.png"

    print(f"Plot of performance saved as: '{output_file}'")
    plt.savefig(output_file)
    plt.close()


def box_plot(data: List[List[float]],
             labels: List[str],
             output_file: str,
             y_logscale: bool = False,
             y_label: str = 'Fitness') -> None:
    if y_logscale:
        plt.yscale('log')
    plt.boxplot(data)
    plt.xticks(ticks=list(range(1, len(labels) + 1)), labels=labels, fontsize=7)  # Asignar nombres a las categorías
    plt.xlabel('Techniques')
    plt.ylabel(y_label)
    plt.title(output_file)
    plt.savefig(output_file)
    plt.close()
