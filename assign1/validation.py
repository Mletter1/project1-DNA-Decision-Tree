#!/usr/bin/python

import reader

"""
This file is used to validate the ID algorithm
"""

class Validate:
	"""
	Constructor.
	"""
	def __init__(self, file_name, interval):
		self.reader = reader.readFile(file_name)
		self.reader.read_file_content()


"""test part"""
x = Validate("validation.txt")

print x.reader.get_attributes()
print x.reader.content
