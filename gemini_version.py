import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix - Gota Larga")

# --- TUS COLORES ---
WHITE = (255, 255, 255)
LIGHT_GREEN = (200, 255, 200)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# --- TAMAÑO DE FUENTE ---
FONT_SIZE = 12
font = pg.font.SysFont("ms gothic", FONT_SIZE, bold=True)

# Caracteres
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + [str(x) for x in range(10)]

# Estructura
columns = WIDTH // FONT_SIZE
drops = [random.randint(-100, 0) for _ in range(columns)]
history_chars = [[random.choice(chars), random.choice(chars)] for _ in range(columns)]

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # --- CONTROL DEL LARGO DE LA GOTA ---
    # Bajamos el Alpha a 15 para que el rastro sea MUCHO más largo.
    # (Antes estaba en 30 o 40).
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(15) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    for i in range(len(drops)):
        # 1. Carácter a Verde Fuerte
        oldest_char = history_chars[i][0]
        green_surface = font.render(oldest_char, True, GREEN)
        screen.blit(green_surface, (i * FONT_SIZE, (drops[i] - 2) * FONT_SIZE))

        # 2. Carácter a Light Green (Brillo)
        mid_char = history_chars[i][1]
        light_surface = font.render(mid_char, True, LIGHT_GREEN)
        screen.blit(light_surface, (i * FONT_SIZE, (drops[i] - 1) * FONT_SIZE))

        # 3. Punta Blanca
        new_char = random.choice(chars)
        history_chars[i][0] = history_chars[i][1]
        history_chars[i][1] = new_char
        
        white_surface = font.render(new_char, True, WHITE)
        screen.blit(white_surface, (i * FONT_SIZE, drops[i] * FONT_SIZE))

        # Movimiento
        drops[i] += 1

        # Reiniciar columna
        # Al ser la gota más larga, el reinicio por azar debe ser menor 
        # para que no se corten las estelas tan seguido.
        if drops[i] * FONT_SIZE > HEIGHT and random.random() > 0.98:
            drops[i] = 0

    pg.display.flip()
    clock.tick(10) # Un poco más de FPS para compensar el tamaño pequeño

pg.quit()