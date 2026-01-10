import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix - Perfect Mutation")

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

    # Overlay (Rastro largo)
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(15) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    for i in range(len(drops)):
        def draw_aligned_char(char, col_idx, row_idx, color, clear_first=False):
            # Coordenadas exactas de la celda
            x_pos = col_idx * FONT_SIZE
            y_pos = row_idx * FONT_SIZE
            
            # SI mueren los caracteres viejos: Limpiamos la celda con negro antes de dibujar
            if clear_first:
                pg.draw.rect(screen, BLACK, (x_pos, y_pos, FONT_SIZE, FONT_SIZE))
            
            char_surf = font.render(char, True, color)
            char_rect = char_surf.get_rect(center=(x_pos + FONT_SIZE // 2, 
                                                   y_pos + FONT_SIZE // 2))
            screen.blit(char_surf, char_rect)

        # --- LÓGICA DE MUTACIÓN SIN SUPERPOSICIÓN ---
        if random.random() > 0.6: 
            mut_offset = random.randint(3, 25)
            target_x = i * FONT_SIZE + FONT_SIZE // 2
            target_y = (drops[i] - mut_offset) * FONT_SIZE + FONT_SIZE // 2
            
            if 0 <= target_y < HEIGHT:
                current_color = screen.get_at((int(target_x), int(target_y)))
                
                if current_color != BLACK:
                    char_mut = random.choice(chars)
                    # LLamamos con clear_first=True para borrar el anterior
                    draw_aligned_char(char_mut, i, drops[i] - mut_offset, current_color, clear_first=True)

        # 1. Verde Fuerte
        draw_aligned_char(history_chars[i][0], i, drops[i] - 2, GREEN)

        # 2. Light Green
        draw_aligned_char(history_chars[i][1], i, drops[i] - 1, LIGHT_GREEN)

        # 3. Punta Blanca
        new_char = random.choice(chars)
        history_chars[i][0] = history_chars[i][1]
        history_chars[i][1] = new_char
        draw_aligned_char(new_char, i, drops[i], WHITE)

        # Movimiento
        drops[i] += 1

        if drops[i] * FONT_SIZE > HEIGHT and random.random() > 0.98:
            drops[i] = 0

    pg.display.flip()
    clock.tick(10)

pg.quit()