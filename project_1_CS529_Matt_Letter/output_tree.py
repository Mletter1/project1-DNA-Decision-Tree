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
    print a node.
    """

    def show(self, current_dna_n, space, base):
        self.offset_space(space)

        print "{0} ".format(base),

        print "{0}/{1}".format(current_dna_n.parent_property, current_dna_n.pre_attribute)

    """
    print space
    """

    def offset_space(self, offset):
        for space in range(offset - 1):
            print " ",

    """
    This method is called to print the whole tree.
    """

    def print_tree(self, node, num1, num2, title):
        self.show(node, num1, title + "." + '')
        tracker = 1

        for dna in node.child_list.values():
            self.print_tree(dna, num1 + 1, tracker, title + "." + '')
            tracker += 1


    """
    print tree
    """

    def run(self):
        self.print_tree(self.root_node_of_tree, 1, 1, "")
