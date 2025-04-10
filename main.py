import pygame
from players import PianoPlayer, UkulelePlayer, FlutePlayer, white_sounds, black_sounds
from ui_elements import *
import piano_lists as pl

pygame.init()

# Game Modes
class MusicMode:
    PIANO = 1
    UKULELE = 2
    SAO_TRUC = 3

# Piano keyboard mappings
PIANO_KEYS = [
    'Q', 'E', 'T', 'Y', 'I', 'P', 'S',  # C4 octave
    'D', 'G', 'J', 'K', 'Z', 'C', 'B',  # C5 octave
    'N', '1', '3', '4', '6', '8', '0'   # C6 octave
]

SHARP_KEYS = [
    'W', 'R',  # C#4, D#4
    'U', 'O',  # F#4, G#4
    'A',       # A#4
    'F', 'H',  # C#5, D#5
    'K',       # F#5
    'X', 'V',  # G#5, A#5
    'M', '2',  # C#6, D#6
    '5', '7',  # F#6, G#6
    '9'        # A#6
]

C4_octaves = {
    'Q': 'C4', 'W': 'Db4', 'E': 'D4', 'R': 'Eb4', 'T': 'E4', 'Y': 'F4',
    'U': 'Gb4', 'I': 'G4', 'O': 'Ab4', 'P': 'A4', 'A': 'Bb4', 'S': 'B4',
}

C5_octaves = {
    'D': 'C5', 'F': 'Db5', 'G': 'D5', 'H': 'Eb5', 'J': 'E5', 'K': 'F5',
    'L': 'Gb5', 'Z': 'G5', 'X': 'Ab5', 'C': 'A5', 'V': 'Bb5', 'B': 'B5',
}

C6_octaves = {
    'N': 'C6', 'M': 'Db6', '1': 'D6', '2': 'Eb6', '3': 'E6', '4': 'F6',
    '5': 'Gb6', '6': 'G6', '7': 'Ab6', '8': 'A6', '9': 'Bb6', '0': 'B6',
}

KEY_TO_CHORD = {
    pygame.K_q: 'C', pygame.K_w: 'D', pygame.K_e: 'E', pygame.K_r: 'F', 
    pygame.K_t: 'G', pygame.K_y: 'A', pygame.K_u: 'B',
    pygame.K_a: 'Cm', pygame.K_s: 'Dm', pygame.K_d: 'Em', 
    pygame.K_f: 'Fm', pygame.K_g: 'Gm', pygame.K_h: 'Am', pygame.K_j: 'Bm',
    pygame.K_z: 'C7', pygame.K_x: 'D7', pygame.K_c: 'E7', 
    pygame.K_v: 'F7', pygame.K_b: 'G7', pygame.K_n: 'A7', pygame.K_m: 'B7'
}

FLUTE_KEY_MAPPING = {
    pygame.K_q: 'C1', pygame.K_w: 'D1', pygame.K_e: 'E1', 
    pygame.K_r: 'F1', pygame.K_t: 'G1', pygame.K_y: 'A1', pygame.K_u: 'B1',
    pygame.K_a: 'C2', pygame.K_s: 'D2', pygame.K_d: 'E2', 
    pygame.K_f: 'F2', pygame.K_g: 'G2', pygame.K_h: 'A2', pygame.K_j: 'B2',
    pygame.K_z: 'C3', pygame.K_x: 'D3', pygame.K_c: 'E3', pygame.K_v: 'F3'
}

def main():
    piano_player = PianoPlayer()
    ukulele_player = UkulelePlayer()
    flute_player = FlutePlayer()
    current_mode = None
    imported_file = False
    active_whites = []
    active_blacks = []
    running = True
    timer = pygame.time.Clock()
    
    while running:
        timer.tick(FPS)
        
        if current_mode is None:
            screen.blit(background, (0, 0))
            piano_button, ukulele_button, sao_button, exit_button = draw_start_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if piano_button.collidepoint(event.pos):
                        current_mode = MusicMode.PIANO
                    elif ukulele_button.collidepoint(event.pos):
                        current_mode = MusicMode.UKULELE
                    elif sao_button.collidepoint(event.pos):
                        current_mode = MusicMode.SAO_TRUC
                    elif exit_button.collidepoint(event.pos):
                        running = False  # Thoát chương trình khi nhấn Exit trong Start Menu
        
        elif current_mode == MusicMode.PIANO:
            screen.blit(piano_background, (0, 0))
            for i, white in enumerate(active_whites):
                white[1] -= 1
            active_whites = [white for white in active_whites if white[1] > 0]
            for i, black in enumerate(active_blacks):
                black[1] -= 1
            active_blacks = [black for black in active_blacks if black[1] > 0]
            
            input_rect, export_rect, play_rect, reset_rect, faster_rect, slower_rect, exit_rect = draw_controls(piano_player)
            white_keys, black_keys, active_whites, active_blacks = draw_piano(screen, piano_player, active_whites, active_blacks)
            back_rect = create_back_button()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.TEXTINPUT:
                    if event.text.upper() in C4_octaves:
                        note = C4_octaves[event.text.upper()]
                        if 'b' in note:
                            index = pl.black_notes.index(note)
                            black_sounds[index].play(0, 1000)
                            active_blacks.append([index, 30])
                        else:
                            index = pl.white_notes.index(note)
                            white_sounds[index].play(0, 1000)
                            active_whites.append([index, 30])
                    elif event.text.upper() in C5_octaves:
                        note = C5_octaves[event.text.upper()]
                        if 'b' in note:
                            index = pl.black_notes.index(note)
                            black_sounds[index].play(0, 1000)
                            active_blacks.append([index, 30])
                        else:
                            index = pl.white_notes.index(note)
                            white_sounds[index].play(0, 1000)
                            active_whites.append([index, 30])
                    elif event.text.upper() in C6_octaves:
                        note = C6_octaves[event.text.upper()]
                        if 'b' in note:
                            index = pl.black_notes.index(note)
                            black_sounds[index].play(0, 1000)
                            active_blacks.append([index, 30])
                        else:
                            index = pl.white_notes.index(note)
                            white_sounds[index].play(0, 1000)
                            active_whites.append([index, 30])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        current_mode = None
                        continue
                    if input_rect.collidepoint(event.pos) and not piano_player.input_active:
                        piano_player.import_file()
                    elif export_rect.collidepoint(event.pos):
                        piano_player.export_audio()
                    elif play_rect.collidepoint(event.pos) and imported_file:
                        if piano_player.is_playing:
                            piano_player.pause_music()
                        else:
                            piano_player.play_music()
                    elif reset_rect.collidepoint(event.pos):
                        piano_player.reset_music()
                        imported_file = False
                    elif faster_rect.collidepoint(event.pos):
                        piano_player.set_tempo(max(0.1, piano_player.tempo - 0.05))
                    elif slower_rect.collidepoint(event.pos):
                        piano_player.set_tempo(min(1.0, piano_player.tempo + 0.05))
                    elif exit_rect.collidepoint(event.pos):
                        running = False  # Thoát chương trình khi nhấn Exit trong Piano Mode
                    else:
                        black_key = False
                        for i, rect in enumerate(black_keys):
                            if rect.collidepoint(event.pos):
                                black_sounds[i].play(0, 1000)
                                active_blacks.append([i, 30])
                                black_key = True
                                break
                        if not black_key:
                            for i, rect in enumerate(white_keys):
                                if rect.collidepoint(event.pos):
                                    white_sounds[i].play(0, 3000)
                                    active_whites.append([i, 30])
                                    break
            if piano_player.input_active and piano_player.import_file():
                imported_file = True
        
        elif current_mode == MusicMode.UKULELE:
            screen.blit(ukelele_instrument, (0, 0))
            input_rect, export_rect, play_rect, reset_rect, faster_rect, slower_rect, exit_rect = draw_controls(ukulele_player)
            back_rect = create_back_button()
            frames_num = draw_ukulele_fretboard(ukulele_player.current_chord, ukulele_player.frames_num)
            ukulele_player.frames_num = frames_num
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in KEY_TO_CHORD:
                        ukulele_player.play_chord(KEY_TO_CHORD[event.key])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        current_mode = None
                        continue
                    if input_rect.collidepoint(event.pos) and not ukulele_player.input_active:
                        ukulele_player.import_file()
                    elif export_rect.collidepoint(event.pos):
                        ukulele_player.export_audio()
                    elif play_rect.collidepoint(event.pos) and imported_file:
                        if ukulele_player.is_playing:
                            ukulele_player.pause_music()
                        else:
                            ukulele_player.play_music()
                    elif reset_rect.collidepoint(event.pos):
                        ukulele_player.reset_music()
                        imported_file = False
                    elif faster_rect.collidepoint(event.pos):
                        ukulele_player.set_tempo(max(0.1, ukulele_player.tempo - 0.05))
                    elif slower_rect.collidepoint(event.pos):
                        ukulele_player.set_tempo(min(1.0, ukulele_player.tempo + 0.05))
                    elif exit_rect.collidepoint(event.pos):
                        running = False  # Thoát chương trình khi nhấn Exit trong Ukulele Mode
            if ukulele_player.input_active and ukulele_player.import_file():
                imported_file = True
        
        elif current_mode == MusicMode.SAO_TRUC:
            screen.blit(flute_background, (0, 0))
            input_rect, export_rect, play_rect, reset_rect, faster_rect, slower_rect, exit_rect = draw_controls(flute_player)
            back_rect = create_back_button()
            draw_flute_fretboard(flute_player.current_note)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in FLUTE_KEY_MAPPING:
                        note = FLUTE_KEY_MAPPING[event.key]
                        if note in flute_player.preloaded_sounds:
                            pygame.mixer.Sound(flute_player.preloaded_sounds[note]).play()
                            flute_player.current_note = flute_player.note_mapping[note]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        current_mode = None
                        continue
                    if input_rect.collidepoint(event.pos) and not flute_player.input_active:
                        flute_player.import_file()
                    elif export_rect.collidepoint(event.pos):
                        flute_player.export_audio()
                    elif play_rect.collidepoint(event.pos) and imported_file:
                        if flute_player.is_playing:
                            flute_player.pause_music()
                        else:
                            flute_player.play_music()
                    elif reset_rect.collidepoint(event.pos):
                        flute_player.reset_music()
                        imported_file = False
                    elif faster_rect.collidepoint(event.pos):
                        flute_player.set_tempo(max(0.1, flute_player.tempo - 0.05))
                    elif slower_rect.collidepoint(event.pos):
                        flute_player.set_tempo(min(1.0, flute_player.tempo + 0.05))
                    elif exit_rect.collidepoint(event.pos):
                        running = False  # Thoát chương trình khi nhấn Exit trong Flute Mode
            if flute_player.input_active and flute_player.import_file():
                imported_file = True
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()