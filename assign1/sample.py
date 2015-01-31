#!/usr/bin/python

"""
This class defines one sample for input.
You need to define all attributes in this class.
After that you can initialize the values used in this class using a list.
You can get a dictionary about all values in the class.
Besides, you can get value for specific attribute.
"""
class Sample:
    """
    Constructor.
    Key arguments:
    attribute_list -- is the attribute used to build this class.
    """
    def __init__(self, attribute_list):
        self.table = {}
        self.attribute_list = attribute_list

        for attribute in attribute_list:
            self.table[attribute] = None

    """
    This method is used to initialize all values, be sure that all values should be in order.
    """
    def initValue(self, value_list):
        counter = 0

        for attribute in self.attribute_list:
            self.table[attribute] = value_list[counter]
            counter = counter + 1

    """
    This method is called to update the value for specific attribute with given value.
    """
    def updateValue(self, attribute, value):
        self.table[attribute] = value

    """
    This method is designed to get the dictory associated with this sample.
    """
    def getTableMap(self):
        return self.table

    """
    This method is designed to get the value for specific value.
    """
    def getValue(self, attribute):
        return self.table[attribute]
