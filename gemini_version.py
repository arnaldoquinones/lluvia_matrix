import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix Digital Rain - Fixed Colors")

# --- TUS COLORES ---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Configuración de fuente
FONT_SIZE = 18
font = pg.font.SysFont("ms gothic", FONT_SIZE, bold=True)

# Caracteres
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + [str(x) for x in range(10)]

# Configuración de columnas
columns = WIDTH // FONT_SIZE
drops = [random.randint(-100, 0) for _ in range(columns)]
# Guardamos el último carácter usado en cada columna para mantener la consistencia
last_chars = [random.choice(chars) for _ in range(columns)]

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # El overlay oscurece el rastro
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(35) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    for i in range(len(drops)):
        # 1. Convertimos la punta del frame anterior en VERDE
        # Usamos el mismo carácter que fue blanco hace un momento
        prev_surface = font.render(last_chars[i], True, GREEN)
        screen.blit(prev_surface, (i * FONT_SIZE, (drops[i] - 1) * FONT_SIZE))

        # 2. Elegimos el nuevo carácter para la punta actual
        new_char = random.choice(chars)
        last_chars[i] = new_char # Lo guardamos para el próximo frame
        
        # 3. Dibujamos la PUNTA actual en BLANCO
        text_surface = font.render(new_char, True, WHITE)
        screen.blit(text_surface, (i * FONT_SIZE, drops[i] * FONT_SIZE))

        # Mover la posición
        drops[i] += 1

        # Reiniciar columna
        if drops[i] * FONT_SIZE > HEIGHT and random.random() > 0.95:
            drops[i] = 0

    pg.display.flip()
    clock.tick(7) 

pg.quit()