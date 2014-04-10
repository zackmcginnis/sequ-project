#!/usr/bin/env python
#zack mcginnis
#cs300

import subprocess
import unittest

class sequCL4Tests(unittest.TestCase):

		def startEndOneFloat(self):
			text = subprocess.getoutput('./sequ.py 1 3.0')
			self.assertEqual(text, '1.0\n2.0\n3.0')
		
		def startEndOneFloat2(self):
			text = subprocess.getoutput('./sequ.py 1.0 4')
			self.assertEqual(text, '1.0\n2.0\n3.0\n4.0')

		def startEndIncAllInt(self):
			text = subprocess.getoutput('./sequ.py 1 2 5')
			self.assertEqual(text, '1\n3\n5')

		def startEndIncAllFloat(self):
			text = subprocess.getoutput('./sequ.py 1.0 2.0 5.0')
			self.assertEqual(text, '1.0\n3.0\n5.0')

		def startFloatEndIncInts(self):
			text = subprocess.getoutput('./sequ.py 1.0 2 4')
			self.assertEqual(text, '1.0\n3.0')

		def twoIntsEndFloat(self):
			text = subprocess.getoutput('./sequ.py 1 2 5.0')
			self.assertEqual(text, '1.0\n3.0\n5.0')

		def twoFloatsIncInt(self):
			text = subprocess.getoutput('./sequ.py 0.0 1.5 4.0')
			self.assertEqual(text, '0.0\n1.5\n3.0')

		def twoFloatsEndInt(self):
			text = subprocess.getoutput('./sequ.py 1.0 2.0 6')
			self.assertEqual(text, '1.0\n3.0\n5.0')

		def oneArgEndInt(self):
			text = subprocess.getoutput('./sequ.py 3')
			self.assertEqual(text, '1\n2\n3')

		def oneArgEndFloat(self):
			text = subprocess.getoutput('./sequ.py 3.0')
			self.assertEqual(text, '1.0\n2.0\n3.0')

		def separatorDash(self):
			text = subprocess.getoutput('./sequ.py -s - 1 5')
			self.assertEqual(text, '1-2-3-4-5')

		def equalWidthInts(self):
			text = subprocess.getoutput('./sequ.py -w 1 50 101')
			self.assertEqual(text, '001\n051\n101')

		def padSpaces(self):
			text = subprocess.getoutput('./sequ.py -P 0 400 800 1200')
			self.assertEqual(text, '   0\n 400\n 800\n1200')
	
		def padChar(self):
			text = subprocess.getoutput('./sequ.py -p x 0 400 1200')
			self.assertEqual(text, 'xxx0\nx400\nx800\n1200')
			
		def equalWidthFloats(self):
			text = subprocess.getoutput('./sequ.py -w 1.0 50.5 101.0')
			self.assertEqual(text, '001.0\n051.5\n101.0')

		def testRoman(self):
			text = subprocess.getoutput('./sequ.py -F roman i v')
			self.assertEqual(text, 'i\nii\niii\niv\nv')
		
		def testRoman1(self):
			text = subprocess.getoutput('./sequ.py -F ROMAN i v')
			self.assertEqual(text, 'I\nII\nIII\nIV\nV')	
			
		def testAlpha(self):
			text = subprocess.getoutput('./sequ.py -F alpha a e')
			self.assertEqual(text, 'a\nb\nc\nd\ne')
		
		def testAlpha1(self):
			text = subprocess.getoutput('./sequ.py -F ALPHA i v')
			self.assertEqual(text, 'A\nB\nC\nD\nE')	

		def testFloat(self):
			text = subprocess.getoutput('./sequ.py -F float 0 3')
			self.assertEqual(text, '0.0\n1.0\n2.0\n3.0')	

		def testFloat1(self):
			text = subprocess.getoutput('./sequ.py -F FLOAT 0 3')
			self.assertEqual(text, '0.0\n1.0\n2.0\n3.0')

		def testArabic(self):
			text = subprocess.getoutput('./sequ.py -F arabic 0 3')
			self.assertEqual(text, '0\n1\n2\n3')	

		def testArabic1(self):
			text = subprocess.getoutput('./sequ.py -F ARABIC 0 3')
			self.assertEqual(text, '0\n1\n2\n3')	

		def testNumberLines(self):
			text = subprocess.getoutput('./sequ.py -n myfile.txt 5')
			self.assertEqual(text, '5 this\n6 is\n7 my\n8 file')				

if __name__ == '__main__':
    unittest.main()
	