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
    # Aumentamos el tamaño de la fuente para un efecto más bold
    font = pg.font.Font(font_path, 16)  
    # Creamos una segunda fuente ligeramente más pequeña para el efecto de bloom
    font_glow = pg.font.Font(font_path, 15)  
except FileNotFoundError:
    print(f"Fuente no encontrada en {font_path}. Usando fuente predeterminada.")
    font = pg.font.Font(None, 16)
    font_glow = pg.font.Font(None, 15)

# Caracteres específicos para la lluvia de Matrix (usando caracteres de ancho completo)
selected_characters = "アイウエオカキクケコサシスセソタチツテト０１２３４５６７８９"

# Configuración de la cuadrícula
CELL_SIZE = 20
column_x_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE

class Letter:
    def __init__(self, char):
        self.char = char
        self.change_time = pg.time.get_ticks() + random.randint(100, 500)

letters = []

def random_char():
    return random.choice(string.ascii_letters)

def random_char2():
    return random.choice(selected_characters)

# Función para renderizar texto con efecto de negrita
def render_bold_text(char, color, font, font_glow):
    # Renderizar el texto principal
    text_surface = font.render(char, True, color)
    
    # Renderizar el resplandor (glow) para efecto de negrita
    glow_surface = font_glow.render(char, True, color)
    
    # Crear una superficie final que combine ambas
    final_surface = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
    
    # Centrar ambas superficies
    text_rect = text_surface.get_rect(center=(CELL_SIZE/2, CELL_SIZE/2))
    glow_rect = glow_surface.get_rect(center=(CELL_SIZE/2, CELL_SIZE/2))
    
    # Dibujar primero el resplandor y luego el texto principal
    final_surface.blit(glow_surface, glow_rect)
    final_surface.blit(text_surface, text_rect)
    
    return final_surface

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
        
        # Renderizar texto con efecto de negrita
        text_surface = render_bold_text(letter.char, color, font, font_glow)
        x_pos = column_x_pos
        y_pos = i * CELL_SIZE
        
        screen.blit(text_surface, (x_pos, y_pos))

    max_letters = HEIGHT // CELL_SIZE
    if len(letters) > max_letters:
        letters.pop(0)

    for i in range(len(letters)):
        if i * CELL_SIZE >= HEIGHT:
            column_x_pos = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE
            letters[i] = Letter(random_char2())

    pg.display.flip()
    pg.time.delay(100)