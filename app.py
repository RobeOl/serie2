from flask import Flask, send_file, request
from flask_cors import CORS
from music21 import *
import tempfile
import os
# from binary import genera_binary
from quaternary import genera_quaternary

app = Flask(__name__)
CORS(app)

def generate_midi(start_note, sequence_type, tempo_type, harmony,
                   note_length=1,
                   interval=3, leap=-1,
                   interval1=3, leap1=3,
                   interval2=6, leap2=-2):

    if sequence_type == "Binary":
        s = genera_binary(tempo_type, note_length, interval, leap, start_note)
    else:
        s = genera_quaternary(tempo_type, note_length,
                              interval1, leap1,
                              interval2, leap2,
                              start_note)

    s.insert(0, metadata.Metadata())
    s.metadata.title = ""
    s.metadata.composer = ""

    s.insert(0, instrument.Piano())

    return s


@app.route("/generate", methods=["POST"])
def generate_midi():
    data = request.json

    s = generate_music(
        data["start_note"],
        data["sequence_type"],
        data["tempo"],
        data["harmony"],
        float(data.get("note_length", 1)),
        data.get("interval", 0),
        data.get("leap", 0),
        data.get("interval1", 0),
        data.get("leap1", 0),
        data.get("interval2", 0),
        data.get("leap2", 0),
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".mid", delete=False)
    s.write('midi', fp=tmp.name)

    return send_file(tmp.name, mimetype="audio/midi")


@app.route("/score", methods=["POST"])
def generate_score():
    data = request.json

    s = generate_music(
        data["start_note"],
        data["sequence_type"],
        data["tempo"],
        data["harmony"],
        float(data.get("note_length", 1)),
        data.get("interval", 0),
        data.get("leap", 0),
        data.get("interval1", 0),
        data.get("leap1", 0),
        data.get("interval2", 0),
        data.get("leap2", 0),
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".musicxml", delete=False)
    s.write('musicxml', fp=tmp.name)

    return send_file(tmp.name, mimetype="application/xml")


port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)