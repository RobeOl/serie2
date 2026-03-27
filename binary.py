from music21 import *
import random
import copy


def f_octave(x):
    # limit notes to octaves 4-5
    if x.octave==6:
        x.octave=4

def f_durata(x):
    x.duration.quarterLength = random.choice([1, 1/2, 1/4])
	
def genera_binary(i,j):
	c = note.Note("C4")

	notes = []

	# first interval, starting with C4
	note1 = c

	# free
	f_durata(note1)
	notes.append(copy.deepcopy(note1))
	prima = note1.name

	note1.transpose(i,inPlace=True)
	f_octave(note1)
	f_durata(note1)
	notes.append(copy.deepcopy(note1))
	seconda = note1.name
	first_couple = [prima,seconda]
	
	condition = True
	# following leaps/intervals
	while condition: 
		note1.transpose(j,inPlace=True)
		f_octave(note1)
		f_durata(note1)
		notes.append(copy.deepcopy(note1))
		prima = note1.name

		note1.transpose(i,inPlace=True)
		f_octave(note1)
		f_durata(note1)
		notes.append(copy.deepcopy(note1))
		seconda = note1.name
		
		current_couple = [prima,seconda]
		condition = (current_couple!=first_couple)
		
	melody = stream.Stream()

	# remove last element
	notes.pop()
	melody.append(notes)

	return(melody)