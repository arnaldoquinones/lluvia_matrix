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

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 250, 0)
BRIGHT_GREEN = (160, 255, 160)
DARK_GREEN = (0, 150, 0)

# Ruta a la fuente personalizada
font_path = (r"C:\Users\Arnaldo\AppData\Local\Microsoft\Windows\Fonts\NotoSansJP-VariableFont_wght.ttf")
# Cargar la fuente
try:
    font = pg.font.Font(font_path, 14)  # Aumentamos ligeramente el tamaño
except FileNotFoundError:
    print(f"Fuente no encontrada en {font_path}. Usando fuente predeterminada.")
    font = pg.font.Font(None, 14)

# Caracteres específicos para la lluvia de Matrix (usando caracteres de ancho completo)
selected_characters = "アイウエオカキクケコサシスセソタチツテト０１２３４５６７８９"  # Números japoneses de ancho completo

# Configuración de la cuadrícula
CELL_SIZE = 20  # Tamaño fijo para cada celda
column_x_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE  # Alinear a la cuadrícula

class Letter:
    def __init__(self, char):
        self.char = char
        self.change_time = pg.time.get_ticks() + random.randint(100, 500)

letters = []

def random_char():
    return random.choice(string.ascii_letters)

def random_char2():
    return random.choice(selected_characters)

# Bucle principal
while True:
    current_time = pg.time.get_ticks()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    screen.fill(BLACK)

    letters.append(Letter(random_char2()))

    for i, letter in enumerate(letters):
        if current_time > letter.change_time:
            letter.char = random_char2()
            letter.change_time = current_time + random.randint(100, 500)
        
        if i == 0:
            color = BRIGHT_GREEN
        elif i < 3:
            color = GREEN
        else:
            color = DARK_GREEN
        
        # Centrar el carácter en su celda
        text = font.render(letter.char, True, color)
        text_rect = text.get_rect()
        x_centered = column_x_pos + (CELL_SIZE - text_rect.width) // 2
        y_pos = i * CELL_SIZE
        
        screen.blit(text, (x_centered, y_pos))

    max_letters = HEIGHT // CELL_SIZE
    if len(letters) > max_letters:
        letters.pop(0)

    for i in range(len(letters)):
        if i * CELL_SIZE >= HEIGHT:
            column_x_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE
            letters[i] = Letter(random_char2())

    pg.display.flip()
    pg.time.delay(100)