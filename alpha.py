#!/usr/bin/env python
#zack mcginnis
#cs300
#english alphabet input/output
class Alpha:
	#initialize
	def __init__(self, input):
		try:
			input = chr(int(input)%26+ord('a')-1)
		except ValueError:
			if type(input) is str:
				if len(input) is not 1:
					raise ValueError("input must be a single char")
				
		if input.isalpha():
			self._input = input
		else:
			raise ValueError("input must be a letter in the english alphabet")	
	
	def __repr__(self):
		return "Alpha('{}')".format(self._input)
		
	def __float__(self):
		return float(int(self))	
	
	def __str__(self):
		return str(self._input)
		
	def __int__(self):
		default = ord('a') if self._input.islower() else ord('A')
		return ord(self._input) - default + 1
		
	def __add__(self, val):
		return Alpha(int(self)+int(val))
		
	def __format__(self, aFormat):
		aChar = aFormat[-1]
		if aChar not in ['a', 'A']:
			raise ValueError("format code unknown".format(aChar, type(self)))
		#for specified format char upper or lower case is decided
		up_low = str.upper if str.isupper(aChar) else str.lower
		return format(up_low(str(self)), aFormat[:-1])		