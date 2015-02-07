#!/usr/bin/python


"""
This file is used to print the result using a root_node node.
"""


class ShowResult:
    """
    give this constructor the root_node_of_tree of the tree you
    want to find info about
    """

    def __init__(self, root_node_of_tree):
        self.root_node_of_tree = root_node_of_tree

    """
    This method is called to show one node.
    """

    def show(self, node, num, title):
        self.generate_space(num)
        print "{0} ".format(title),
        print "{0}/{1}".format(node.parent_property, node.pre_attribute)

    """
    print space
    """

    def generate_space(self, num):
        for i in range(num - 1):
            print " ",

    """
    This method is called to print the whole tree.
    """

    def generateResult(self, node, num1, num2, title):
        self.show(node, num1, title + "." + '')
        counter = 1

        for item in node.child_list.values():
            self.generateResult(item, num1 + 1, counter, title + "." + '')
            counter += 1


    """
    print tree
    """

    def run(self):
        self.generateResult(self.root_node_of_tree, 1, 1, "")
