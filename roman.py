#!/usr/bin/env python
#zack mcginnis
#cs300

#list/definition of roman numeral representations
#and corresponding integer values
ROMAN_CONVERSION = {
  1     : 'i',  4     : 'iv', 5     : 'v',
  9     : 'ix', 10    : 'x',  40    : 'xl',
  50    : 'l',  90    : 'xc', 100   : 'c',
  500   : 'd',  1000  : 'm'
 }
#Roman class will manipulate roman numeral and integer input to
#print sequence in traditional roman numeral fashion
class Roman(object):  
    def __init__(self, num):
        if type(num) is Roman: #constructor
            self._roman = num._roman
            return
        try:	
            self._roman = num 
            _ = int(self)
            return	
        except (AttributeError, ValueError):	
            pass
			
        num = int(num)
        if num <= 0:
            raise ValueError('value must be greater than zero')	
        self._roman = ''
        for i in reversed(sorted(ROMAN_CONVERSION)):
            self._roman += ROMAN_CONVERSION[i] * (num // i)
            num %= i
        return
		
    def __repr__(self):
        return "Roman('{}')".format(str(self))		
		
    def __float__(self):
        return float(int(self))
		
    def __int__(self):
        num = 0
        roman = self._roman.lower()
        for i in reversed(sorted(ROMAN_CONVERSION, key=lambda a: 
				len(ROMAN_CONVERSION[a]))):
            while ROMAN_CONVERSION[i] in roman:
                num += i
                roman = roman.replace(ROMAN_CONVERSION[i], '', 1)
        if roman:
            raise ValueError('must be valid roman numeral')
        return num
						
    def __str__(self):
        return str(self._roman)
		
    def __len__(self):
        return len(str(self))

    def __add__(self, other):
        return Roman(int(self) + int(other))

    def __format__(self, aFormat):
        aChar = aFormat[-1]
        if aChar not in ['r', 'R']:
            raise ValueError("format code unknown".format(aChar, type(self)))
		#upper/lowercase transition based on specified format
        up_low = str.upper if str.isupper(aChar) else str.lower
        return format(up_low(str(self)), aFormat[:-1])
	
