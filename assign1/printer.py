#!/usr/bin/python

import sample

"""
This file is used to print the result using a root_node node.
"""

class ShowResult:
    """
    Constrcutor.
    Key arguments:
    root_node -- is the root_node node for the decision tree.
    """
    def __init__(self, root):
        self.root = root
    """
    This method is called to show one node.
    """
    def show(self, node, num, title):
        self.generate_space(num)
        print "{0} ".format(title),
        print "{0}/{1}".format(node.parent_property, node.pre_attribute)

    """
    This method is called to print the space before each node.
    """
    def generate_space(self, num):
        for i in range(num-1):
            print "\t",

    """
    This method is called to print the whole tree.
    """
    def generateResult(self, node, num1, num2, title):
        self.show(node, num1, title + "." + 'num2')
        counter = 1

        for item in node.child_list.values():
            self.generateResult(item, num1+1, counter, title + "." + 'num2')
            counter = counter + 1

    """
    This method is called to print the whole tree after the instance has been build.
    """
    def run(self):
        self.generateResult(self.root, 1, 1, "")
