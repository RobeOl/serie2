import random
from music21 import *

def f_octave(x, ottave, oct, midi_min=None, midi_max=None):
    if midi_min is not None and midi_max is not None:
        # Usa il range degli slider del frontend
        lo = midi_min
        hi = midi_max
    else:
        # Fallback al comportamento originale
        midi_start = (oct + 1) * 12
        lo = midi_start - 12
        hi = midi_start + ottave * 12

    while x.pitch.midi < lo:
        x.pitch.midi += 12
    while x.pitch.midi > hi:
        x.pitch.midi -= 12

def f_durata(x):
    x.duration.quarterLength = random.choice([1, 1/2, 1/4])
