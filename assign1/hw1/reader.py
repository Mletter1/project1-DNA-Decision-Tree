#!/usr/bin/python

import sample
import copy

"""
This file contains the method to read a file data, and return the value as sample class.
"""
class readFile:
    """
    Constructor.

    Key arguments:
    fileName -- is the file to read.
    """
    def __init__(self, file_name):
        self.f = open(file_name, "r+")
        self.attribute = []
        self.content = []
        self.attributeNum = 58

    #This code is used for test accuracy improvement
    # 	def get_max_percentage(self, list):
    # 		gc = 0
    #
    # 		for word in list:
    # 			if word is 'c' or 'g':
    # 				gc += 1
    #
    # 		if (1.0 * gc/ len(list)) > 0.5:
    # 			return "c"
    # 		else:
    # 			return "a"

    """
    This method is called to read one line from the file.

    return a list containing all letters for one sequence.
    """
    def read_single_line(self):
        text = self.f.readline()

        result = []

        for word in text.split():
            for letter in word:
                result.append(letter)

        return result

    """
    This method is called to initialize the attributes for each DNA sequence. It includes
    57 generic acid position and one attribute to indicate if the sequence is promotor.

    return a list containing all attributes name.
    """
    def generate_file_attribute(self):
        for i in range(self.attributeNum - 1):
            self.attribute.append("pos{0}".format(i+1))

        self.attribute.append("isPromotor")

        return self.attribute

    """
    This method is called to get attributes for the each sequence.

    return attribute list.
    """
    def get_attributes(self):
        return self.attribute

    """
    This method is called to read data from the file and create attributes for the
    sequence read.

    return a list containing all sequences read from the file as sample instances.
    """
    def read_file_content(self):
        self.generate_file_attribute()

        #read line from file
        for line in self.f:
            #reset the list every time
            result = []

            for word in line.split():

                for letter in word:
                    result.append(letter)
            element = sample.Sample(copy.deepcopy(self.attribute))#
            element.init_value(list(result))
            self.content.append(element)
        return self.content
