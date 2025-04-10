import pygame
from pygame import mixer
import librosa
import numpy as np
import sounddevice as sd
import easygui
import threading
import queue
from scipy.io import wavfile
import os
import piano_lists as pl
from audio_effects import add_effects

pygame.mixer.init()
pygame.mixer.set_num_channels(50)

# Load piano sounds
white_sounds = [mixer.Sound(f'notes/{note}.wav') for note in pl.white_notes]
black_sounds = [mixer.Sound(f'notes/{note}.wav') for note in pl.black_notes]

# Ukulele notes and chords
UKULELE_NOTES = 'C, D, E, F, G, A, B, Cm, Dm, Em, Fm, Gm, Am, Bm, C7, D7, E7, F7, G7, A7, B7'
NOTES_LIST = UKULELE_NOTES.split(', ')
ukulele_notes_sounds = {note: mixer.Sound(f'Tracks/ukelele/{note}.wav') for note in NOTES_LIST 
                        if os.path.exists(f'Tracks/ukelele/{note}.wav')}

class PianoPlayer:
    def __init__(self):
        self.notes = []
        self.combined_signal = None
        self.sr = 44100
        self.is_playing = False
        self.tempo = 0.25
        self.status_text = "No file imported"
        self.current_position = 0
        self.stream = None
        self.current_notes = set()
        self.note_timings = []
        self.note_map = {
            'A0': 'Tracks/piano/A0.wav', 'A#0': 'Tracks/piano/Bb0.wav', 'B0': 'Tracks/piano/B0.wav',
            'C1': 'Tracks/piano/C1.wav', 'C#1': 'Tracks/piano/Db1.wav', 'D1': 'Tracks/piano/D1.wav',
            'D#1': 'Tracks/piano/Eb1.wav', 'E1': 'Tracks/piano/E1.wav', 'F1': 'Tracks/piano/F1.wav',
            'F#1': 'Tracks/piano/Gb1.wav', 'G1': 'Tracks/piano/G1.wav', 'G#1': 'Tracks/piano/Ab1.wav',
            'A1': 'Tracks/piano/A1.wav', 'A#1': 'Tracks/piano/Bb1.wav', 'B1': 'Tracks/piano/B1.wav',
            'C2': 'Tracks/piano/C2.wav', 'C#2': 'Tracks/piano/Db2.wav', 'D2': 'Tracks/piano/D2.wav',
            'D#2': 'Tracks/piano/Eb2.wav', 'E2': 'Tracks/piano/E2.wav', 'F2': 'Tracks/piano/F2.wav',
            'F#2': 'Tracks/piano/Gb2.wav', 'G2': 'Tracks/piano/G2.wav', 'G#2': 'Tracks/piano/Ab2.wav',
            'A2': 'Tracks/piano/A2.wav', 'A#2': 'Tracks/piano/Bb2.wav', 'B2': 'Tracks/piano/B2.wav',
            'C3': 'Tracks/piano/C3.wav', 'C#3': 'Tracks/piano/Db3.wav', 'D3': 'Tracks/piano/D3.wav',
            'D#3': 'Tracks/piano/Eb3.wav', 'E3': 'Tracks/piano/E3.wav', 'F3': 'Tracks/piano/F3.wav',
            'F#3': 'Tracks/piano/Gb3.wav', 'G3': 'Tracks/piano/G3.wav', 'G#3': 'Tracks/piano/Ab3.wav',
            'A3': 'Tracks/piano/A3.wav', 'A#3': 'Tracks/piano/Bb3.wav', 'B3': 'Tracks/piano/B3.wav',
            'C4': 'Tracks/piano/C4.wav', 'C#4': 'Tracks/piano/Db4.wav', 'D4': 'Tracks/piano/D4.wav',
            'D#4': 'Tracks/piano/Eb4.wav', 'E4': 'Tracks/piano/E4.wav', 'F4': 'Tracks/piano/F4.wav',
            'F#4': 'Tracks/piano/Gb4.wav', 'G4': 'Tracks/piano/G4.wav', 'G#4': 'Tracks/piano/Ab4.wav',
            'A4': 'Tracks/piano/A4.wav', 'A#4': 'Tracks/piano/Bb4.wav', 'B4': 'Tracks/piano/B4.wav',
            'C5': 'Tracks/piano/C5.wav', 'C#5': 'Tracks/piano/Db5.wav', 'D5': 'Tracks/piano/D5.wav',
            'D#5': 'Tracks/piano/Eb5.wav', 'E5': 'Tracks/piano/E5.wav', 'F5': 'Tracks/piano/F5.wav',
            'F#5': 'Tracks/piano/Gb5.wav', 'G5': 'Tracks/piano/G5.wav', 'G#5': 'Tracks/piano/Ab5.wav',
            'A5': 'Tracks/piano/A5.wav', 'A#5': 'Tracks/piano/Bb5.wav', 'B5': 'Tracks/piano/B5.wav',
            'C6': 'Tracks/piano/C6.wav', 'C#6': 'Tracks/piano/Db6.wav', 'D6': 'Tracks/piano/D6.wav',
            'D#6': 'Tracks/piano/Eb6.wav', 'E6': 'Tracks/piano/E6.wav', 'F6': 'Tracks/piano/F6.wav',
            'F#6': 'Tracks/piano/Gb6.wav', 'G6': 'Tracks/piano/G6.wav', 'G#6': 'Tracks/piano/Ab6.wav',
            'A6': 'Tracks/piano/A6.wav', 'A#6': 'Tracks/piano/Bb6.wav', 'B6': 'Tracks/piano/B6.wav',
            'C7': 'Tracks/piano/C7.wav', 'C#7': 'Tracks/piano/Db7.wav', 'D7': 'Tracks/piano/D7.wav',
            'D#7': 'Tracks/piano/Eb7.wav', 'E7': 'Tracks/piano/E7.wav', 'F7': 'Tracks/piano/F7.wav',
            'F#7': 'Tracks/piano/Gb7.wav', 'G7': 'Tracks/piano/G7.wav', 'G#7': 'Tracks/piano/Ab7.wav',
            'A7': 'Tracks/piano/A7.wav', 'A#7': 'Tracks/piano/Bb7.wav', 'B7': 'Tracks/piano/B7.wav',
            'C8': 'Tracks/piano/C8.wav',
        }
        self.preloaded_sounds = self.preload_sounds()
        self.file_queue = queue.Queue()
        self.input_active = False

    def preload_sounds(self):
        preloaded = {}
        for note, path in self.note_map.items():
            try:
                y, sr = librosa.load(path, sr=self.sr)
                y = add_effects(y, self.sr)
                preloaded[note] = y
            except Exception as e:
                print(f"Could not preload sound for {note}: {e}")
        return preloaded

    def import_file(self):
        if self.input_active:
            try:
                file_path = self.file_queue.get_nowait()
                if file_path:
                    with open(file_path, 'r') as file:
                        self.notes = []
                        for line in file:
                            self.notes.extend(line.strip().split())
                            self.notes.append('\n')
                    self.status_text = "Loading file..."
                    threading.Thread(target=self.load_audio_files).start()
                    self.input_active = False
                    return True
                else:
                    self.input_active = False
                    return False
            except queue.Empty:
                return False

        def file_dialog_thread(q):
            file_path = easygui.fileopenbox(filetypes=["*.txt"])
            q.put(file_path)

        self.input_active = True
        threading.Thread(target=file_dialog_thread, args=(self.file_queue,), daemon=True).start()
        return False

    def load_audio_files(self):
        note_spacing = int(self.sr * self.tempo)
        total_notes = 0
        newline_count = 0
        for note in self.notes:
            if note == '\n':
                newline_count += 1
            else:
                total_notes += 1
        
        estimated_length = (total_notes * note_spacing) + (newline_count * int(self.sr * 0.5))
        max_note_length = max((len(self.preloaded_sounds.get(n, np.array([]))) for n in self.preloaded_sounds), default=0)
        total_length = estimated_length + max_note_length
        
        self.combined_signal = np.zeros(total_length)
        self.note_timings = []
        
        current_position = 0
        current_time = 0
        
        for note in self.notes:
            if note == '\n':
                current_position += int(self.sr * 0.5)
                current_time += 0.5
                continue
            
            notes = note.split(',')
            self.note_timings.append((current_time, notes))
            
            for n in notes:
                if n in self.preloaded_sounds:
                    y = self.preloaded_sounds[n]
                    end_pos = current_position + len(y)
                    if end_pos > len(self.combined_signal):
                        self.combined_signal = np.pad(self.combined_signal, (0, end_pos - len(self.combined_signal)))
                    self.combined_signal[current_position:end_pos] += y
            
            current_position += note_spacing
            current_time += self.tempo
        
        if current_position < len(self.combined_signal):
            self.combined_signal = self.combined_signal[:current_position]
        
        self.status_text = "File imported"

    def play_music(self):
        if self.combined_signal is not None and not self.is_playing:
            self.is_playing = True
            threading.Thread(target=self._play_thread).start()

    def pause_music(self):
        if self.is_playing:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            self.is_playing = False

    def reset_music(self):
        self.pause_music()
        self.combined_signal = None
        self.notes = []
        self.status_text = "No file imported"
        self.current_position = 0
        self.current_notes.clear()

    def set_tempo(self, tempo):
        if self.is_playing:
            current_time = self.current_position / self.sr
            new_position = int(current_time * self.sr * (self.tempo / tempo))
            self.current_position = new_position
        self.tempo = tempo
        if self.notes:
            was_playing = self.is_playing
            if was_playing:
                self.pause_music()
            self.load_audio_files()
            if was_playing:
                self.play_music()

    def export_audio(self):
        if self.combined_signal is None:
            self.status_text = "No audio to export"
            return False
        self.status_text = "Exporting audio..."
        threading.Thread(target=self._export_audio_thread, daemon=True).start()
        return True

    def _export_audio_thread(self):
        try:
            file_path = easygui.filesavebox(
                default="exported_music.wav",
                filetypes=["*.wav"],
                title="Save Audio File"
            )
            if file_path:
                normalized_signal = np.int16(self.combined_signal * 32767)
                wavfile.write(file_path, self.sr, normalized_signal)
                self.status_text = f"Audio exported to {os.path.basename(file_path)}"
            else:
                self.status_text = "Export cancelled"
        except Exception as e:
            self.status_text = f"Error exporting audio: {str(e)}"

    def _play_thread(self, start_position=0):
        if self.combined_signal is None:
            return

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            current_time = self.current_position / self.sr
            self.current_notes = set()
            for t, notes in self.note_timings:
                if abs(t - current_time) < self.tempo / 2:
                    self.current_notes.update(notes)
            if self.current_position >= len(self.combined_signal):
                self.is_playing = False
                self.current_notes.clear()
                raise sd.CallbackStop()
            if len(self.combined_signal) - self.current_position < frames:
                data = self.combined_signal[self.current_position:]
                outdata[:len(data)] = data.reshape(-1, 1)
                outdata[len(data):] = 0
                raise sd.CallbackStop()
            else:
                data = self.combined_signal[self.current_position:self.current_position + frames]
                outdata[:] = data.reshape(-1, 1)
            self.current_position += frames

        try:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
            self.current_position = start_position
            self.stream = sd.OutputStream(channels=1, callback=callback, samplerate=self.sr)
            self.stream.start()
        except Exception as e:
            print(f"Error in _play_thread: {e}")
            self.is_playing = False

class UkulelePlayer:
    def __init__(self):
        self.is_playing = False
        self.tempo = 0.25
        self.status_text = "No file imported"
        self.current_chord = ''
        self.frames_num = 30
        self.notes = []
        self.current_position = 0
        self.combined_signal = None
        self.sr = 44100
        self.stream = None
        self.dict_chords_sounds = ukulele_notes_sounds
        self.loop_enabled = False
        self.preloaded_sounds = self.preload_sounds()
        self.file_queue = queue.Queue()
        self.input_active = False
        self.note_timings = []

    def preload_sounds(self):
        preloaded = {}
        for note in NOTES_LIST:
            try:
                y, sr = librosa.load(f'Tracks/ukelele/{note}.wav', sr=self.sr)
                y = add_effects(y, self.sr)
                preloaded[note] = y
            except Exception as e:
                print(f"Could not preload sound for {note}: {e}")
        return preloaded

    def import_file(self):
        if self.input_active:
            try:
                file_path = self.file_queue.get_nowait()
                if file_path:
                    with open(file_path, 'r') as file:
                        self.notes = []
                        for line in file:
                            self.notes.extend(line.strip().split())
                            self.notes.append('\n')
                    self.status_text = "Loading file..."
                    threading.Thread(target=self.load_audio_files).start()
                    self.input_active = False
                    return True
                else:
                    self.input_active = False
                    return False
            except queue.Empty:
                return False

        def file_dialog_thread(q):
            file_path = easygui.fileopenbox(filetypes=["*.txt"])
            q.put(file_path)

        self.input_active = True
        threading.Thread(target=file_dialog_thread, args=(self.file_queue,), daemon=True).start()
        return False

    def load_audio_files(self):
        note_spacing = int(self.sr * self.tempo * 2)
        total_notes = 0
        newline_count = 0
        for note in self.notes:
            if note == '\n':
                newline_count += 1
            else:
                total_notes += 1
        
        estimated_length = (total_notes * note_spacing) + (newline_count * int(self.sr * 0.5))
        max_note_length = max((len(self.preloaded_sounds.get(n, np.array([]))) for n in self.preloaded_sounds), default=0)
        total_length = estimated_length + max_note_length
        
        self.combined_signal = np.zeros(total_length)
        self.note_timings = []
        
        current_position = 0
        current_time = 0
        
        for note in self.notes:
            if note == '\n':
                current_position += int(self.sr * 0.5)
                current_time += 0.5
                continue
            
            self.note_timings.append((current_time, [note]))
            if note in self.preloaded_sounds:
                y = self.preloaded_sounds[note]
                end_pos = current_position + len(y)
                if end_pos > len(self.combined_signal):
                    self.combined_signal = np.pad(self.combined_signal, (0, end_pos - len(self.combined_signal)))
                self.combined_signal[current_position:end_pos] += y
            
            current_position += note_spacing
            current_time += self.tempo * 2
        
        if current_position < len(self.combined_signal):
            self.combined_signal = self.combined_signal[:current_position]
        
        self.status_text = f"Imported {len(self.notes)} notes"

    def export_audio(self):
        if self.combined_signal is None:
            self.status_text = "No audio to export"
            return False
        self.status_text = "Exporting audio..."
        threading.Thread(target=self._export_audio_thread, daemon=True).start()
        return True

    def _export_audio_thread(self):
        try:
            file_path = easygui.filesavebox(
                default="exported_music.wav",
                filetypes=["*.wav"],
                title="Save Audio File"
            )
            if file_path:
                normalized_signal = np.int16(self.combined_signal * 32767)
                wavfile.write(file_path, self.sr, normalized_signal)
                self.status_text = f"Audio exported to {os.path.basename(file_path)}"
            else:
                self.status_text = "Export cancelled"
        except Exception as e:
            self.status_text = f"Error exporting audio: {str(e)}"

    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        self.status_text = f"Loop {'enabled' if self.loop_enabled else 'disabled'}"

    def play_chord(self, chord_name):
        if chord_name in self.dict_chords_sounds:
            self.current_chord = chord_name
            self.dict_chords_sounds[chord_name].play(0, 1000)
            self.frames_num = 30

    def play_music(self):
        if self.combined_signal is not None and not self.is_playing:
            self.is_playing = True
            threading.Thread(target=self._play_thread).start()

    def pause_music(self):
        if self.is_playing:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            self.is_playing = False

    def reset_music(self):
        self.pause_music()
        self.combined_signal = None
        self.notes = []
        self.note_timings = []
        self.status_text = "No file imported"
        self.current_position = 0
        self.current_chord = ''
        self.frames_num = 30

    def set_tempo(self, tempo):
        if tempo <= 0:
            return
        if self.is_playing:
            current_time = self.current_position / self.sr
            new_position = int(current_time * self.sr * (self.tempo / tempo))
            self.current_position = new_position
        self.tempo = tempo
        if self.notes:
            was_playing = self.is_playing
            if was_playing:
                self.pause_music()
            self.load_audio_files()
            if was_playing:
                self.play_music()

    def update_frames(self):
        if self.frames_num > 0:
            self.frames_num -= 1
        if self.frames_num == 0:
            self.current_chord = ''
        return self.frames_num

    def _play_thread(self, start_position=0):
        if self.combined_signal is None:
            return

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            current_time = self.current_position / self.sr
            self.current_chord = ''
            for t, notes in self.note_timings:
                if abs(t - current_time) < (self.tempo * 2) / 2:
                    if notes[0] in NOTES_LIST:
                        self.current_chord = notes[0]
            if self.current_position >= len(self.combined_signal):
                if self.loop_enabled:
                    self.current_position = 0
                else:
                    self.is_playing = False
                    self.current_chord = ''
                    raise sd.CallbackStop()
            if len(self.combined_signal) - self.current_position < frames:
                data = self.combined_signal[self.current_position:]
                outdata[:len(data)] = data.reshape(-1, 1)
                outdata[len(data):] = 0
                if self.loop_enabled:
                    self.current_position = 0
                else:
                    self.is_playing = False
                    self.current_chord = ''
                    raise sd.CallbackStop()
            else:
                data = self.combined_signal[self.current_position:self.current_position + frames]
                outdata[:] = data.reshape(-1, 1)
            self.current_position += frames

        try:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
            self.current_position = start_position
            self.stream = sd.OutputStream(channels=1, callback=callback, samplerate=self.sr)
            self.stream.start()
        except Exception as e:
            print(f"Error in _play_thread: {e}")
            self.is_playing = False

class FlutePlayer:
    def __init__(self):
        self.is_playing = False
        self.tempo = 0.25
        self.status_text = "No file imported"
        self.current_note = ''
        self.notes = []
        self.current_position = 0
        self.combined_signal = None
        self.sr = 44100
        self.stream = None
        self.note_mapping = {
            'C1': 'do1', 'D1': 're1', 'E1': 'mi1', 'F1': 'fa1', 'G1': 'sol1', 'A1': 'la1', 'B1': 'si1',
            'C2': 'do2', 'D2': 're2', 'E2': 'mi2', 'F2': 'fa2', 'G2': 'sol2', 'A2': 'la2', 'B2': 'si2',
            'C3': 'do3', 'D3': 're3', 'E3': 'mi3', 'F3': 'fa3'
        }
        self.preloaded_sounds = self.preload_sounds()
        self.file_queue = queue.Queue()
        self.input_active = False
        self.note_timings = []

    def preload_sounds(self):
        preloaded = {}
        for piano_note, flute_note in self.note_mapping.items():
            try:
                y, sr = librosa.load(f'Tracks/flute/{flute_note}.wav', sr=self.sr)
                y = add_effects(y, self.sr)
                preloaded[piano_note] = y
            except Exception as e:
                print(f"Could not preload sound for {flute_note}: {e}")
        return preloaded

    def import_file(self):
        if self.input_active:
            try:
                file_path = self.file_queue.get_nowait()
                if file_path:
                    with open(file_path, 'r') as file:
                        self.notes = []
                        for line in file:
                            self.notes.extend(line.strip().split())
                            self.notes.append('\n')
                    self.status_text = "Loading file..."
                    threading.Thread(target=self.load_audio_files).start()
                    self.input_active = False
                    return True
                else:
                    self.input_active = False
                    return False
            except queue.Empty:
                return False

        def file_dialog_thread(q):
            file_path = easygui.fileopenbox(filetypes=["*.txt"])
            q.put(file_path)

        self.input_active = True
        threading.Thread(target=file_dialog_thread, args=(self.file_queue,), daemon=True).start()
        return False

    def load_audio_files(self):
        note_spacing = int(self.sr * self.tempo * 2)
        total_notes = 0
        newline_count = 0
        for note in self.notes:
            if note == '\n':
                newline_count += 1
            else:
                total_notes += 1
        
        estimated_length = (total_notes * note_spacing) + (newline_count * int(self.sr * 0.5))
        max_note_length = max((len(self.preloaded_sounds.get(n, np.array([]))) for n in self.preloaded_sounds), default=0)
        total_length = estimated_length + max_note_length
        
        self.combined_signal = np.zeros(total_length)
        self.note_timings = []
        
        current_position = 0
        current_time = 0
        
        for note in self.notes:
            if note == '\n':
                current_position += int(self.sr * 0.5)
                current_time += 0.5
                continue
            
            self.note_timings.append((current_time, [note]))
            if note in self.preloaded_sounds:
                y = self.preloaded_sounds[note]
                end_pos = current_position + len(y)
                if end_pos > len(self.combined_signal):
                    self.combined_signal = np.pad(self.combined_signal, (0, end_pos - len(self.combined_signal)))
                self.combined_signal[current_position:end_pos] += y
            
            current_position += note_spacing
            current_time += self.tempo * 2
        
        if current_position < len(self.combined_signal):
            self.combined_signal = self.combined_signal[:current_position]
        
        self.status_text = f"Imported {len(self.notes)} notes"

    def play_music(self):
        if self.combined_signal is not None and not self.is_playing:
            self.is_playing = True
            threading.Thread(target=self._play_thread).start()

    def pause_music(self):
        if self.is_playing:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            self.is_playing = False

    def reset_music(self):
        self.pause_music()
        self.combined_signal = None
        self.notes = []
        self.note_timings = []
        self.status_text = "No file imported"
        self.current_position = 0
        self.current_note = ''

    def set_tempo(self, tempo):
        if tempo <= 0:
            return
        if self.is_playing:
            current_time = self.current_position / self.sr
            new_position = int(current_time * self.sr * (self.tempo / tempo))
            self.current_position = new_position
        self.tempo = tempo
        if self.notes:
            was_playing = self.is_playing
            if was_playing:
                self.pause_music()
            self.load_audio_files()
            if was_playing:
                self.play_music()

    def export_audio(self):
        if self.combined_signal is None:
            self.status_text = "No audio to export"
            return False
        self.status_text = "Exporting audio..."
        threading.Thread(target=self._export_audio_thread, daemon=True).start()
        return True

    def _export_audio_thread(self):
        try:
            file_path = easygui.filesavebox(
                default="exported_music.wav",
                filetypes=["*.wav"],
                title="Save Audio File"
            )
            if file_path:
                normalized_signal = np.int16(self.combined_signal * 32767)
                wavfile.write(file_path, self.sr, normalized_signal)
                self.status_text = f"Audio exported to {os.path.basename(file_path)}"
            else:
                self.status_text = "Export cancelled"
        except Exception as e:
            self.status_text = f"Error exporting audio: {str(e)}"

    def _play_thread(self, start_position=0):
        if self.combined_signal is None:
            return

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            current_time = self.current_position / self.sr
            self.current_note = ''
            for t, notes in self.note_timings:
                if abs(t - current_time) < (self.tempo * 2) / 2:
                    if notes[0] in self.note_mapping:
                        self.current_note = self.note_mapping[notes[0]]
            if self.current_position >= len(self.combined_signal):
                self.is_playing = False
                self.current_note = ''
                raise sd.CallbackStop()
            if len(self.combined_signal) - self.current_position < frames:
                data = self.combined_signal[self.current_position:]
                outdata[:len(data)] = data.reshape(-1, 1)
                outdata[len(data):] = 0
                raise sd.CallbackStop()
            else:
                data = self.combined_signal[self.current_position:self.current_position + frames]
                outdata[:] = data.reshape(-1, 1)
            self.current_position += frames

        try:
            if self.stream is not None:
                self.stream.stop()
                self.stream.close()
            self.current_position = start_position
            self.stream = sd.OutputStream(channels=1, callback=callback, samplerate=self.sr)
            self.stream.start()
        except Exception as e:
            print(f"Error in _play_thread: {e}")
            self.is_playing = False