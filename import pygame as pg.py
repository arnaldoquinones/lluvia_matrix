import pygame as pg
import random
import os

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Lluvia Matrix")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 250, 0)

# Ruta a la fuente personalizada
font_path = (r"C:\Users\Arnaldo\AppData\Local\Microsoft\Windows\Fonts\katakana_tfb.ttf")
# Cargar la fuente
try:
    font = pg.font.Font(font_path, 22)  # Usamos 22 como tamaño de fuente
    print("Fuente cargada correctamente.")
except FileNotFoundError:
    print(f"Fuente no encontrada en {font_path}. Usando fuente predeterminada.")
    font = pg.font.Font(None, 22)  # Fuente predeterminada si la fuente no se encuentra

# Caracteres específicos para la lluvia de Matrix
selected_characters = "アイウエオカキクケコサシスセソタチツテト0123456789"
letters = []  # Lista para almacenar las letras

# Columna única
column_x_pos = random.randint(0, WIDTH - 22)  # Posición aleatoria horizontal dentro de la pantalla

# Función para generar un carácter aleatorio de la lista específica
def random_char2():
    char = random.choice(selected_characters)
    print(f"Carácter generado: {char}")  # Imprimir el carácter generado para diagnóstico
    return char

# Bucle principal
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    # Llenar el fondo de negro
    screen.fill(BLACK)

    # Añadir un nuevo carácter a la lista cada vez
    letters.append(random_char2())

    # Dibujar los caracteres en la pantalla, uno debajo del otro (verticalmente)
    for i, letter in enumerate(letters):
        text = font.render(letter, True, GREEN)
        screen.blit(text, (column_x_pos, i * 22))  # Espaciado vertical de 22 píxeles

    # Limitar la cantidad de letras visibles
    max_letters = HEIGHT // 22  # Establecemos el límite según el espaciado
    if len(letters) > max_letters:  # Cuando la lista de letras excede el límite
        letters.pop(0)  # Eliminar la letra más antigua (la que está más arriba)

    # Cambiar la posición del primer carácter cuando se ha desplazado completamente
    for i in range(len(letters)):
        if i * 22 >= HEIGHT:  # Si la letra ha llegado al final de la pantalla
            # Reiniciar la letra en un nuevo lugar (en la parte superior pero más abajo)
            column_x_pos = random.randint(0, WIDTH - 22)  # Reiniciar la letra con un nuevo carácter
            # Cambiar la posición para que aparezca más abajo en la pantalla
            letters[i] = random_char2()

    # Actualizar la pantalla
    pg.display.flip()

    # Control de velocidad de fotogramas
    pg.time.delay(100)
