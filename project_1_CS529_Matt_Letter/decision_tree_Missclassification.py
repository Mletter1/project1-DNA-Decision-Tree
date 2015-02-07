#!/usr/bin/python
import math
import fileparser
import scipy.stats

__author__ = 'matthewletter'

"""
this class is used to recursively build the decision tree
it also acts as a level for each treee.
"""


class DecisionTreeMissclassification:
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
                 confidence_interval):
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
        self.max_info_gain = 30.0
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

        #count positive and negative in node
        self.positive = result["positive"]
        self.negative = result["negative"]

        # return if there is only one class
        if is_single_class(self.list_of_dna_strands_in_node, self.classification_key):
            return

        if not self.determine_splitting_node():
            return

        self.prep_for_split()

        self.recurse_and_run_new_nodes()

    """
    find attribute to spilit on
    return true after finding splitting attribute otherwise, return false.
    """

    def determine_splitting_node(self):
        # get bases list
        bases_left = list(set(self.dictionary_attribute_keys) - set(self.found_attribute))
        bases_left.remove(self.classification_key)

        # we are at the bottom of the tree if there is no more dna
        if len(bases_left) == 0:
            return False

        # find info gain for each base
        for position_of_base in bases_left:

            # set base info gain to that of the parent node
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
            if chi_squared_test(bases_seen_at_this_position.values(), self.classification_key,
                              self.confidence_interval) and error < self.max_info_gain:
                self.max_info_gain = error
                self.pre_attribute = position_of_base
                self.final_list_of_sorted_dna = bases_seen_at_this_position
        #print self.max_info_gain
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
            self.child_list[splitting_base] = DecisionTreeMissclassification(self.dictionary_attribute_keys, new_attribute_list,
                                                           splitting_base,
                                                           self.final_list_of_sorted_dna[splitting_base],
                                                           self.classification_key, self.confidence_interval)

    """
    cleanup
    """

    def __del__(self):
        # print ("deconstructing buffer")
        pass
class ValidateMissclassification:
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

    def one_class(self):
        #get class and see if its different from previous
        for current_class in self.tree.values():
            #return false if they dont match
            if is_single_class(current_class, self.classification_string_for_dictionary) is False:
                return False

        return True

    """
    get node for run.
    """

    def get_class_dna(self):
        max_value = -1
        max_key = None
        #get current key from tree keys
        for current_key in self.tree.keys():
            current_entropy = get_set_entropy(self.tree[current_key], self.classification_string_for_dictionary)
            #current value is high so swap
            if current_entropy > max_value:
                max_value = current_entropy
                max_key = current_key
        return max_key

    """
    classify group.
    key is the node used to classify the group
    """

    def classify_dna_group(self, key):
        node_dna_list = self.tree.pop(key)

        # build 2 dictionarys for temp values
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
                dictionary_2[dna.get_value_at_attribute(key.pre_attribute)] = DecisionTreeMissclassification(None, None, None, None,
                                                                                           None, 0)

        #update items
        for item_key in dictionary_1.keys():
            if len(dictionary_1[item_key]) > 0:
                self.tree[dictionary_2[item_key]] = dictionary_1[item_key]

    """
    classify the validation samples
    """

    def run(self):
        if self.one_class():
            return

        key = self.get_class_dna()
        node_num = len(key.child_list)
        if node_num == 0:
            return

        self.classify_dna_group(key)

        self.run()

    """
    return error for node.
    """

    def cal_node_error(self, cal_list):
        result = get_positive_and_negative_class_numbers_as_dictionary(cal_list,
                                                                       self.classification_string_for_dictionary)

        return 1 - (1.0 * max(result.values()) / len(cal_list))

    """
    return the error rate for validation dna.
    """

    def calculate_full_error_of_run(self):

        # initialize to float
        accumulated_error = float()

        #accumulate error
        for dna_list_for_node in self.tree.values():
            accumulated_error += (
                self.cal_node_error(dna_list_for_node) * len(dna_list_for_node) / self.number_of_samples)

        return (1 - accumulated_error) * 100

# ###########################################################################################

# ###########################################################################################
"""
return true if chi-square value is less than expected. Otherwise, return false.
"""


def chi_squared_test(child_nodes, classification_key, confidence_value):
    positive_dna_num = []
    negative_dna_num = []
    list_of_pos_s = []
    list_of_neg_s = []

    # get each child node and grab number of positive and negative classes
    for child_node in child_nodes:
        result = get_positive_and_negative_class_numbers_as_dictionary(child_node, classification_key)
        # build up all the positives
        positive_dna_num.append(result["positive"])
        # build up all the negatives
        negative_dna_num.append(result["negative"])

    for i in range(len(positive_dna_num)):
        list_of_pos_s.append(get_expected(positive_dna_num[i], negative_dna_num[i], sum(positive_dna_num), sum(negative_dna_num), True))
        list_of_neg_s.append(get_expected(positive_dna_num[i], negative_dna_num[i], sum(positive_dna_num), sum(negative_dna_num), False))

    # get chi-square value from table.
    chi_sqr_value = 0.0
    for i in range(len(positive_dna_num)):
        chi_sqr_value += (get_square(positive_dna_num[i], list_of_pos_s[i]) + get_square(negative_dna_num[i], list_of_neg_s[i]))

    # chi_result = scipy.stats.chi.pdf(chi_sqr_value, len(positive_dna_num) - 1)

    # print chi_sqr_value
    # print scipy.stats.chi2.ppf(confidence_value, 1)
    # print confidence_value
    # print chi_sqr_value >= scipy.stats.chi2.ppf(confidence_value, 1)
    # print
    if math.isnan(chi_sqr_value):
        return False
    return chi_sqr_value >= scipy.stats.chi2.ppf(confidence_value, 1)

"""
get max of positve negative
"""
def get_max_error(ps, ns):
    if sum(ps) > sum(ns):
        return 1.0 * (sum(ps) / (sum(ps) + sum(ns)))
    return 1.0 * (sum(ns) / (sum(ns) + sum(ps)))


"""
return a floating percentage
"""


def get_percent(numerator, denomator):
    return_value = 1.0 * numerator / denomator
    return return_value


"""
return the product.
"""


def get_product(perc):
    return_value = 1.0 * perc * math.log(perc, 2)
    return return_value


"""
return the entropy for the number list.
"""


def get_entropy(entropy_list):
    num_of_items = sum(entropy_list)
    return_sum_entropy = 0.0

    for i in entropy_list:
        return_sum_entropy += get_product(get_percent(i, num_of_items))

    return 0.0 - return_sum_entropy


"""
return the entropy of set.
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
return a dictionary containing + - #numbers.
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
return the expected value
"""


def get_expected(pistive_number, negative_number, total_positive, total_negative, bol_is_this_dna_a_promoter):
    total = total_negative

    if bol_is_this_dna_a_promoter:
        total = total_positive

    return 1.0 * total * (pistive_number + negative_number) / (total_positive + total_negative)


"""
return square value
"""


def get_square(observed_value, expected_value):
    if expected_value == 0:
        return 0.0

    return 0.0 + ((observed_value - expected_value) ** 2) / expected_value

"""
used for testing
"""
if __name__ == "__main__":
    obj = DecisionTreeMissclassification()
    del obj