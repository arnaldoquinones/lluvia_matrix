import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix Digital Rain - Optimized")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 70)
WHITE = (210, 255, 210) 

# Configuración de fuente
FONT_SIZE = 18
# Mantenemos la negrita que solicitaste
font = pg.font.SysFont("ms gothic", FONT_SIZE, bold=True)

# Caracteres (Katakana y números)
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + [str(x) for x in range(10)]

# Configuración de columnas
columns = WIDTH // FONT_SIZE
drops = [random.randint(-100, 0) for _ in range(columns)]

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Fondo con rastro
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(30) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    for i in range(len(drops)):
        # Seleccionar carácter aleatorio
        char = random.choice(chars)
        
        # 1. Dibujar el carácter "brillante" (el primero de la fila)
        text_surface = font.render(char, True, WHITE)
        screen.blit(text_surface, (i * FONT_SIZE, drops[i] * FONT_SIZE))

        # 2. Dibujar un carácter verde justo arriba del blanco para dejar rastro
        prev_char = random.choice(chars)
        prev_text = font.render(prev_char, True, GREEN)
        screen.blit(prev_text, (i * FONT_SIZE, (drops[i] - 1) * FONT_SIZE))

        # Mover la posición de la columna
        drops[i] += 1

        # Reiniciar columna cuando llega al final o por azar
        if drops[i] * FONT_SIZE > HEIGHT and random.random() > 0.95:
            drops[i] = 0

    pg.display.flip()
    
    # --- LA CLAVE DE LA VELOCIDAD ---
    # Bajamos de 30 a 10 (o menos) para que sea MUCHO más lento
    # 10 significa que la gota avanza solo 10 cuadros por segundo
    clock.tick(10) 

pg.quit()