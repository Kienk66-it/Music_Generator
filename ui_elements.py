import pygame
import piano_lists as pl

pygame.init()

WIDTH = 1300
HEIGHT = 650
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Music Player")

background = pygame.image.load("BackGround/2.jpg")
ukelele_instrument = pygame.image.load("BackGround/3.jpg")
piano_background = pygame.image.load("BackGround/4.jpg")
flute_background = pygame.image.load("BackGround/1.jpg")

font = pygame.font.Font("Fonts/UTM Bebas.ttf", 20)
label_font = pygame.font.Font(None, 14)

PIANO_Y = 300
WHITE_KEY_WIDTH = 25
WHITE_KEY_HEIGHT = 200
BLACK_KEY_WIDTH = 20
BLACK_KEY_HEIGHT = 120
NUM_WHITE_KEYS = 52
NUM_BLACK_KEYS = 36

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20  # Khoảng cách giữa các nút trong Start Menu

CHORDS_ARRAY = {
    'C': [[1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]],
    'D': [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]],
    'E': [[0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'F': [[0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'G': [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'A': [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'B': [[0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Cm': [[0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Dm': [[0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Em': [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Fm': [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Gm': [[0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Am': [[0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'Bm': [[0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'C7': [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'D7': [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'E7': [[0, 0, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'F7': [[0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'G7': [[0, 0, 0, 0, 1], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'A7': [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    'B7': [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

def create_button(text, position):
    button_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    button_surface.fill(GRAY)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(BUTTON_WIDTH/2, BUTTON_HEIGHT/2))
    button_surface.blit(text_surface, text_rect)
    button_rect = pygame.Rect(position[0], position[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    return button_surface, button_rect

def draw_start_menu():
    start_y = HEIGHT // 2 - 2 * BUTTON_HEIGHT - 1.5 * BUTTON_SPACING  # Đẩy các nút lên trên để căn giữa cả 4 nút
    piano_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    ukulele_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)
    sao_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, start_y + 3 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)
    
    pygame.draw.rect(screen, GRAY, piano_button)
    pygame.draw.rect(screen, GRAY, ukulele_button)
    pygame.draw.rect(screen, GRAY, sao_button)
    pygame.draw.rect(screen, GRAY, exit_button)
    
    text_piano = font.render("Piano Mode", True, WHITE)
    text_ukulele = font.render("Ukulele Mode", True, WHITE)
    text_sao = font.render("Flute Mode", True, WHITE)
    text_exit = font.render("Exit", True, WHITE)
    
    screen.blit(text_piano, (piano_button.centerx - text_piano.get_width()//2, 
                            piano_button.centery - text_piano.get_height()//2))
    screen.blit(text_ukulele, (ukulele_button.centerx - text_ukulele.get_width()//2, 
                              ukulele_button.centery - text_ukulele.get_height()//2))
    screen.blit(text_sao, (sao_button.centerx - text_sao.get_width()//2, 
                          sao_button.centery - text_sao.get_height()//2))
    screen.blit(text_exit, (exit_button.centerx - text_exit.get_width()//2, 
                            exit_button.centery - text_exit.get_height()//2))
    
    return piano_button, ukulele_button, sao_button, exit_button

def draw_controls(player):
    # Vị trí bắt đầu và khoảng cách để căn chỉnh đều
    start_x_left = 50  # Cột trái
    start_x_center = WIDTH // 2 - BUTTON_WIDTH - BUTTON_SPACING // 2  # Cột giữa bên trái
    start_x_right = WIDTH // 2 + BUTTON_SPACING // 2  # Cột giữa bên phải
    start_y = 20  # Dòng đầu tiên
    
    # Nút cột trái
    input_button, input_rect = create_button("Input File", (start_x_left, start_y))
    export_button, export_rect = create_button("Export wav file", (start_x_left, start_y + BUTTON_HEIGHT + BUTTON_SPACING))
    
    # Nút cột giữa
    play_status = "Pause" if player.is_playing else "Play"
    play_button, play_rect = create_button(play_status, (start_x_center, start_y))
    reset_button, reset_rect = create_button("Reset", (start_x_right, start_y))
    faster_button, faster_rect = create_button("Faster", (start_x_center, start_y + BUTTON_HEIGHT + BUTTON_SPACING))
    slower_button, slower_rect = create_button("Slower", (start_x_right, start_y + BUTTON_HEIGHT + BUTTON_SPACING))
    
    # Nút Exit trong controls (giữ nguyên từ yêu cầu trước)
    exit_button, exit_rect = create_button("Exit", (start_x_left, start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING)))
    
    # Văn bản tempo và status
    tempo_text = f"Current Tempo: {0.25/player.tempo:.1f}x"
    tempo_surface = font.render(tempo_text, True, WHITE)
    tempo_rect = tempo_surface.get_rect(center=(WIDTH/2, start_y + 3 * (BUTTON_HEIGHT + BUTTON_SPACING)))
    
    status_surface = font.render(player.status_text, True, WHITE)
    status_rect = status_surface.get_rect(center=(WIDTH/2, start_y + 3 * (BUTTON_HEIGHT + BUTTON_SPACING) + 30))
    
    # Vẽ các nút lên màn hình
    screen.blit(input_button, input_rect)
    screen.blit(export_button, export_rect)
    screen.blit(play_button, play_rect)
    screen.blit(reset_button, reset_rect)
    screen.blit(faster_button, faster_rect)
    screen.blit(slower_button, slower_rect)
    screen.blit(exit_button, exit_rect)
    screen.blit(tempo_surface, tempo_rect)
    screen.blit(status_surface, status_rect)
    
    return input_rect, export_rect, play_rect, reset_rect, faster_rect, slower_rect, exit_rect

def draw_piano(screen, player, active_whites, active_blacks):
    white_rects = []
    black_rects = []
    
    for i in range(NUM_WHITE_KEYS):
        is_active = (pl.white_notes[i] in player.current_notes) or any(w[0] == i and w[1] > 0 for w in active_whites)
        color = GREEN if is_active else WHITE
        rect = pygame.draw.rect(screen, color, 
                                [i * WHITE_KEY_WIDTH, PIANO_Y, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT], 0, 2)
        white_rects.append(rect)
        pygame.draw.rect(screen, BLACK, 
                         [i * WHITE_KEY_WIDTH, PIANO_Y, WHITE_KEY_WIDTH, WHITE_KEY_HEIGHT], 1, 2)
        key_label = label_font.render(pl.white_notes[i], True, BLACK)
        screen.blit(key_label, (i * WHITE_KEY_WIDTH + 5, PIANO_Y + WHITE_KEY_HEIGHT - 17))

    skip_count = 0
    last_skip = 2
    skip_track = 2
    for i in range(NUM_BLACK_KEYS):
        is_active = (pl.black_notes[i] in player.current_notes) or any(b[0] == i and b[1] > 0 for b in active_blacks)
        color = GREEN if is_active else BLACK
        x_pos = 15 + (i * WHITE_KEY_WIDTH) + (skip_count * WHITE_KEY_WIDTH)
        rect = pygame.draw.rect(screen, color, [x_pos, PIANO_Y, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT], 0, 2)
        black_rects.append(rect)
        skip_track += 1
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    return white_rects, black_rects, active_whites, active_blacks

def draw_ukulele_fretboard(current_chord, frames_num):
    gray_color = (169, 169, 169)
    yellow_color = (255, 255, 0)
    x_start = 475
    y_start = 420
    circle_radius = 15
    spacing_x = 60
    spacing_y = 33

    notes = [
        ["G", "G#", "A", "A#", "B"],
        ["D", "D#", "E", "E", "F#"],
        ["A#", "B", "C", "C#", "D"],
        ["F", "F#", "G", "G#", "A"]
    ]

    if current_chord in CHORDS_ARRAY and frames_num >= 0:
        chords = CHORDS_ARRAY[current_chord]
        for row in range(4):
            for col in range(5):
                x_pos = x_start + col * spacing_x
                y_pos = y_start + row * spacing_y
                color = yellow_color if chords[row][col] > 0 else gray_color
                pygame.draw.circle(screen, color, (x_pos, y_pos), circle_radius)
                note_text = label_font.render(notes[row][col], True, BLACK)
                screen.blit(note_text, (x_pos - note_text.get_width() // 2, y_pos - note_text.get_height() // 2))
    else:
        for row in range(4):
            for col in range(5):
                x_pos = x_start + col * spacing_x
                y_pos = y_start + row * spacing_y
                pygame.draw.circle(screen, gray_color, (x_pos, y_pos), circle_radius)
                note_text = label_font.render(notes[row][col], True, BLACK)
                screen.blit(note_text, (x_pos - note_text.get_width() // 2, y_pos - note_text.get_height() // 2))
    
    return frames_num - 1

def draw_flute_fretboard(current_note):
    OPEN_HOLE = WHITE
    CLOSED_HOLE = GREEN
    
    x_start = WIDTH // 3 - 0.9
    y_center = HEIGHT // 2 + 5 
    circle_radius = 10
    spacing_x = 50
    
    NOTE_PATTERNS = {
        'do1': [1, 1, 1, 1, 1, 1], 're1': [1, 1, 1, 1, 1, 0], 'mi1': [1, 1, 1, 1, 0, 0],
        'fa1': [1, 1, 1, 0, 0, 0], 'sol1': [1, 1, 0, 0, 0, 0], 'la1': [1, 0, 0, 0, 0, 0],
        'si1': [0, 0, 0, 0, 0, 0], 'do2': [1, 1, 1, 1, 1, 1], 're2': [1, 1, 1, 1, 1, 0],
        'mi2': [1, 1, 1, 1, 0, 0], 'fa2': [1, 1, 1, 0, 0, 0], 'sol2': [1, 1, 0, 0, 0, 0],
        'la2': [1, 0, 0, 0, 0, 0], 'si2': [0, 0, 0, 0, 0, 0], 'do3': [1, 1, 1, 1, 1, 1],
        're3': [1, 1, 1, 1, 1, 0], 'mi3': [1, 1, 1, 1, 0, 0], 'fa3': [1, 1, 1, 0, 0, 0]
    }
    
    hole_pattern = NOTE_PATTERNS.get(current_note, [0, 0, 0, 0, 0, 0])
    
    for i in range(6):
        x_offset = 0 if i < 3 else (16.25 if i < 5 else 31.5)
        x = x_start + (i * spacing_x) + x_offset
        y = y_center
        color = CLOSED_HOLE if hole_pattern[i] else OPEN_HOLE
        pygame.draw.circle(screen, color, (x, y), circle_radius)
        
    if current_note:
        note_text = label_font.render(f"{current_note}", True, WHITE)
        screen.blit(note_text, (WIDTH // 2 - note_text.get_width() // 2, y_center - 60))

def create_back_button():
    back_button, back_rect = create_button("Back to Menu", (50, HEIGHT - 70))
    screen.blit(back_button, back_rect)
    return back_rect