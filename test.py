# -----------------------------
# - PROYECTO LLUVIA DE MATRIX -
# -----------------------------

import pygame as pg
import random
import string
import os

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 400
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("LLuvia Matrix.")

# Colores con degradado
WHITE = (255, 255, 255)
LIGHT_GREEN = (200, 255, 200)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
DARKER_GREEN = (0, 50, 0)
BLACK = (0, 0, 0)

# Ruta a la fuente personalizada
font_path = (r"C:\Users\Arnaldo\AppData\Local\Microsoft\Windows\Fonts\NotoSansJP-VariableFont_wght.ttf")
# Cargar la fuente
try:
    font = pg.font.Font(font_path, 11) 
    # ACTIVAR NEGRITA AQUÍ:
    font.set_bold(True) 
except FileNotFoundError:
    print(f"Fuente no encontrada en {font_path}. Usando fuente predeterminada.")
    font = pg.font.SysFont("arial", 14, bold=True) # Fuente del sistema en negrita como respaldo

# Caracteres específicos para la lluvia de Matrix (usando caracteres de ancho completo)
selected_characters = "アイウエオカキクケコサシスセソタチツテト０１２３４５６７８９"  # Números japoneses de ancho completo

# Configuración de la cuadrícula
CELL_SIZE = 20  # Tamaño fijo para cada celda
column_x_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE  # Alinear a la cuadrícula

class Letter:
    def __init__(self, char):
        self.char = char
        self.change_time = pg.time.get_ticks() + random.randint(200, 800)  # Tiempo más largo para cambios más lentos

letters = []

def random_char():
    return random.choice(string.ascii_letters)

def random_char2():
    return random.choice(selected_characters)

# Función para obtener color según la posición (ahora invertida)
def get_gradient_color(position, total_positions):
    if position == 0:
        return BLACK
    elif position == 1:
        return DARKER_GREEN
    elif position < total_positions * 0.3:
        return DARK_GREEN
    elif position < total_positions * 0.6:
        return GREEN
    elif position < total_positions * 0.8:
        return LIGHT_GREEN
    else:
        return WHITE

# Contador de cadenas completadas
completed_chains = 0
MAX_CHAINS = 3  # Número de cadenas completas que queremos generar
chain_complete = False

# Bucle principal
running = True
while running:
    current_time = pg.time.get_ticks()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(BLACK)

    # Solo agregamos nuevas letras si no hemos completado la cadena actual
    if not chain_complete:
        letters.append(Letter(random_char2()))

    max_letters = HEIGHT // CELL_SIZE
    total_letters = len(letters)

    for i, letter in enumerate(letters):
        if current_time > letter.change_time:
            letter.char = random_char2()
            letter.change_time = current_time + random.randint(200, 800)  # Tiempo más largo para cambios más lentos
        
        # Obtener color basado en la posición
        color = get_gradient_color(i, max_letters)
        
        # Centrar el carácter en su celda
        text = font.render(letter.char, True, color)
        text_rect = text.get_rect()
        x_centered = column_x_pos + (CELL_SIZE - text_rect.width) // 2
        y_pos = i * CELL_SIZE
        
        screen.blit(text, (x_centered, y_pos))

    if len(letters) > max_letters:
        letters.pop(0)
        if not chain_complete:
            chain_complete = True
            completed_chains += 1
            if completed_chains >= MAX_CHAINS:
                pg.time.delay(1000)
                running = False

    if chain_complete and completed_chains < MAX_CHAINS:
        column_x_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE
        letters = []
        chain_complete = False

    pg.display.flip()
    pg.time.delay(200)  # Aumentado el delay para hacer la caída más lenta

pg.quit()