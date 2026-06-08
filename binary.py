from music21 import *
import random
import copy
from utility import f_octave,f_durata


def genera_binary(tipo,note_len,i,j,ottave,bass_clef,starting_note,discard_closure=False,midi_min=None,midi_max=None):
	c = note.Note(starting_note)

	if starting_note <= 7:
		c.octave = 4
	else:
		c.octave = 3

	oct = c.octave

	notes = []

	# first interval, starting with C4
	note1 = c

	if tipo=="sequence-constrained":
		# sequence-constrained
	
		f_durata(note1)
		notes.append(copy.deepcopy(note1))
		prima = note1.name

		note1.transpose(i,inPlace=True)
		f_octave(note1, ottave, oct, midi_min, midi_max)
		notes.append(copy.deepcopy(note1))
		seconda = note1.name
		first_couple = [prima,seconda]
	
		condition = True
		# following leaps/intervals
		while condition: 
			note1.transpose(j,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			f_durata(note1)
			notes.append(copy.deepcopy(note1))
			prima = note1.name

			note1.transpose(i,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			notes.append(copy.deepcopy(note1))
			seconda = note1.name
		
			current_couple = [prima,seconda]
			condition = (current_couple!=first_couple)
			
	elif tipo=="length-constrained":
		# length-constrained
		conta = 1
		note_number = random.choice([2,3,5,6])

		f_durata(note1)
		notes.append(copy.deepcopy(note1))
		prima = note1.name

		note1.transpose(i,inPlace=True)
		f_octave(note1, ottave, oct, midi_min, midi_max)
		if conta==note_number:
			f_durata(note1)
			conta=1
		else:
			conta = conta+1

		notes.append(copy.deepcopy(note1))
		seconda = note1.name
		first_couple = [prima,seconda]

		condition = True
		# following leaps/intervals
		while condition: 
			note1.transpose(j,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			if conta==note_number:
				f_durata(note1)
				conta=1
			else:
				conta = conta+1
			notes.append(copy.deepcopy(note1))
			prima = note1.name

			note1.transpose(i,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			if conta==note_number:
				f_durata(note1)
				conta=1
			else:
				conta = conta+1
			notes.append(copy.deepcopy(note1))
			seconda = note1.name
		
			current_couple = [prima,seconda]
			condition = (current_couple!=first_couple)
			
	elif tipo=="constant":
		# constant
		c.duration.quarterLength = note_len
		notes.append(copy.deepcopy(note1))
		prima = note1.name

		note1.transpose(i,inPlace=True)
		f_octave(note1, ottave, oct, midi_min, midi_max)
		notes.append(copy.deepcopy(note1))
		seconda = note1.name
		first_couple = [prima,seconda]

		condition = True
		# following leaps/intervals
		while condition: 
			note1.transpose(j,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			notes.append(copy.deepcopy(note1))
			prima = note1.name

			note1.transpose(i,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			notes.append(copy.deepcopy(note1))
			seconda = note1.name
		
			current_couple = [prima,seconda]
			condition = (current_couple!=first_couple)
			
	else:
		# free
		f_durata(note1)
		notes.append(copy.deepcopy(note1))
		prima = note1.name

		note1.transpose(i,inPlace=True)
		f_octave(note1, ottave, oct, midi_min, midi_max)
		f_durata(note1)
		notes.append(copy.deepcopy(note1))
		seconda = note1.name
		first_couple = [prima,seconda]
	
		condition = True
		# following leaps/intervals
		while condition: 
			note1.transpose(j,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			f_durata(note1)
			notes.append(copy.deepcopy(note1))
			prima = note1.name

			note1.transpose(i,inPlace=True)
			f_octave(note1, ottave, oct, midi_min, midi_max)
			f_durata(note1)
			notes.append(copy.deepcopy(note1))
			seconda = note1.name
		
			current_couple = [prima,seconda]
			condition = (current_couple!=first_couple)
			
	melody = stream.Stream()
	# remove last element
	notes.pop()
	# remove cycle closure
	if discard_closure:
		notes.pop()
	if bass_clef:
		melody.insert(0, clef.BassClef())
		melody.append(notes)
		melody_bass = melody.transpose(-24)
		melody = melody_bass
	else:
		melody.append(notes)
   
	return(melody)
