from music21 import *
import copy

def make_chord_with_min_third(A, B):
    # calcola distanza in semitoni (melodica A → B)
    semitones = interval.Interval(A, B).semitones

    # se inferiore a 3 semitoni (terza minore)
    if abs(semitones) < 3:
        A = A.transpose(-12)  # abbassa A di un'ottava

    return chord.Chord([A, B])


def fill_to_measure(left, beats_per_measure=4):
    # Aggiunge una pausa finale per completare l'ultima battuta.
    total = sum(el.duration.quarterLength for el in left.notesAndRests)
    position_in_measure = total % beats_per_measure
    if position_in_measure > 0:
        remainder = beats_per_measure - position_in_measure
        r = note.Rest()
        r.duration.quarterLength = remainder
        left.append(r)


def add_final_chord(left, notes, N):
    # Aggiunge il bicordo finale: ultima nota una e due ottave sotto.
    last = copy.deepcopy(notes[N])
    low1 = copy.deepcopy(notes[N])
    low2 = copy.deepcopy(notes[N])
    low1.octave = last.octave - 1
    low2.octave = last.octave - 2
    Cf = chord.Chord([low2, low1])
    Cf.duration.quarterLength = last.duration.quarterLength
    left.append(Cf)


def genera_armonia(seq_type, harmony_type, s):
    # caso binary
    if seq_type == "Binary":
        left = stream.Part()
        # check se inizia con pausa, perché proveniente da Retrograde
        for el in s.notesAndRests:
            if el.isRest:
                left.append(el)
            else:
                break

        notes = s.notes
        N = len(notes) - 1
        nn = 0

        # accordi su coppie di note
        while nn < N:
            X1 = copy.deepcopy(notes[nn])
            X1.octave = 3
            X2 = copy.deepcopy(notes[nn + 1])
            X2.octave = 3
            durata = X1.duration.quarterLength + X2.duration.quarterLength
            Cx = chord.Chord([X1, X2])
            Cx.duration.quarterLength = durata
            left.append(Cx)
            nn = nn + 2

        # bicordo finale: ultima nota una e due ottave sotto
        add_final_chord(left, notes, N)

        # pausa per completare l'ultima battuta
        fill_to_measure(left)

    # caso quaternary
    elif seq_type == "Quaternary":
        left = stream.Part()
        # check se inizia con pausa, perché proveniente da Retrograde
        for el in s.notesAndRests:
            if el.isRest:
                left.append(el)
            else:
                break

        notes = s.notes
        N = len(notes) - 1
        nn = 0

        if harmony_type == "classic":
            # accordi su quattro note
            while nn < N:
                X1 = copy.deepcopy(notes[nn])
                X1.octave = 3
                X2 = copy.deepcopy(notes[nn + 1])
                X2.octave = 3
                X3 = copy.deepcopy(notes[nn + 2])
                X3.octave = 3
                X4 = copy.deepcopy(notes[nn + 3])
                X4.octave = 3
                durata = (X1.duration.quarterLength + X2.duration.quarterLength +
                          X3.duration.quarterLength + X4.duration.quarterLength)
                Cx = chord.Chord([X1, X2, X3, X4])
                Cx.duration.quarterLength = durata
                left.append(Cx)
                nn = nn + 4

        elif harmony_type == "onbeat":
            # accordi su due note (1-3 e 2-4)
            while nn < N:
                X1 = copy.deepcopy(notes[nn])
                X1.octave = 3
                X2 = copy.deepcopy(notes[nn + 1])
                X2.octave = 3
                X3 = copy.deepcopy(notes[nn + 2])
                X3.octave = 3
                X4 = copy.deepcopy(notes[nn + 3])
                X4.octave = 3
                durata13 = X1.duration.quarterLength + X3.duration.quarterLength
                durata24 = X2.duration.quarterLength + X4.duration.quarterLength
                Cx = make_chord_with_min_third(X1, X3)
                Cx.duration.quarterLength = durata13
                left.append(Cx)
                Cx = make_chord_with_min_third(X2, X4)
                Cx.duration.quarterLength = durata24
                left.append(Cx)
                nn = nn + 4

        elif harmony_type == "offbeat":
            # accordi su due note (2-4 e 1-3)
            while nn < N:
                X1 = copy.deepcopy(notes[nn])
                X1.octave = 3
                X2 = copy.deepcopy(notes[nn + 1])
                X2.octave = 3
                X3 = copy.deepcopy(notes[nn + 2])
                X3.octave = 3
                X4 = copy.deepcopy(notes[nn + 3])
                X4.octave = 3
                durata24 = X2.duration.quarterLength + X4.duration.quarterLength
                durata13 = X1.duration.quarterLength + X3.duration.quarterLength
                Cx = make_chord_with_min_third(X2, X4)
                Cx.duration.quarterLength = durata24
                left.append(Cx)
                Cx = make_chord_with_min_third(X1, X3)
                Cx.duration.quarterLength = durata13
                left.append(Cx)
                nn = nn + 4
            
        # bicordo finale: ultima nota una e due ottave sotto
        add_final_chord(left, notes, N)

        # pausa per completare l'ultima battuta
        fill_to_measure(left)

    # caso senary
    elif seq_type == "Senary":
        left = stream.Part()
        # check se inizia con pausa, perché proveniente da Retrograde
        for el in s.notesAndRests:
            if el.isRest:
                left.append(el)
            else:
                break

        notes = s.notes
        N = len(notes) - 1
        nn = 0

        if harmony_type == "classic":
            # accordi su tre note (una si una no dell'esacordo)
            while nn < N:
                X1 = copy.deepcopy(notes[nn])
                X1.octave = 3
                X2 = copy.deepcopy(notes[nn + 1])
                X2.octave = 3
                X3 = copy.deepcopy(notes[nn + 2])
                X3.octave = 3
                X4 = copy.deepcopy(notes[nn + 3])
                X4.octave = 3
                X5 = copy.deepcopy(notes[nn + 4])
                X5.octave = 3
                X6 = copy.deepcopy(notes[nn + 5])
                X6.octave = 3
                durata = (X1.duration.quarterLength + X2.duration.quarterLength +
                          X3.duration.quarterLength + X4.duration.quarterLength +
                          X5.duration.quarterLength + X6.duration.quarterLength)
                Cx = chord.Chord([X1, X3, X5])
                Cx.duration.quarterLength = durata
                left.append(Cx)
                nn = nn + 6

        elif harmony_type == "onbeat":
            # accordi su tre note (1-3-5 e 2-4-6)
            while nn < N:
                X1 = copy.deepcopy(notes[nn])
                X1.octave = 3
                X2 = copy.deepcopy(notes[nn + 1])
                X2.octave = 3
                X3 = copy.deepcopy(notes[nn + 2])
                X3.octave = 3
                X4 = copy.deepcopy(notes[nn + 3])
                X4.octave = 3
                X5 = copy.deepcopy(notes[nn + 4])
                X5.octave = 3
                X6 = copy.deepcopy(notes[nn + 5])
                X6.octave = 3
                durata135 = X1.duration.quarterLength + X3.duration.quarterLength + X5.duration.quarterLength
                durata246 = X2.duration.quarterLength + X4.duration.quarterLength + X6.duration.quarterLength
                Cx = chord.Chord([X1, X3, X5])
                Cx.duration.quarterLength = durata135
                left.append(Cx)
                Cx = chord.Chord([X2, X4, X6])
                Cx.duration.quarterLength = durata246
                left.append(Cx)
                nn = nn + 6

        elif harmony_type == "offbeat":
            # accordi su due note (2-4 e 1-3)
            while nn < N:
                X1 = copy.deepcopy(notes[nn])
                X1.octave = 3
                X2 = copy.deepcopy(notes[nn + 1])
                X2.octave = 3
                X3 = copy.deepcopy(notes[nn + 2])
                X3.octave = 3
                X4 = copy.deepcopy(notes[nn + 3])
                X4.octave = 3
                X5 = copy.deepcopy(notes[nn + 4])
                X5.octave = 3
                X6 = copy.deepcopy(notes[nn + 5])
                X6.octave = 3
                durata246 = X2.duration.quarterLength + X4.duration.quarterLength + X6.duration.quarterLength
                durata135 = X1.duration.quarterLength + X3.duration.quarterLength + X5.duration.quarterLength
                Cx = chord.Chord([X2, X4, X6])
                Cx.duration.quarterLength = durata246
                left.append(Cx)
                Cx = chord.Chord([X1, X3, X5])
                Cx.duration.quarterLength = durata135
                left.append(Cx)
                nn = nn + 6

        # bicordo finale: ultima nota una e due ottave sotto
        add_final_chord(left, notes, N)

        # pausa per completare l'ultima battuta
        fill_to_measure(left)

    return left
