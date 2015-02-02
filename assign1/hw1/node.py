#!/usr/bin/python

import helper

"""
This class is node class which contains the node in decision tree.
"""
class Node:
    """
    Constructor

    Keyword arguments:
    dictionary_attribute_keys -- is the attributes list for the input data.
    found_attribute --  is the attributes list used so far for classification.
    parent_property -- is the catalog from the parent.
    current_dna_list  -- is the list of samples to separate.
    classification_key -- is the attribute name used for concept definition.
    confidence_interval -- is the p-value for testing.
    """
    def __init__(self, attribute_list, found_attribute, parent_property, current_list, concept_string, compare_value):
        self.attribute_list = attribute_list
        self.found_attribute = found_attribute
        self.current_list = current_list
        self.child_list = {}
        self.parent_property = parent_property
        self.concept_string = concept_string
        self.parent_entropy = helper.get_set_entropy(current_list, concept_string)
        self.pre_attribute = ""
        self.cal_gain = 0
        self.cat_list_final = {}
        self.positive = 0
        self.negative = 0
        self.compare_value = compare_value

    """
    This method is used to calculate which attribute to choose.

    return true if there is an attribute for classification, otherwise, return false.
    """
    def calculate_new_attribute(self):
        temp_list = list(set(self.attribute_list) - set(self.found_attribute))
        temp_list.remove(self.concept_string)

        if len(temp_list) == 0:
            return False

        for attr in temp_list:
            ini_gain = self.parent_entropy
            cat_list = {}

            for item in self.current_list:
                if item.get_value(attr) in cat_list.keys():
                    cat_list[item.get_value(attr)].append(item)
                else:
                    cat_list[item.get_value(attr)] = [item]

            for sublist in cat_list.values():
                ini_gain -= (len(sublist)/len(self.current_list) * helper.get_set_entropy(sublist, self.concept_string))

            if helper.cal_chi_square(cat_list.values(), self.concept_string, self.compare_value) and ini_gain > self.cal_gain:
                self.cal_gain = ini_gain
                self.pre_attribute = attr
                self.cat_list_final = cat_list

        return True

    """
    This method is used to prepare children nodes for calculation.
    """
    def preChildren(self):
        for key in self.cat_list_final.keys():
            new_attribute_list = list(self.found_attribute)
            new_attribute_list.append(self.pre_attribute)
            self.child_list[key] = Node(self.attribute_list, new_attribute_list, key, self.cat_list_final[key], self.concept_string, self.compare_value)

    """
    This method is called to calculate all children nodes.
    """
    def runChildren(self):
        for child in self.child_list.values():
            child.run_build_tree()

    """
    This method is called to calculate this node.
    """
    def run(self):
        #check if the sample is pure, if it is pure, just end it
        result = helper.calculate_stat(self.current_list, self.concept_string)

        self.positive = result["positive"]
        self.negative = result["negative"]

        if helper.isPure(self.current_list, self.concept_string):
            return

        if self.calculate_new_attribute() == False:
            return

        self.preChildren()

        self.runChildren()
