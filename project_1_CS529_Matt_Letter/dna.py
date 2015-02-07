#!/usr/bin/python
import copy

__author__ = 'matthewletter'

"""
data structure for holding a piece of DNA
"""


class DNAClass:
    """
    class set up
    dictionary_attribute_keys is a list of attributes used to scaffold the class
    """

    def __init__(self, attribute_list=None):
        self.dictionary = {}
        self.attribute_list = attribute_list

        # set each item in the dictionary to none
        for att in attribute_list:
            self.dictionary[att] = None

        #debug info
        #print "dictionary"
        #print self.dictionary

    """
    cleanup
    """

    def __del__(self):
        #print ("deconstructing buffer")
        pass

    """
    add actual values to dictionary
    """

    def build_dna_dictionary(self, dna_values):
        counter = 0

        for att in self.attribute_list:
            self.dictionary[att] = dna_values[counter]
            counter += 1

    """
    update attribute value.
    """

    def update_attribute_value(self, attribute, value):
        self.dictionary[attribute] = value

    """
    This method is designed to get the dictory associated with this sample.
    """

    def get_dictionary(self):
        return self.dictionary

    """
    This method is designed to get the value for specific value.
    """

    def get_value_at_attribute(self, attribute):
        return self.dictionary[attribute]


"""
used for testing
"""
if __name__ == "__main__":

    attributes = []
    attributeNum = 10
    for i in range(attributeNum):
        if i == attributeNum - 1:
            attributes.append("Promoter")
        else:
            attributes.append("Posistion-{0}".format(i + 1))
    print attributes
    obj = DNAClass(copy.deepcopy(attributes))
    del obj