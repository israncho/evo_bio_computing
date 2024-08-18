import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update(frame):
    """
    Actualiza la posición del punto en cada cuadro de la animación.

    :param frame: Número del cuadro actual.
    """
    position = frame / (frames - 1)  # Normalizar entre 0 y 1
    point.set_data([position], [0])  # Actualizar la posición del punto con listas
    return point,

# Configurar la figura y el eje
fig, ax = plt.subplots()
ax.set_xlim(0, 1)   # Limites del eje x
ax.set_ylim(-0.5, 0.5)  # Limites del eje y
ax.set_xlabel('Posición')
ax.set_ylabel('Valor')
ax.set_title('Simulación del Movimiento')

# Crear un punto (scatter) en la gráfica
point, = ax.plot([], [], 'ro', markersize=10)  # 'ro' es un punto rojo

# Número total de cuadros
frames = 100

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=frames, blit=True, interval=50)

# Guardar la animación como un archivo GIF
ani.save('results/animation.gif', writer='pillow', fps=60)

print("El GIF ha sido guardado como 'animation.gif'")
