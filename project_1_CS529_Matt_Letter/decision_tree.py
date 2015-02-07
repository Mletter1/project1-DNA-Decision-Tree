#!/usr/bin/python
import math
import fileparser
import scipy.stats

__author__ = 'matthewletter'

"""
this class is used to recursively build the decision tree
it also acts as a level for each treee.
"""


class DecisionTree:
    """
    Keyword arguments:
    dictionary_attribute_keys input data.
    found_attribute attributes already traversed.
    parent_property parent entropy.
    list_of_dna_strands_in_node list of dna in this node.
    classification_key key value used to store section of promotor in dictionary.
    confidence_interval 0->0.99999.
    """

    def __init__(self, attribute_list, found_attribute, parent_property, current_list, classification_key,
                 confidence_interval, info_gain=True):
        # our dictionary need some keys
        self.dictionary_attribute_keys = attribute_list

        # this will be set to empty for the root_node node
        self.found_attribute = found_attribute

        # list of data dna elements
        self.list_of_dna_strands_in_node = current_list

        # dictionary of the child elements for a node
        self.child_list = {}

        # info about the parent node
        self.parent_property = parent_property
        self.classification_key = classification_key

        # find entropy for this node
        self.parent_entropy = get_set_entropy(current_list, classification_key)
        self.pre_attribute = ""
        self.max_info_gain = 10.0
        self.final_list_of_sorted_dna = {}

        # number of positive and negative values in this node
        self.positive = 0
        self.negative = 0

        # ci
        self.confidence_interval = 0.0 + confidence_interval

    """
    recursively build out the decision tree until empty set, pure set, or
    """

    def run_build_tree(self):

        # check if the sample is pure, if it is pure, just end it
        result = get_positive_and_negative_class_numbers_as_dictionary(self.list_of_dna_strands_in_node,
                                                                       self.classification_key)

        #
        self.positive = result["positive"]
        self.negative = result["negative"]

        # return if there is only one class
        if is_single_class(self.list_of_dna_strands_in_node, self.classification_key):
            return

        if not self.calculate_new_attribute():
            return

        self.prep_for_split()

        self.recurse_and_run_new_nodes()

    """
    find attribute to spilit on
    return true after finding splitting attribute otherwise, return false.
    """

    def calculate_new_attribute(self):
        # get bases list
        bases_left = list(set(self.dictionary_attribute_keys) - set(self.found_attribute))
        bases_left.remove(self.classification_key)

        # we are at the bottom of the tree if there is no more dna
        if len(bases_left) == 0:
            return False

        # find info gain for each base
        for position_of_base in bases_left:

            # set base info gain to that of the parent node
            ini_gain = self.parent_entropy
            child_average_gain = 0.0
            error = 0

            # list of info gain of
            bases_seen_at_this_position = {}

            # grab each dna strand
            for dna_strand in self.list_of_dna_strands_in_node:
                if dna_strand.get_value_at_attribute(position_of_base) in bases_seen_at_this_position.keys():
                    #grab list at key and append dna strand to it
                    bases_seen_at_this_position[dna_strand.get_value_at_attribute(position_of_base)].append(dna_strand)
                else:
                    #create a list at key, of dna strands
                    bases_seen_at_this_position[dna_strand.get_value_at_attribute(position_of_base)] = [dna_strand]

            #calc info gain for this position
            for base_dna_list in bases_seen_at_this_position.values():
                child_average_gain += (get_percent(len(base_dna_list), len(self.list_of_dna_strands_in_node))
                                       * get_set_entropy(base_dna_list, self.classification_key))

            #calc info gained by this split
            ini_gain -= child_average_gain


            #uncomment for missclass error
            ps = list()
            ns = list()

            #get each child node and grab number of positive and negative classes
            for child_node in bases_seen_at_this_position.values():
                result = get_positive_and_negative_class_numbers_as_dictionary(child_node, self.classification_key)
                #build up all the positives
                ps.append(result["positive"])
                #build up all the negatives
                ns.append(result["negative"])
                error += 1 - get_max_error(ps, ns)
                #print error


            #
            if cal_chi_square(bases_seen_at_this_position.values(), self.classification_key,
                              self.confidence_interval) and error < self.max_info_gain:
                self.max_info_gain = error
                self.pre_attribute = position_of_base
                self.final_list_of_sorted_dna = bases_seen_at_this_position
        print self.max_info_gain
        return True

    """
    run child nodes
    """

    def recurse_and_run_new_nodes(self):
        for branch_node in self.child_list.values():
            branch_node.run_build_tree()

    """
    build child set of nodes
    """

    def prep_for_split(self):

        # for each base
        for splitting_base in self.final_list_of_sorted_dna.keys():
            #populate our new list
            new_attribute_list = list(self.found_attribute)
            new_attribute_list.append(self.pre_attribute)

            #build new node
            self.child_list[splitting_base] = DecisionTree(self.dictionary_attribute_keys, new_attribute_list,
                                                           splitting_base,
                                                           self.final_list_of_sorted_dna[splitting_base],
                                                           self.classification_key, self.confidence_interval)

    """
    cleanup
    """

    def __del__(self):
        # print ("deconstructing buffer")
        pass

# ###########################################################################################

# ###########################################################################################

"""
takes validations data and built dc tree and outputs the accuracy
"""


class Validate:
    """
    file_name validation file
    root_node root_node node of the tree from dc
    classification_key string key for class dictionary.
    """

    def __init__(self, file_name, root_node, classification_string_for_dictionary):
        self.io_parser = fileparser.ParserClass(file_name)
        self.io_parser.parse_file()
        self.root_node = root_node
        self.tree = {root_node: self.io_parser.data_elements}
        self.number_of_samples = len(self.io_parser.data_elements)
        self.classification_string_for_dictionary = classification_string_for_dictionary

    """
    return true if all + or -. Otherwise, return false.
    """

    def check_pure(self):
        for item in self.tree.values():
            if is_single_class(item, self.classification_string_for_dictionary) is False:
                return False

        return True

    """
    get node for classification.
    """

    def get_class_dna(self):
        temp_value = -1
        temp_key = None

        for item in self.tree.keys():
            temp = get_set_entropy(self.tree[item], self.classification_string_for_dictionary)

            if temp > temp_value:
                temp_value = temp
                temp_key = item

        return temp_key

    """
    classify group.
    key is the node used to classify the group
    """

    def classify_group(self, key):
        node_dna_list = self.tree.pop(key)

        #build 2 dictionarys for temp values
        dictionary_1 = {}
        dictionary_2 = {}

        #iterate through the child list
        for child_node in key.child_list.values():
            dictionary_1[child_node.parent_property] = []
            dictionary_2[child_node.parent_property] = child_node

        #build out dictionary with dna list
        for dna in node_dna_list:
            if dna.get_value_at_attribute(key.pre_attribute) in dictionary_1.keys():
                dictionary_1[dna.get_value_at_attribute(key.pre_attribute)].append(dna)
            else:
                dictionary_1[dna.get_value_at_attribute(key.pre_attribute)] = [dna]
                dictionary_2[dna.get_value_at_attribute(key.pre_attribute)] = DecisionTree(None, None, None, None,
                                                                                           None, 0)

        #update items
        for item_key in dictionary_1.keys():
            if len(dictionary_1[item_key]) > 0:
                self.tree[dictionary_2[item_key]] = dictionary_1[item_key]

    """
    classify the validation samples
    """

    def classification(self):
        if self.check_pure():
            return

        key_to_cal = self.get_class_dna()

        if len(key_to_cal.child_list) == 0:
            return

        self.classify_group(key_to_cal)

        self.classification()

    """
    calculate error for one node.
    cal_list node list to calculate error rate.
    return error for node.
    """

    def cal_node_error(self, cal_list):
        result = get_positive_and_negative_class_numbers_as_dictionary(cal_list, self.classification_string_for_dictionary)

        return 1 - (1.0 * max(result.values()) / len(cal_list))

    """
    calculate error information.

    return the error rate for validation samples.
    """

    def calculate_full_error_of_run(self):

        #initialize to float
        accumulated_error = float()

        #accumulate error
        for dna_list_for_node in self.tree.values():
            accumulated_error += (self.cal_node_error(dna_list_for_node) * len(dna_list_for_node) / self.number_of_samples)

        return (1 - accumulated_error) * 100


# ###########################################################################################

# ###########################################################################################
def get_max_error(ps, ns):
    if sum(ps) > sum(ns):
        return 1.0 * (sum(ps) / (sum(ps) + sum(ns)))
    return 1.0 * (sum(ns) / (sum(ns) + sum(ps)))


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


def get_set_entropy(list_of_dna_strands, attribute="Promoter"):
    if (attribute is None) or (list_of_dna_strands is None):
        return -1

    dictionary_ispromotor = {}

    for dna_strand in list_of_dna_strands:
        if dna_strand.get_value_at_attribute(attribute) in dictionary_ispromotor.keys():
            dictionary_ispromotor[dna_strand.get_value_at_attribute(attribute)] += 1
        else:
            dictionary_ispromotor[dna_strand.get_value_at_attribute(attribute)] = 1

    return get_entropy(dictionary_ispromotor.values())


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
list_of_dna_strands_in_node -- is the list to be checked.
classification_key -- is the attribute name of the classifier.

return True iff the list only contains 1 class
"""


def is_single_class(current_list_of_dna_strands, classification_key):
    # get the class of the first DNA strand in the list
    classification_of_first_dna_strand = current_list_of_dna_strands[0].get_value_at_attribute(classification_key)

    # go through each dna strand looking for a miss-match
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
    instances_here = ntotal

    if isPromotor:
        instances_here = ptotal

    return 1.0 * instances_here * (p + n) / (ptotal + ntotal)


"""
This method is called to calculate (observer-expected)^2/expected value.

Key arguments:
observed_value
expected_value

return the value calculated.
"""


def cal_square(observed_value, expected_value):
    if expected_value == 0:
        return 0.0

    return 0.0 + ((observed_value - expected_value) ** 2) / expected_value


"""
This method is called to calculate chi-square value.

Key arguments:
child_list_to_test -- is the child list for calculation.
classification_key -- is the name of attribute used for concept definition.
confidence_interval -- is the p-value for testing.

return true if chi-square value is less than expected. Otherwise, return false.
"""


def cal_chi_square(child_nodes, classification_key, confidence_value):
    ps = []  # number of positive dna
    ns = []  # number of negative dna
    pps = []  # confidence_value number of positive dna
    nps = []  # confidence_value number of negative dna

    # get each child node and grab number of positive and negative classes
    for child_node in child_nodes:
        result = get_positive_and_negative_class_numbers_as_dictionary(child_node, classification_key)
        # build up all the positives
        ps.append(result["positive"])
        # build up all the negatives
        ns.append(result["negative"])

    for i in range(len(ps)):
        pps.append(cal_expected_value(ps[i], ns[i], sum(ps), sum(ns), True))
        nps.append(cal_expected_value(ps[i], ns[i], sum(ps), sum(ns), False))

    # get chi-square value from table.
    chi_sqr_value = 0.0
    for i in range(len(ps)):
        chi_sqr_value += (cal_square(ps[i], pps[i]) + cal_square(ns[i], nps[i]))

    # chi_result = scipy.stats.chi.pdf(chi_sqr_value, len(ps) - 1)

    # print chi_sqr_value
    # print scipy.stats.chi2.ppf(confidence_value, 1)
    # print confidence_value
    # print chi_sqr_value >= scipy.stats.chi2.ppf(confidence_value, 1)
    # print
    if math.isnan(chi_sqr_value):
        return False
    return chi_sqr_value >= scipy.stats.chi2.ppf(confidence_value, 1)


"""
used for testing
"""
if __name__ == "__main__":
    obj = DecisionTree()
    del obj