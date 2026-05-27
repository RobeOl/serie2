import random
from music21 import *

def f_octave(x, ottave, oct):
    midi_start = (oct + 1) * 12       # MIDI del Do dell'ottava di partenza (C4=60 se oct=4)
    midi_min   = midi_start - 12      # sempre 1 ottava sotto il Do di partenza
    midi_max   = midi_start + ottave * 12  # ottave=1 → C5, ottave=2 → C6

    while x.pitch.midi < midi_min:
        x.pitch.midi += 12
    while x.pitch.midi > midi_max:
        x.pitch.midi -= 12

def f_durata(x):
    x.duration.quarterLength = random.choice([1, 1/2, 1/4])
