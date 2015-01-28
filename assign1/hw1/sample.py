#!/usr/bin/python

"""
This class defines one sample for input. You need to define all attributes in this class.
After that you can initialize the values used in this class using a list.
You can get a dictionary about all values in the class. Besides, you can get value for specific attribute.
"""
class Sample:
    """
    Constructor.

    Key arguments:
    attribute_list -- is the attribute list used to build one sample.
    """
    def __init__(self, attribute_list):
        self.table = {}
        self.attribute_list = attribute_list

        for attribute in attribute_list:
            self.table[attribute] = None

    """
    This method is used to initialize values for all attributes. Be sure that all values should be in order.

    Key arguments:
    value_list -- contains all values for this sample in order.
    """
    def init_value(self, value_list):
        counter = 0

        for attribute in self.attribute_list:
            self.table[attribute] = value_list[counter]
            counter = counter + 1

    """
    This method is called to update the value for specific attribute with given value.

    Key arguments:
    attribute -- is the attribute name to be updated.
    value -- is the new value set to the attribute.
    """
    def update_value(self, attribute, value):
        self.table[attribute] = value

    """
    This method is designed to get the dictionary associated with this sample.

    return a dictionary with attribute as key and generic acid or promotor type as value.
    """
    def get_tablemap(self):
        return self.table

    """
    This method is designed to get the value for specific attribute.

    return the value for specific attribute.
    """
    def get_value(self, attribute):
        return self.table[attribute]
