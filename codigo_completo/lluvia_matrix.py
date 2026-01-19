import pygame as pg
import random

# Inicializar Pygame
pg.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Matrix - Glow Persistente")

# --- COLORES ---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GLOW_COLOR = (100, 255, 100) 

# --- CONFIGURACIÓN ---
FONT_SIZE = 10
font = pg.font.SysFont("ms gothic", FONT_SIZE, bold=True)
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + [str(x) for x in range(10)]

# --- LÓGICA DE DENSIDAD ---
MAX_COLUMNS = WIDTH // FONT_SIZE
all_slots = list(range(MAX_COLUMNS))
random.shuffle(all_slots)

active_columns = [] 
drops = {}          
history = {}        
speeds = {}
counters = {}

current_limit = 1.0  
growth_speed = 0.1   

clock = pg.time.Clock()

def draw_aligned_char(char, col_idx, row_idx, color, glow_intensity=0, clear_first=False):
    """
    Dibuja un carácter con su glow integrado en una sola superficie 
    para que el brillo persista y se desvanezca con la letra.
    """
    x_pos, y_pos = col_idx * FONT_SIZE, row_idx * FONT_SIZE
    
    if clear_first:
        pg.draw.rect(screen, BLACK, (x_pos, y_pos, FONT_SIZE, FONT_SIZE))

    # 1. Crear una superficie para el carácter + su glow (con espacio extra para el aura)
    padding = 6
    char_surf_main = font.render(char, True, color)
    combined_surf = pg.Surface((char_surf_main.get_width() + padding*2, 
                               char_surf_main.get_height() + padding*2), pg.SRCALPHA)
    
    center_x, center_y = combined_surf.get_width()//2, combined_surf.get_height()//2

    # 2. Dibujar el glow DENTRO de la superficie combinada
    if glow_intensity > 0:
        radius_limit = int(FONT_SIZE * 0.7)
        for radius in range(radius_limit, 2, -2):
            alpha = glow_intensity // (radius // 2)
            temp_glow = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
            pg.draw.circle(temp_glow, (*GLOW_COLOR, alpha), (radius, radius), radius)
            combined_surf.blit(temp_glow, (center_x - radius, center_y - radius))

    # 3. Dibujar la letra encima del glow en la misma superficie
    char_rect = char_surf_main.get_rect(center=(center_x, center_y))
    combined_surf.blit(char_surf_main, char_rect)

    # 4. Blit final a la pantalla
    final_rect = combined_surf.get_rect(center=(x_pos + FONT_SIZE//2, y_pos + FONT_SIZE//2))
    screen.blit(combined_surf, final_rect)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False

    # Overlay de rastro (ahora afectará al glow porque están en la misma capa)
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(15) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    if current_limit < MAX_COLUMNS:
        current_limit += growth_speed

    just_started_now = set()

    if len(active_columns) < int(current_limit) and all_slots:
        candidates = [s for s in all_slots if (s-1 not in just_started_now) and (s+1 not in just_started_now)]
        if candidates:
            new_col = random.choice(candidates)
            all_slots.remove(new_col)
            active_columns.append(new_col)
            drops[new_col] = 0 
            history[new_col] = [random.choice(chars) for _ in range(3)]
            speeds[new_col] = random.randint(1, 3)
            counters[new_col] = 0
            just_started_now.add(new_col)

    for i in active_columns:
        counters[i] += 1
        if counters[i] < speeds[i]:
            continue  
        counters[i] = 0

        # --- MUTACIÓN (Ahora hereda glow) ---
        if random.random() > 0.2:
            mut_offset = random.randint(4, 30)
            target_row = drops[i] - mut_offset
            if 0 <= target_row * FONT_SIZE < HEIGHT:
                sample_x = i * FONT_SIZE + FONT_SIZE // 2
                sample_y = target_row * FONT_SIZE + FONT_SIZE // 2
                curr_color = screen.get_at((int(sample_x), int(sample_y)))
                
                if curr_color != BLACK:
                    # Aplicamos intensidad de glow (ej. 50) que se desvanecerá con el rastro
                    draw_aligned_char(random.choice(chars), i, target_row, curr_color, 
                                    glow_intensity=50, clear_first=True)

        # --- DIBUJO DE LA GOTA ---
        if drops[i] >= 3: draw_aligned_char(history[i][0], i, drops[i] - 3, GREEN)
        
        # Las cabezas blancas llevan su glow integrado (Intensidad: 100)
        if drops[i] >= 2: draw_aligned_char(history[i][1], i, drops[i] - 2, WHITE, glow_intensity=70)
        if drops[i] >= 1: draw_aligned_char(history[i][2], i, drops[i] - 1, WHITE, glow_intensity=70)

        new_char = random.choice(chars)
        history[i].pop(0)
        history[i].append(new_char)
        draw_aligned_char(new_char, i, drops[i], WHITE, glow_intensity=70)

        drops[i] += 1
        if drops[i] * FONT_SIZE > HEIGHT:
            if random.random() > 0.95: 
                if (i-1 not in just_started_now) and (i+1 not in just_started_now):
                    drops[i] = 0
                    speeds[i] = random.randint(1, 3) 
                    just_started_now.add(i)

    pg.display.flip()
    clock.tick(20)

pg.quit()