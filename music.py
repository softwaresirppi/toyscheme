from numpy import zeros, sin, linspace, pi
from sounddevice import play, wait
from toyscheme_objects import SchemeNil
from math import floor, ceil

sound = None
sample_rate = 8000

def clamp(minimum, x, maximum):
    return min(maximum, max(minimum, x))

def begin_music(duration):
    global sound
    duration = float(duration)
    sound = zeros(int(duration * sample_rate))
    print(sound.shape)
    return SchemeNil()

def play_sine_wave(freq, amplitude, start, end):
    global sound
    freq, amplitude, start, end = float(freq), float(amplitude), float(start), float(end)
    start = clamp(0, start, len(sound) / sample_rate)
    end = clamp(0, end, len(sound) / sample_rate)
    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)
    t = linspace(start, end, end_sample - start_sample, endpoint=False)
    sound[start_sample:end_sample] += sin(t * 2 * pi * freq) * amplitude
    return SchemeNil()

def end_music():
    global sound
    play(sound, samplerate=sample_rate)
    wait()
    return SchemeNil()

# open_music()
# open_chord(0.5)
# square_note(440, 0.5)
# close_chord()
# open_chord(0.25)
# noise_note(0.5)
# close_chord()
# open_chord(0.5)
# square_note(440, 0.5)
# close_chord()
# close_music()