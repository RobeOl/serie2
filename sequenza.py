import random
from music21 import *
from binary import genera_binary
from quaternary import genera_quaternary
from senary import genera_senary
from ternary import genera_ternary
from multidimensional import genera_multidimensional


def genera_sequenza(seq_type, tipo, note_len,
                    i, j,
                    i1, j1, i2, j2,
                    ii1, jj1, ii2, jj2, ii3, jj3,
                    int_i, int_j, int_k,
                    ottave, bass_clef, starting_note,
                    multi_values=None,
                    discard_closure=False,
                    midi_min=None, midi_max=None):
    #
    # Dispatcher verso il generatore corretto in base a seq_type.

    # Parametri aggiuntivi rispetto alla versione precedente
    # -------------------------------------------------------
    # multi_values : list[int] | None
    #     Lista di K interi (intervalli in semitoni) per la modalità
    #     Multidimensional.  Se None o lista vuota viene usata [0].
    # discard_closure : bool
    #     Se True, rimuove l'ultima nota della sequenza (uguale alla prima).
    #

    if seq_type == "Binary":
        s = genera_binary(tipo, note_len, i, j,
                          ottave, bass_clef, starting_note,
                          discard_closure=discard_closure,
                          midi_min=midi_min, midi_max=midi_max)

    elif seq_type == "Quaternary":
        s = genera_quaternary(tipo, note_len, i1, j1, i2, j2,
                              ottave, bass_clef, starting_note,
                              discard_closure=discard_closure,
                              midi_min=midi_min, midi_max=midi_max)

    elif seq_type == "Senary":
        s = genera_senary(tipo, note_len, ii1, jj1, ii2, jj2, ii3, jj3,
                          ottave, bass_clef, starting_note,
                          discard_closure=discard_closure)

    elif seq_type == "Multidimensional":
        n_K = multi_values if multi_values else [0]
        s = genera_multidimensional(tipo, note_len, n_K,
                                    ottave, bass_clef, starting_note,
                                    discard_closure=discard_closure)

    else:  # Ternary (default)
        s = genera_ternary(tipo, note_len, int_i, int_j, int_k,
                           ottave, bass_clef, starting_note,
                           discard_closure=discard_closure)

    return s
