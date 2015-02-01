#!/usr/bin/python

import sample
import copy

"""
This file contains the method to read a file, and return the value as sample class.
"""

class readFile:
	"""
	Constructor.
	fileName is the file to read.
	"""
	def __init__(self, file_name):
		self.f = open(file_name, "r+")
		self.attribute = []
		self.content = []
		self.attributeNum = 58

	"""
	This method is called to read one line
	"""
	def read_single_line(self):
		text = self.f.readline()
		result = []

		for word in text.split():
			for letter in word:
				result.append(letter)

		return result

	"""
	This method is called to initialize the first line, which is attribute line.
	"""
	def generate_file_attribute(self):
		for i in range(self.attributeNum - 1):
			self.attribute.append("pos{0}".format(i+1))
		
		self.attribute.append("isPromotor")

		return self.attribute

	"""
	This method is called to get attributes for the table
	"""
	def get_attributes(self):
		return self.attribute

	"""
	This method is called to read data from the table.
	"""
	def read_file_content(self):
		self.generate_file_attribute()

		while True:
			text = self.read_single_line()
			
			if len(text) == 0:
				break

			element = sample.Sample(copy.deepcopy(self.attribute))
			element.initValue(list(text))
			self.content.append(element)

		return self.content

"""Test part"""

#x = readFile("training.txt")
#x.read_file_content()
#print len(x.read_single_line())
#for item in x.content:
#	print item.get_dictionary()
