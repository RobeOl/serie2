from music21 import *
import random
import copy


def f_octave(x, ottave, oct):
    if (ottave == 1) and (x.octave >= (oct + 2)):
        x.octave = oct
    elif (ottave == 2) and (x.octave >= (oct + 3)):
        x.octave = oct


def f_durata(x):
    x.duration.quarterLength = random.choice([1, 1/2, 1/4])


def genera_multidimensional(tipo, note_len, n_K, ottave, bass_clef, starting_note, harmony, harmony_type):
    """
    Genera una sequenza Multidimensionale con K intervalli per ciclo.

    Parametri
    ---------
    tipo           : str   – "sequence-constrained" | "length-constrained" | "constant" | "free"
    note_len       : float – durata nota (usata solo in modalità "constant")
    n_K            : list  – lista di K interi (intervalli in semitoni)
    ottave         : int   – 1 → 1 ottava, 2 → 2 ottave
    bass_clef      : bool  – trasponi 2 ottave sotto e usa chiave di basso
    starting_note  : int   – pitch-class 0-11 (0=C, 1=C#, …, 11=B)
    harmony        : bool  – riservato per coerenza con gli altri generatori
    harmony_type   : str   – riservato per coerenza con gli altri generatori

    Logica (da qualsiasi.py)
    ------------------------
    La sequenza parte dalla nota iniziale, applica K trasposizioni
    consecutive (un ciclo), poi ripete finché il pitch-class corrente
    coincide con quello di partenza.
    """

    K = len(n_K)
    if K == 0:
        return stream.Stream()

    c = note.Note(starting_note)
    if starting_note <= 6:
        c.octave = 4
    else:
        c.octave = 3

    oct = c.octave
    note1 = c
    notes = []

    # ── sequence-constrained ─────────────────────────────────────────────────
    # Il cambio di durata avviene una volta per ciclo di K note: sull'ultima
    # trasposizione del ciclo, prima del deepcopy. In questo modo ogni blocco
    # di K note ha una sola variazione ritmica, alla sua fine.
    if tipo == "sequence-constrained":
        f_durata(note1)
        notes.append(copy.deepcopy(note1))
        first_note = note1.name

        # primo ciclo
        for idx in range(K):
            note1.transpose(n_K[idx], inPlace=True)
            f_octave(note1, ottave, oct)
            if idx == K - 1:
                f_durata(note1)          # cambio durata prima del deepcopy
            notes.append(copy.deepcopy(note1))

        current_note = note1.name
        while current_note != first_note:
            for idx in range(K):
                note1.transpose(n_K[idx], inPlace=True)
                f_octave(note1, ottave, oct)
                if idx == K - 1:
                    f_durata(note1)
                notes.append(copy.deepcopy(note1))
            current_note = note1.name

    # ── length-constrained ───────────────────────────────────────────────────
    elif tipo == "length-constrained":
        conta = 1
        note_number = random.choice([2, 3, 5, 6])

        f_durata(note1)
        notes.append(copy.deepcopy(note1))
        first_note = note1.name

        for idx in range(K):
            note1.transpose(n_K[idx], inPlace=True)
            f_octave(note1, ottave, oct)
            if conta == note_number:
                f_durata(note1)
                conta = 1
            else:
                conta += 1
            notes.append(copy.deepcopy(note1))

        current_note = note1.name
        while current_note != first_note:
            for idx in range(K):
                note1.transpose(n_K[idx], inPlace=True)
                f_octave(note1, ottave, oct)
                if conta == note_number:
                    f_durata(note1)
                    conta = 1
                else:
                    conta += 1
                notes.append(copy.deepcopy(note1))
            current_note = note1.name

    # ── constant ─────────────────────────────────────────────────────────────
    elif tipo == "constant":
        note1.duration.quarterLength = note_len
        notes.append(copy.deepcopy(note1))
        first_note = note1.name

        for idx in range(K):
            note1.transpose(n_K[idx], inPlace=True)
            f_octave(note1, ottave, oct)
            notes.append(copy.deepcopy(note1))

        current_note = note1.name
        while current_note != first_note:
            for idx in range(K):
                note1.transpose(n_K[idx], inPlace=True)
                f_octave(note1, ottave, oct)
                notes.append(copy.deepcopy(note1))
            current_note = note1.name

    # ── free ─────────────────────────────────────────────────────────────────
    else:
        f_durata(note1)
        notes.append(copy.deepcopy(note1))
        first_note = note1.name

        for idx in range(K):
            note1.transpose(n_K[idx], inPlace=True)
            f_octave(note1, ottave, oct)
            f_durata(note1)
            notes.append(copy.deepcopy(note1))

        current_note = note1.name
        while current_note != first_note:
            for idx in range(K):
                note1.transpose(n_K[idx], inPlace=True)
                f_octave(note1, ottave, oct)
                f_durata(note1)
                notes.append(copy.deepcopy(note1))
            current_note = note1.name

    # ── costruzione stream ───────────────────────────────────────────────────
    melody = stream.Stream()

    if bass_clef:
        melody.insert(0, clef.BassClef())
        melody.append(notes)
        melody = melody.transpose(-24)
    else:
        melody.append(notes)

    return melody
