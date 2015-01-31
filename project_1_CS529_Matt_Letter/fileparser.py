#!/usr/bin/env python
import copy

__author__ = 'Matthew letter'

"""
A utilities class used for importing DNA files and objectafying them
"""


class ParserClass:
    """Constructs a file_buffer
    builds data elements to be filled once subsequent methods are called

    """
    def __init__(self, file_name="data/training.txt", number_of_attributes=58):
        print ("setting up file parser")
        self.attributes = []
        self.data_elements = []  # stores input as nodes
        self.file_buffer = open(file_name, "r+")
        self.attributeNum = number_of_attributes

    """
    close buffer
    """

    def __del__(self):
        print ("deconstructing buffer")
        self.file_buffer.close()
    """
    initialize the attributes

    return list of attributes
    """
    def build_attributes(self):
        for i in range(self.attributeNum):
            if i == self.attributeNum -1:
                self.attributes.append("isPromotor")
            else:
                self.attributes.append("pos{0}".format(i+1))

        print self.attributes
        return self.attributes


    """
    read file and build attributes from sequence read.

    return list of samples.
    """
    def parse_file(self):
        self.build_attributes()
        # read line from file
        for line in self.file_buffer:
            #reset the list every time
            result = []
            for word in line.split():
                #print word
                for letter in word:
                    #print letter
                    result.append(letter)
        #     element = sample.Sample(copy.deepcopy(self.attributes))  #
        #     element.init_value(list(result))
        #     self.content.append(element)
        # return self.content

    """
    return attribute list.
    """
    def get_attributes(self):
        return self.attributes


"""
used for testing
"""
if __name__ == "__main__":
    obj = ParserClass()
    obj.parse_file()
    del obj