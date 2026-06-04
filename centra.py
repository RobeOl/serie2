import copy
from music21 import stream, note

# Range consentito: C3 (MIDI 48) – C6 (MIDI 84)
# MIDI_MIN = 48   # C3
# MIDI_MAX = 84   # C6
# MIDI_MIN = 60   # C4
# MIDI_MAX = 96   # C7
MIDI_MIN = 52   # E3
MIDI_MAX = 88   # E6


def centra_stream(s: stream.Part, midi_min: int = None, midi_max: int = None) -> stream.Part:
    if midi_min is None:
        midi_min = MIDI_MIN
    if midi_max is None:
        midi_max = MIDI_MAX
    # Prende un stream.Part (es. il risultato di invert_stream) e trasla
    # nota per nota verso l'alto o verso il basso di ottave intere (multipli
    # di 12 semitoni) in modo che ogni nota ricada nell'intervallo C3–C6
    # (MIDI 48–84).

    # Se lo span della melodia è contenibile in C3–C6, tutta la melodia viene
    # traslata di un unico shift globale (i rapporti di ottava tra le note
    # restano invariati).

    # Se lo span supera 36 semitoni (impossibile contenere in C3–C6 con un
    # solo shift), ogni singola nota viene corretta individualmente: viene
    # spostata di quante ottave servono per portarla dentro il range, senza
    # toccare le note già dentro.

    # --- raccoglie tutti i MIDI delle note (ignora pause) ---
    midi_pitches = [
        el.pitch.midi
        for el in s.recurse()
        if isinstance(el, note.Note)
    ]

    if not midi_pitches:
        centered = stream.Part()
        for el in s.recurse(classFilter=('Note', 'Rest')):
            centered.append(copy.deepcopy(el))
        return centered

    lowest  = min(midi_pitches)
    highest = max(midi_pitches)
    span    = highest - lowest

    centered = stream.Part()

    if span <= (midi_max - midi_min):
        shift = 0

        # Porta lowest dentro il range
        while lowest + shift < midi_min:
            shift += 12
        while lowest + shift > midi_max:
            shift -= 12

        # Se highest sfora in alto, scendi di ottave
        while highest + shift > midi_max:
            shift -= 12

        # Verifica che dopo l'aggiustamento lowest non sia uscito sotto:
        # se lo è, non esiste uno shift a multipli di 12 che contenga
        # entrambi gli estremi → fallback a correzione per nota (Caso 2).
        if lowest + shift < midi_min:
            for el in s.recurse(classFilter=('Note', 'Rest')):
                new_el = copy.deepcopy(el)
                if isinstance(new_el, note.Note):
                    m = new_el.pitch.midi
                    while m < midi_min:
                        m += 12
                    while m > midi_max:
                        m -= 12
                    new_el.pitch.midi = m
                centered.append(new_el)
            return centered

        for el in s.recurse(classFilter=('Note', 'Rest')):
            new_el = copy.deepcopy(el)
            if isinstance(new_el, note.Note):
                new_el.pitch.midi += shift
            centered.append(new_el)

    else:
        # ── CASO 2: correzione per nota ───────────────────────────────────
        # Lo span supera il range C3–C6: non è possibile un unico shift.
        # Ogni nota viene spostata individualmente di quante ottave servono
        # per portarla dentro [MIDI_MIN, MIDI_MAX].
        for el in s.recurse(classFilter=('Note', 'Rest')):
            new_el = copy.deepcopy(el)
            if isinstance(new_el, note.Note):
                m = new_el.pitch.midi
                while m < midi_min:
                    m += 12
                while m > midi_max:
                    m -= 12
                new_el.pitch.midi = m
            centered.append(new_el)

    return centered
