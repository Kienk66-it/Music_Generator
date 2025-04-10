import numpy as np

def add_effects(audio_signal, sr):
    def echo(signal, sr=44100, delay=0.025, decay=0.6, num_echoes=3):
        delay_samples = int(sr * delay)
        impulse_length = delay_samples * num_echoes + 1
        impulse = np.zeros(impulse_length)
        impulse[0] = 1
        for i in range(1, num_echoes + 1):
            impulse[delay_samples * i] = decay ** i
        
        n = len(signal) + len(impulse) - 1
        signal_fft = np.fft.fft(signal, n)
        impulse_fft = np.fft.fft(impulse, n)
        result = np.real(np.fft.ifft(signal_fft * impulse_fft))[:len(signal)]
        return result
    
    def fade_in(audio, duration=0.1):
        fade_samples = int(sr * duration)
        fade_curve = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] *= fade_curve
        return audio

    def fade_out(audio, duration=0.2):
        fade_samples = int(sr * duration)
        fade_curve = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] *= fade_curve
        return audio

    audio_with_echo = echo(audio_signal)
    audio_with_fade = fade_in(audio_with_echo)
    return fade_out(audio_with_fade)