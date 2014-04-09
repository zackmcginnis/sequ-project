#!/usr/bin/env python

#zack mcginnis

import argparse
import sys
import codecs
from alpha import Alpha
from roman import Roman
from itertools import count

class NumberLines(argparse.Action):
    def __call__(self, PARSER, namespace, values, option_string=None):	
        namespace.__setattr__(self.dest, values)	
        namespace.end = 1

def whichType(input):
    try:
        return Roman(input)
    except ValueError:	
        pass

    try:	
        return Alpha(input)
    except ValueError:
        pass		

    try:	
        return intOrFloat(input)
    except argparse.ArgumentTypeError:
        pass
		
    raise argparse.ArgumentTypeError(
            'input must be of type roman, alpha, int or float')
	
#we need to create a function which differentiates between	
#ints and floats based on args specified by user.  
#this function will check for a decimal in the args, and
#label each arg accordingly.  the type of each arg is stored
#in start, end, or increment			
def intOrFloat(input):
    if '.' in str(input):
        argType = float	
    else:	
        argType = int	
    try:
        return argType(input)	
    except ValueError:
        raise argparse.ArgumentTypeError('input must be an integer or float value')
	
#this function stores the specified --pad arg	
#as a string. Using the unEscape function, single character	
#args can be utilized without conflict.  If --pad arg is more	
#than one char, we raise an error. 		
def padType(string):
    string = unEscape(string)	
    if len(string) == 1:
        return string
    raise argparse.ArgumentTypeError('arg must be one char')
				
FORMAT_WORDS = {
	'roman'  : 'r', 
	'ROMAN'  : 'R',	
    'alpha'  : 'a', 
	'ALPHA'  : 'A',
    'arabic' : 'f', 
	'ARABIC' : 'f',	
    'float'  : 'f', 
	'FLOAT'  : 'f',	
    }

FORMAT_WORDTYPE = {	
    Roman : 'roman',  
	'roman'  : Roman,	
    Alpha : 'alpha',  
	'alpha'  : Alpha,	
    int   : 'arabic', 
	'arabic' : int,	
    float : 'float',  
	'float'  : float
	}	
					
#using argparse-+, we retrieve start, end, increment, and format word from user input	
#in addition, we will take optional formatting args from group_1, and an 	
#optional formatting arg from group_2			
	
PARSER = argparse.ArgumentParser(	
    description='Print numbers from FIRST to LAST, in steps of INCREMENT')

PARSER.add_argument(	
    '-F', 
	'--format-word',	
	help='one word arg which indicates the type of sequence (alpha,roman,arabic, or float)',
	dest='format_word',	
	choices = FORMAT_WORDS.keys())
	
PARSER.add_argument(
    '--version',	
    action='version', 
	version='2.0')	
				
GROUP_1 = PARSER.add_mutually_exclusive_group()

GROUP_1.add_argument(
	'-n',
	'--number-lines',
	dest='file',
	action=NumberLines,
	const=sys.stdin,
	nargs='?',
	type=argparse.FileType('r+'))	

GROUP_1.add_argument(
    '-f', 
	'--format', 
	metavar='FORMAT',
    help='python floating-point FORMAT',
    dest='formatString',
    type=str)
		
GROUP_1.add_argument(
    '-w', 
	'--equal-width',
    help='pad with leading zeroes',
    dest='width',
    const='0', 
	action='store_const')		
		
GROUP_1.add_argument(
    '-p', 
	'--pad', 	
    help='pad with the padding provided',
    dest='width',	
    type=padType)
		
GROUP_1.add_argument(
    '-P', 
	'--pad-spaces',
    help='equalize width by padding with leading spaces',
    dest='width',
    const=' ', 
	action='store_const')

GROUP_2 = PARSER.add_mutually_exclusive_group()	
	
try:
	args = PARSER.parse_known_args()[0]
	default=' ' if args.file else '\n'
except IndexError:
	default='\n'	

GROUP_2.add_argument(	
    '-s', 
	'--separator', 
	metavar='STRING',
    help='use the STRING to separate numbers',	
    dest='separator',	
	default=default,
    type=str)	
	
GROUP_2.add_argument(
    '-W', 
	'--words',	
    help='Output the sequence as a single space-separeted line of words',	
    dest='separator',
    const=' ', 
	action='store_const')
	

		
args = PARSER.parse_known_args()[0]	
	
try:
    argument_type = FORMAT_WORDTYPE[
            str(args.format_word).lower()]
except KeyError:
    argument_type = whichType

PARSER.add_argument(
    'start', 
	metavar='START',	
    help='The first number',
    type=argument_type, 
	default=argument_type(1), 
	nargs='?')
		
PARSER.add_argument(	
    'increment', 
	metavar='INCREMENT',
    help='The step size',
    type=argument_type, 
	default=argument_type(1), 
	nargs='?')

if not args.file:	
	PARSER.add_argument(
		'end', 
		metavar='END',	
		help='The last number',
		type=argument_type)	
		

#this function manipulates the start, end, and increment args and returns
#the sequence of numbers in type float	
def floatRange(start, end, increment=1.0):

	if start > end:
		return
	else:
		x = start
		while x < end:
			yield float(x)
			x += increment
		
def space(separator, iterable):

    item = iter(iterable)
    val = next(item)
    yield val
    for i in item:
        yield separator
        yield i
		
def longest_roman(n):
    """ Return the length of the longest roman number given a number """
    lengths = [1, 2, 3, 8, 18, 28, 38, 88, 188, 288, 388, 488, 988]
    n = int(Roman(n))	
    i = 0	
    for v in sorted(lengths):
        if n%1000 <= v:
            break
        i += 1
    return (i + 1) + (n // 1000)		

#this function will allow single chars to be accepted as padding args	
#by removing escaping when the char is given as an arg at the command line.		
def unEscape(string):
    return codecs.getdecoder('unicode_escape')(string)[0]	
	
def main():

	args = PARSER.parse_args()
	
	fractional_length = max(
        map(lambda parts: len(parts[1]) if len(parts) == 2 else 0,
            map(lambda num: str(num).split('.'), 
                [args.start, args.end, args.increment])))
	
    # Determine the format type
	try:
		format_type = FORMAT_WORDTYPE[args.format_word.lower()]
	except (KeyError, AttributeError):
		format_type = type(args.end)
		format_type = float if format_type is int else format_type
				
    # Determine the format character	
	try:
		formatChar = FORMAT_WORDS[args.format_word]
	except KeyError:
		word = FORMAT_WORDTYPE[type(args.end)]	
		word = word.lower() if str(args.end).islower() else word.upper()
		formatChar = FORMAT_WORDS[word]
		
    # The length of the largest number.
	if formatChar in ['f']:
		max_length = len(str(int(args.end))) + fractional_length
		max_length += 1 if fractional_length else 0 # for the '.'
	elif formatChar in ['r', 'R']:	
		max_length = longest_roman(args.end)
	elif formatChar in ['a', 'A']:
		max_length = 1	

		#in our if statement, if a format was specified, then that 
        #format will be passed into formatString.  
        #in our elif statement, if a width (specified in padding) was provided, it will be
        #placed passed into formatString
        #else, formatString will be empty when no format is provided	
	if args.formatString:
		formatString = '{{{}}}'.format(args.formatString)
	else:
        # Else construct the format by the options given
		formatString = '{{:{}{}{}{}}}'.format(
			'{}>{}'.format(args.width, max_length) if args.width else '',
			'.' if formatChar == 'f' else '',
			fractional_length if formatChar == 'f' else '',
			formatChar)	
				
	separator = unEscape(args.separator)
	
    # The following statement creates a list of integers using the
    # range specified by first, last, and increment. The map
    # transforms the list into a list of interger strings using the
    # format given. separate places the separator between each element.
	sequence = map(formatString.format,  # Apply format
			   map(format_type,        # Apply type
			   count(args.start, args.increment) if args.file else
			   floatRange(float(args.start), (float(args.end)+1), 
						  float(args.increment))))
    
	if args.file: 
		for i, line in zip(sequence, args.file):
			print('{}{}{}'.format(i, separator, line), end='')
	else:
		for i in space(separator, sequence):
			print(i, end='')
		print()	
	
if __name__ == '__main__':

    try:
        main()
    except SystemExit:
        sys.exit(1)
    else:
        sys.exit(0)	
		