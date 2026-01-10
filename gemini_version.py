import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix Digital Rain - Brillo Extendido")

# --- TUS COLORES ---
WHITE = (255, 255, 255)
LIGHT_GREEN = (200, 255, 200) # Verde muy clarito para el brillo
GREEN = (0, 255, 0)           # Tu verde fuerte
BLACK = (0, 0, 0)

# Configuración de fuente
FONT_SIZE = 12
font = pg.font.SysFont("ms gothic", FONT_SIZE, bold=True)

# Caracteres
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + [str(x) for x in range(10)]

# Estructura de datos
columns = WIDTH // FONT_SIZE
drops = [random.randint(-100, 0) for _ in range(columns)]
# Necesitamos guardar los últimos dos caracteres para mantener la consistencia del brillo
history_chars = [[random.choice(chars), random.choice(chars)] for _ in range(columns)]

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Overlay para el rastro
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(30) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    for i in range(len(drops)):
        # 1. El carácter que estaba en la posición -2 se vuelve VERDE FUERTE
        # (Ya pasó su etapa de brillo)
        oldest_char = history_chars[i][0]
        green_surface = font.render(oldest_char, True, GREEN)
        screen.blit(green_surface, (i * FONT_SIZE, (drops[i] - 2) * FONT_SIZE))

        # 2. El carácter que estaba en la posición -1 se vuelve LIGHT_GREEN
        # (Es la transición del brillo)
        mid_char = history_chars[i][1]
        light_surface = font.render(mid_char, True, LIGHT_GREEN)
        screen.blit(light_surface, (i * FONT_SIZE, (drops[i] - 1) * FONT_SIZE))

        # 3. Elegimos el nuevo carácter para la PUNTA actual (WHITE)
        new_char = random.choice(chars)
        # Rotamos el historial: el que era 1 pasa a 0, y el nuevo entra en 1
        history_chars[i][0] = history_chars[i][1]
        history_chars[i][1] = new_char
        
        # Dibujamos la punta blanca
        white_surface = font.render(new_char, True, WHITE)
        screen.blit(white_surface, (i * FONT_SIZE, drops[i] * FONT_SIZE))

        # Mover la posición
        drops[i] += 1

        # Reiniciar columna
        if drops[i] * FONT_SIZE > HEIGHT and random.random() > 0.95:
            drops[i] = 0

    pg.display.flip()
    clock.tick(7) 

pg.quit()