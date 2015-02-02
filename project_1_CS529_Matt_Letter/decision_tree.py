#!/usr/bin/python
import math
import fileparser
import scipy.stats as sst

__author__ = 'matthewletter'

"""
this class is used to recursively build the decision tree
it also acts as a level for each treee.
"""


class DecisionTree:
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

    def __init__(self, attribute_list, found_attribute, parent_property, current_list, classification_key,
                 confidence_interval):
        # our dictionary need some keys
        self.dictionary_attribute_keys = attribute_list

        # this will be set to empty for the root node
        self.found_attribute = found_attribute

        #list of elements
        self.current_dna_list = current_list

        #dictionary of the child elements for a node
        self.child_list = {}

        #info about the parent node
        self.parent_property = parent_property
        self.classification_key = classification_key

        #find entropy for this node
        self.parent_entropy = get_set_entropy(current_list, classification_key)
        self.pre_attribute = ""
        self.cal_gain = 0
        self.cat_list_final = {}

        #number of positive and negative values in this node
        self.positive = 0
        self.negative = 0

        #
        self.confidence_interval = confidence_interval

    """
    This method is used to calculate which attribute to choose.

    return true if there is an attribute for classification, otherwise, return false.
    """

    def calculate_new_attribute(self):
        #get dna list
        dna_list = list(set(self.dictionary_attribute_keys) - set(self.found_attribute))
        dna_list.remove(self.classification_key)

        #we are at the bottom of the tree if there is no more dna
        if len(dna_list) == 0:
            return False

        for dna_strand in dna_list:
            ini_gain = self.parent_entropy
            cat_list = {}

            for item in self.current_dna_list:
                if item.get_value_at_attribute(dna_strand) in cat_list.keys():
                    cat_list[item.get_value_at_attribute(dna_strand)].append(item)
                else:
                    cat_list[item.get_value_at_attribute(dna_strand)] = [item]

            for sublist in cat_list.values():
                ini_gain -= (
                    len(sublist) / len(self.current_dna_list) * get_set_entropy(sublist, self.classification_key))

            if cal_chi_square(cat_list.values(), self.classification_key, self.confidence_interval) \
                    and ini_gain > self.cal_gain:
                self.cal_gain = ini_gain
                self.pre_attribute = dna_strand
                self.cat_list_final = cat_list

        return True

    """
    This method is used to prepare children nodes for calculation.
    """

    def preChildren(self):
        for key in self.cat_list_final.keys():
            new_attribute_list = list(self.found_attribute)
            new_attribute_list.append(self.pre_attribute)
            self.child_list[key] = DecisionTree(self.dictionary_attribute_keys, new_attribute_list, key,
                                                self.cat_list_final[key],
                                                self.classification_key, self.confidence_interval)

    """
    This method is called to calculate all children nodes.
    """

    def runChildren(self):
        for child in self.child_list.values():
            child.run_build_tree()

    """
    This method is called to calculate this node.
    """

    def run_build_tree(self):

        # check if the sample is pure, if it is pure, just end it
        result = get_positive_and_negative_class_numbers_as_dictionary(self.current_dna_list, self.classification_key)

        #
        self.positive = result["positive"]
        self.negative = result["negative"]

        # return if there is only one class
        if is_single_class(self.current_dna_list, self.classification_key):
            return

        if not self.calculate_new_attribute():
            return

        self.preChildren()

        self.runChildren()

    """
    cleanup
    """

    def __del__(self):
        # print ("deconstructing buffer")
        pass

# ###########################################################################################

# ###########################################################################################

"""
This file is used to validate the ID algorithm
"""


class Validate:
    """
    Constructor.

    key arguments:
    file_name -- is the name of file for validation.
    root -- is the root node for training algorithm.
    classification_key -- is the name of attribute for concept defination.
    """

    def __init__(self, file_name, root, concept_string):
        self.reader = fileparser.ParserClass(file_name)
        self.reader.parse_file()
        self.root = root
        self.result_map = {root: self.reader.data_elements}
        self.sample_num = len(self.reader.data_elements)
        self.concept_string = concept_string

    """
    This method is called to check if all list is pure.

    return true if the list only contains promoters or non-promoters. Otherwise, return false.
    """

    def check_pure(self):
        for item in self.result_map.values():
            if is_single_class(item, self.concept_string) is False:
                return False

        return True

    """
    This method is called to check which group should be used for classification.

    return the node for classification.
    """

    def cal_classified_group(self):
        temp_value = -1
        temp_key = None

        for item in self.result_map.keys():
            temp = get_set_entropy(self.result_map[item], self.concept_string)

            if temp > temp_value:
                temp_value = temp
                temp_key = item

        return temp_key

    """
    This method is called to classify the specific group.

    Key arguments:
    key -- is the node used to classify specific group.
    """

    def classify_group(self, key):
        value = self.result_map.pop(key)

        temp_map1 = {}
        temp_map2 = {}

        for child in key.child_list.values():
            temp_map1[child.parent_property] = []
            temp_map2[child.parent_property] = child

        for item in value:
            if item.get_value_at_attribute(key.pre_attribute) in temp_map1.keys():
                temp_map1[item.get_value_at_attribute(key.pre_attribute)].append(item)
            else:
                temp_map1[item.get_value_at_attribute(key.pre_attribute)] = [item]
                temp_map2[item.get_value_at_attribute(key.pre_attribute)] = DecisionTree(None, None, None, None, None,
                                                                                         None)

        for item_key in temp_map1.keys():
            if len(temp_map1[item_key]) > 0:
                self.result_map[temp_map2[item_key]] = temp_map1[item_key]

    """
    This method is used to classify the validation samples
    """

    def classification(self):
        if self.check_pure():
            return

        key_to_cal = self.cal_classified_group()

        if len(key_to_cal.child_list) == 0:
            return

        self.classify_group(key_to_cal)

        self.classification()

    """
    This method is used to calculate the error for one node.

    Key arguments:
    cal_list -- is node list of the child node to calculate error rate.

    return the error for the node.
    """

    def cal_node_error(self, cal_list):
        result = get_positive_and_negative_class_numbers_as_dictionary(cal_list, self.concept_string)

        return 1 - (1.0 * max(result.values()) / len(cal_list))

    """
    This method is called to calculate error information.

    return the error rate for validation samples.
    """

    def cal_error(self):
        result = 0

        for item in self.result_map.values():
            result += (self.cal_node_error(item) * len(item) / self.sample_num)

        return result

############################################################################################

############################################################################################

"""
This method is used to calculate percentage with numerator and denomator.

Key arguments:
numerator -- is the numerator.
denomator -- is the denomator.

return a floating percentage number associated to the input.
"""


def get_percent(numerator, denomator):
    return 1.0 * numerator / denomator


"""
This method is used to get product for entropy calculation using percentage provided.

Key arguments:
percentage -- is the percentage used for product calculation.

return the product used for entropy calculation.
"""


def get_product(percentage):
    return 1.0 * percentage * math.log(percentage, 2)


"""
This method is used to get entropy for specific numeric list.

Key arguments:
list_to_cal -- is the number list for entropy calculation.

return the entropy for the number list.
"""


def get_entropy(list_to_cal):
    total = sum(list_to_cal)
    totalResult = 0.0

    for i in list_to_cal:
        totalResult += get_product(get_percent(i, total))

    return 0.0 - totalResult


"""
This method is called to get subset entropy. If the attribute is null, return -1

Key arguments:
list_to_cal -- is the list of samples to calculate entropy.
attribute -- is the attribute for the sample to calculate entropy.

return the entropy associated with the list passed and attribute.
"""


def get_set_entropy(list_to_cal, attribute):
    if (attribute is None) or (list_to_cal is None):
        return -1

    num_list = {}

    for item in list_to_cal:
        if item.get_value_at_attribute(attribute) in num_list.keys():
            num_list[item.get_value_at_attribute(attribute)] += 1
        else:
            num_list[item.get_value_at_attribute(attribute)] = 1

    return get_entropy(num_list.values())


"""
Calculate the positive and negative sample numbers.

cur_list -- is the list to check promoter and non-promoter numbers.
classification_key -- is the attribute name for concept definition.

return a dictionary containing promotor and non-promotor numbers.
"""


def get_positive_and_negative_class_numbers_as_dictionary(dna_list, classification_key):
    positive_negative_ratio_list = {"positive": 0, "negative": 0}

    for dna in dna_list:
        if dna.get_value_at_attribute(classification_key) is "+":
            positive_negative_ratio_list["positive"] += 1
        else:
            positive_negative_ratio_list["negative"] += 1

    return positive_negative_ratio_list


"""
current_dna_list -- is the list to be checked.
classification_key -- is the attribute name of the classifier.

return True iff the list only contains 1 class
"""


def is_single_class(current_list_of_dna_strands, classification_key):
    #get the class of the first DNA strand in the list
    classification_of_first_dna_strand = current_list_of_dna_strands[0].get_value_at_attribute(classification_key)

    #go through each dna strand looking for a miss-match
    for dna_strand in current_list_of_dna_strands:
        if classification_of_first_dna_strand != dna_strand.get_value_at_attribute(classification_key):
            return False
    return True


"""
This method is used to calculate expected value for specific observed value.

Key arguments:
p -- is the number of promoters for the group to calculate.
n -- is the number of non-promoters for the group to calculate.
ptotal -- is the total number of promoters in the list to be classified.
ntotal -- is the total number of non-promoters in the list to be classified.
isPromotor -- is true if expected promoter number is calculated. Otherwise, false if expected
non-promoter number is calculated.

return the expected value to calculate.
"""


def cal_expected_value(p, n, ptotal, ntotal, isPromotor):
    test_value = ntotal

    if isPromotor:
        test_value = ptotal

    return 1.0 * test_value * (p + n) / (ptotal + ntotal)


"""
This method is called to calculate (observer-expected)^2/expected value.

Key arguments:
observed_value
expected_value

return the value calculated.
"""


def cal_square(observed_value, expected_value):
    if expected_value == 0:
        return 0

    return (observed_value - expected_value) ** 2 / expected_value



"""
This method is called to calculate chi-square value.

Key arguments:
child_list_to_test -- is the child list for calculation.
classification_key -- is the name of attribute used for concept definition.
confidence_interval -- is the p-value for testing.

return true if chi-square value is less than expected. Otherwise, return false.
"""


def cal_chi_square(child_nodes, classification_key, expected):
    ps = []  # number of positive dna
    ns = []  # number of negative dna
    pps = []  # expected number of positive dna
    nps = []  # expected number of negative dna

    #get each child node and grab number of positive and negative classes
    for child_node in child_nodes:
        result = get_positive_and_negative_class_numbers_as_dictionary(child_node, classification_key)
        #build up all the positives
        ps.append(result["positive"])
        #build up all the negatives
        ns.append(result["negative"])

    for i in range(len(ps)):
        pps.append(cal_expected_value(ps[i], ns[i], sum(ps), sum(ns), True))
        nps.append(cal_expected_value(ps[i], ns[i], sum(ps), sum(ns), False))

    #get chi-square value.
    chi_sqr_value = 0
    for i in range(len(ps)):
        chi_sqr_value += (cal_square(ps[i], pps[i]) + cal_square(ns[i], nps[i]))

    chi_result = sst.chi.pdf(chi_sqr_value, len(ps) - 1)

    return chi_result < expected


"""
used for testing
"""
if __name__ == "__main__":
    obj = DecisionTree()
    del obj