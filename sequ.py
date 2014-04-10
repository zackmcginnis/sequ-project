#!/usr/bin/env python
#zack mcginnis
#cs300
import argparse
import sys
import codecs
from alpha import Alpha
from roman import Roman 
from itertools import count #for numberlines

def whichType(input):
	try:
		return intOrFloat(input)
	except argparse.ArgumentTypeError:
		pass
	
	try:
		return Roman(input)
	except ValueError:
		pass
	
	try:
		return Alpha(input)
	except ValueError:
		pass		

	raise argparse.ArgumentTypeError('input must be of type roman, alpha, int or float')
			
#list of acceptable words and their corresponding char representatives		
FORMAT_CHARWORDS = {
	'roman'  : 'r', 
	'ROMAN'  : 'R',	
    'alpha'  : 'a', 
	'ALPHA'  : 'A',
    'arabic' : 'f', 
	'ARABIC' : 'f',	
    'float'  : 'f', 
	'FLOAT'  : 'f',	
    }
#list of acceptable words and their corresponding type
FORMAT_WORDTYPE = {		
    int      : 'arabic', 
	'arabic' :  int,	
    float    : 'float',  
	'float'  :  float,
	Roman    : 'roman',  
	'roman'  :  Roman,	
    Alpha    : 'alpha',  
	'alpha'  :  Alpha,
	}				
			
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
	
#class to define --number-lines arg when specified			
class NumberTheLines(argparse.Action):
    def __call__(self, PARSER, namespace, values, option_string=None):	
        namespace.__setattr__(self.dest, values)	
        namespace.end = None			
					
#using argparse, we retrieve start, end, inc, format word, and file from user input	
#in addition, we will take optional formatting args from group_1, and an 	
#optional formatting arg from group_2			
PARSER = argparse.ArgumentParser(	
    description='Print numbers from FIRST to LAST, in steps of INCREMENT')

PARSER.add_argument(	
    '-F', 
	'--format-word',	
	help='one word arg which indicates the type of sequence (alpha,roman,arabic, or float)',
	dest='formatWord',
	choices=FORMAT_CHARWORDS.keys())
	
PARSER.add_argument(
    '--version',	
    action='version',
	help='the version',
	version='2.0')	
				
GROUP_1 = PARSER.add_mutually_exclusive_group()

GROUP_1.add_argument(
	'-n',
	'--number-lines',
	help='number each line of file supplied at command line using start/inc args',
	dest='file',
	action=NumberTheLines,
	const=sys.stdin,
	nargs='?',
	type=argparse.FileType('r+'))	

GROUP_1.add_argument(
    '-f', 
	'--format', 
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
    help='pad with leading spaces',
    dest='width',
    const=' ', 
	action='store_const')

GROUP_2 = PARSER.add_mutually_exclusive_group()	
#for separator, default value may change if
#--number-lines is specified	
try:
	args = PARSER.parse_known_args()[0]
	default=' ' if args.file else '\n'
except IndexError:
	default='\n'	

GROUP_2.add_argument(	
    '-s', 
	'--separator', 
    help='output will be separated by string provided',	
    dest='separator',	
	default=default,
    type=str)	
	
GROUP_2.add_argument(
    '-W', 
	'--words',	
    help='output will print on a line separated by spaces',	
    dest='separator',
    const=' ', 
	action='store_const')
		
args = PARSER.parse_known_args()[0]	
#determine arg types of start/end/inc	
try:
    startEndIncType = FORMAT_WORDTYPE[str(args.formatWord).lower()]
except KeyError:
    startEndIncType = whichType

PARSER.add_argument(
    'start', 	
    help='The first number of the seq',
    type=startEndIncType, 
	default=startEndIncType(1), 
	nargs='?')
		
PARSER.add_argument(	
    'increment', 
    help='The step size of the seq',
    type=startEndIncType, 
	default=startEndIncType(1), 
	nargs='?')
#since end is not necessary when --number-lines is given
if not args.file:	
	PARSER.add_argument(
		'end', 	
		help='The last number of the seq',
		type=startEndIncType)	
		
#this function places the given separator between
#every iteration of a created iterable object			
def space(separator, iterable):

    item = iter(iterable)
    val = next(item)
    yield val
    for i in item:
        yield separator
        yield i	

#this function will allow single chars to be accepted as padding args	
#by removing escaping when the char is given as an arg at the command line.		
def unEscape(string):
    return codecs.getdecoder('unicode_escape')(string)[0]	
	
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

#for any number specified in the args, this function will return
#the longest number by the roman format.  
#e.g. for input of 11 (xi), the longest roman length is 8 (viii)		
def romanLength(num):
    rLength = [1, 2, 3, 8, 18, 28, 38, 88, 188, 288, 388, 488, 988]
    num = int(Roman(num))	
    x = 0	
    for i in sorted(rLength):
        if num%1000 <= i:
            break
        x += 1
    return (x + 1) + (num // 1000)				
	
def main():

	args = PARSER.parse_args()

	#this block will determine the maximum length 
	#of the given start/end/inc args by converting
	#them to string types.  The args are then divided at
	#the decimal point (i.e. 23.5235 divided to 23 and 5235)
	#the length of the string (if applicable) is taken and the largest
	#will be returned for later consumption.
	decLength = max(map(lambda parts: len(parts[1]) if len(parts) == 2 
													else 0, map(lambda num: str(num).split('.'), 
					[args.start, args.end, args.increment])))
	#assign which arg is specified if/when --number-lines is provided
	defArg = args.start if args.file else args.end
	
    #this block will determine the type of format word from our list
	#type will be inferred otherwise
	try:
		formatType = FORMAT_WORDTYPE[args.formatWord.lower()]
	except (KeyError, AttributeError):
		formatType = type(defArg)
		formatType = float if formatType is int else formatType
    #this block will determine the type of format word from our list
	#if a char is given as a format word arg
	#type will be inferred otherwise
	try:
		formatChar = FORMAT_CHARWORDS[args.formatWord]
	except KeyError:
		aWord = FORMAT_WORDTYPE[formatType]	
		aWord = aWord.lower() if str(defArg).islower() else aWord.upper()
		formatChar = FORMAT_CHARWORDS[aWord]
	#building off of the romanLength function, we determine the maximum string length
	#produced by the given args.  romanLength is used for roman, alpha length will always be 1
	#and appropriate conversions are set in place for int and float.
	if formatChar in ['f']:
		maxL = len(str(int(defArg))) + decLength
		maxL += 1 if decLength else 0 
	elif formatChar in ['a', 'A']:
		maxL = 1					
	elif formatChar in ['r', 'R']:	
		maxL = romanLength(defArg)
	
	#if --format was provided at command line it will be used as specified
	#else, the formatString will be created using width provided
	if args.formatString:
		formatString = '{{{}}}'.format(args.formatString)
	else:
		formatString = '{{:{}{}{}{}}}'.format('{}>{}'.format(
			args.width, maxL) if args.width else '',
			'.' if formatChar == 'f' else '',
			decLength if formatChar == 'f' else '', formatChar)	
	
	separator = unEscape(args.separator)
	#mapList is created by placing the start/end/inc args into the floatrange function
	#to make a list of elements.  The list is then mapped according to the specified
	#formatString and formatWordType.
	#when --number-lines is given, we will utilize python's count function
	#to implement it within the map
	mapList = map(formatString.format, map(formatType, 
				count(args.start, args.increment) if args.file 
					else
						floatRange(float(args.start), (float(args.end)+1), 
						  float(args.increment))))
    #implement --number-lines if specified, else utilize read in specified separator
	#and map into the space function
	if args.file: 
		for i, line in zip(mapList, args.file):
			print('{}{}{}'.format(i, separator, line), end='')
	else:
		for i in space(separator, mapList):
			print(i, end='')
		print()	
	#python exit sequence
if __name__ == '__main__':
	#exit with correct status
    try:
        main()
    except SystemExit:
        sys.exit(1)
    else:
        sys.exit(0)	
		