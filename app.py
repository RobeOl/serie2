from flask import Flask, send_file, request
from flask_cors import CORS
from music21 import *
import tempfile
import os
from sequenza import genera_sequenza
from armonia import genera_armonia
import copy

app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:8000",
    "https://murosigma.it",
    "https://www.murosigma.it",
    "https://marcobittelli.it",
    "https://www.marcobittelli.it"
])

# 🔹 CACHE GLOBALE
last_stream = None
last_params = None
access_count = 0


def generate_music(start_note, sequence_type, tempo_type, harmony, harmony_type, ottave, bass_clef, bpm=100,
                   note_length=1,
                   interval=3, leap=-1,
                   interval1=3, leap1=3,
                   interval2=6, leap2=-2):

    s = genera_sequenza(sequence_type,tempo_type, note_length,
        interval,leap,
        interval1, leap1,
        interval2, leap2,
        ottave, bass_clef, start_note, harmony, harmony_type)

    if harmony and (tempo_type=="sequence-constrained" or tempo_type=="constant"):
        left = genera_armonia(sequence_type,harmony_type,s)
        # right hand
        right = stream.Part()
        for el in s:
            right.append(el)
        right.insert(0, instrument.Piano())
        ts = meter.TimeSignature('4/4')
        right.insert(0, ts)
        # calcola lunghezza pausa rigo superiore
        total_duration = right.duration.quarterLength
        measure_duration = ts.barDuration.quarterLength
        remainder = total_duration % measure_duration
        if remainder != 0:
            missing = measure_duration - remainder
            right.append(note.Rest(quarterLength=missing))
        
        left.insert(0, instrument.Piano())
        left.insert(0, clef.BassClef())
        # calcola lunghezza pausa rigo inferiore
        total_duration = left.duration.quarterLength
        remainder = total_duration % measure_duration
        if remainder != 0:
            missing = measure_duration - remainder
            left.append(note.Rest(quarterLength=missing))

        # === Score (grand staff) ===
        melody = stream.Score()
        melody.insert(0, right)
        melody.insert(0, left)
        melody.insert(0, key.Key('C'))
        melody.insert(0, metadata.Metadata())
        melody.metadata.title = ""
        melody.metadata.composer = ""
        melody.insert(0, instrument.Piano())
    else:
        melody = s
        ts = meter.TimeSignature('4/4')
        melody.insert(0, ts)
        total_duration = melody.duration.quarterLength
        measure_duration = ts.barDuration.quarterLength
        remainder = total_duration % measure_duration
        if remainder != 0:
            missing = measure_duration - remainder
            melody.append(note.Rest(quarterLength=missing))
        melody.insert(0, key.Key('C'))
        melody.insert(0, metadata.Metadata())
        melody.metadata.title = ""
        melody.metadata.composer = ""
        melody.insert(0, instrument.Piano())

    return melody

def invert_stream(s):
    inverted = stream.Part()

    prev_pitch = None
    last_new_pitch = None

    for el in s.recurse():

        if isinstance(el, chord.Chord):
            # inversione "verticale"
            pitches = [p.midi for p in el.pitches]
            axis = pitches[0]

            new_pitches = []
            for p in pitches:
                new_p = axis - (p - axis)
                while new_p < axis - 6:
                    new_p += 12
                while new_p > axis + 6:
                    new_p -= 12
                new_pitches.append(new_p)

            new_chord = chord.Chord(new_pitches, quarterLength=el.quarterLength)
            inverted.append(new_chord)

        elif isinstance(el, note.Note):

            if prev_pitch is None:
                new_note = note.Note(el.pitch, quarterLength=el.quarterLength)
                last_new_pitch = el.pitch.midi
            else:
                interval = el.pitch.midi - prev_pitch
                inv_interval = -interval
                new_pitch = last_new_pitch + inv_interval

                while abs(new_pitch - last_new_pitch) > 6:
                    if new_pitch < last_new_pitch:
                        new_pitch += 12
                    else:
                        new_pitch -= 12

                new_note = note.Note()
                new_note.pitch.midi = new_pitch
                new_note.quarterLength = el.quarterLength

                last_new_pitch = new_pitch

            prev_pitch = el.pitch.midi
            inverted.append(new_note)

        elif isinstance(el, note.Rest):
            inverted.append(note.Rest(quarterLength=el.quarterLength))

    return inverted

@app.route("/generate", methods=["POST"])
def generate_midi():
    global last_stream
    global last_params

    data = request.json

    s = generate_music(
        data.get("start_note"),
        data.get("sequence_type"),
        data.get("tempo"),
        data.get("harmony"),
        data.get("harmony_type"),
        data.get("octave", 1),
        data.get("bass_clef"),
        data.get("bpm", 100),
        float(data.get("note_length", 1)),
        data.get("interval", 0),
        data.get("leap", 0),
        data.get("interval1", 0),
        data.get("leap1", 0),
        data.get("interval2", 0),
        data.get("leap2", 0)
    )

    # 🔴 salva la sequenza reale (fondamentale)
    last_stream = copy.deepcopy(s)
    # salva ultimi parametri
    last_params = data

    tmp = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
    s.write('midi', fp=tmp.name)

    return send_file(tmp.name, mimetype="audio/midi")


@app.route("/score", methods=["POST"])
def generate_score():
    global last_stream

    if last_stream is None:
        return {"error": "No sequence generated yet"}, 400

    tmp = tempfile.NamedTemporaryFile(suffix=".musicxml", delete=False)
    last_stream.write('musicxml', fp=tmp.name)

    return send_file(tmp.name, mimetype="application/xml")

@app.route("/transform", methods=["POST"])
def invert_sequence():
    global last_stream

    if last_stream is None:
        return {"error": "No sequence generated yet"}, 400

    # 🎼 CASO CON ARMONIA
    if isinstance(last_stream, stream.Score):

        parts = list(last_stream.parts)

        right = parts[0]  # melodia

        # 1. inverti melodia
        inverted_melody = invert_stream(right)

        # 2. rigenera armonia
        new_left = genera_armonia(
            last_params.get("sequence_type"),
            last_params.get("harmony_type"),
        inverted_melody
        )
        
        # 3. ricostruisci score
        new_score = stream.Score()

        # mano destra
        new_score.insert(0, inverted_melody)

        # mano sinistra
        new_left.insert(0, instrument.Piano())
        new_left.insert(0, clef.BassClef())
        new_score.insert(0, new_left)

        # metadata
        new_score.insert(0, key.Key('C'))
        new_score.insert(0, metadata.Metadata())
        new_score.insert(0, instrument.Piano())
        new_score.metadata.title = ""
        new_score.metadata.composer = ""

        last_stream = copy.deepcopy(new_score)

        s = new_score

    # 🎼 CASO SENZA ARMONIA
    else:
        s = invert_stream(last_stream)
        s.insert(0, key.Key('C'))
        s.insert(0, metadata.Metadata())
        s.insert(0, instrument.Piano())
        s.metadata.title = ""
        s.metadata.composer = ""
        last_stream = copy.deepcopy(s)

    # 🎵 esporta MIDI
    tmp = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
    s.write('midi', fp=tmp.name)

    return send_file(tmp.name, mimetype="audio/midi")

@app.route("/health")
def health():
    return {"status": "ok"}, 200


port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)