#!/usr/bin/python

import math
import scipy.stats as sst

"""
This file provides some basic methods to be used.
"""

"""
This method is used to calculate percentage with numerator and denomator.

Key arguments:
numerator -- is the numerator.
denomator -- is the denomator.

return a floating percentage number associated to the input.
"""
def get_percent(numerator, denomator):
	return 1.0 * numerator/denomator

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
		if item.get_value(attribute) in num_list.keys():
			num_list[item.get_value(attribute)] += 1
		else:
			num_list[item.get_value(attribute)] = 1
	
	return get_entropy(num_list.values())

"""
Calculate the positive and negative sample numbers.

cur_list -- is the list to check promoter and non-promoter numbers.
classification_key -- is the attribute name for concept definition.

return a dictionary containing promotor and non-promotor numbers.
"""
def calculate_stat(cur_list, concept_string):
	result = {}
	result["positive"] = 0
	result["negative"] = 0
	
	for item in cur_list:
		if item.get_value(concept_string) is "+":
			result["positive"] += 1
		else:
			result["negative"] += 1
	
	return result

"""
This method is used to check if the current sample list is pure.

current_dna_list -- is the list to be checked.
classification_key -- is the attribute name for concept definition.

return True if the list only contains promoter or non-promoter. Otherwise, return False. 
"""
def isPure(current_list, concept_string):
	temp_property = current_list[0].get_value(concept_string)
	
	for item in current_list:
		if temp_property != item.get_value(concept_string):
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
	
	return 1.0 * test_value * (p + n)/(ptotal + ntotal)

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
		
	return (observed_value - expected_value)**2 / expected_value

"""
The method is used to help calculate chi_square value.

Key arguments:
ps -- is the list of observed promoter number.
ns -- is the list of observed non-promoter number.
pps -- is the list of expected promoter number.
nps -- is the list of expected non-promoter number.

return the chi-square value.
"""
def cal_chi_square_helper(ps, ns, pps, nps):
	total = 0
	
	for i in range(len(ps)):
		total += (cal_square(ps[i], pps[i]) + cal_square(ns[i], nps[i]))
	
	return total
"""
This method is called to calculate chi-square value.

Key arguments:
child_list_to_test -- is the child list for calculation.
classification_key -- is the name of attribute used for concept definition.
confidence_interval -- is the p-value for testing.

return true if chi-square value is less than expected. Otherwise, return false.
"""
def cal_chi_square(child_list_to_test, concept_string, compare_value):
	ps = [] 	#The observed promotors number
	ns = []		#The observed non-promotors number
	pps = [] 	#The expected promotors number
	nps = []	#The expected non-promotors number

	for child in child_list_to_test:
		result = calculate_stat(child, concept_string)
		ps.append(result["positive"])
		ns.append(result["negative"])
	
	for i in range(len(ps)):
		pps.append(cal_expected_value(ps[i], ns[i], sum(ps), sum(ns), True))
		nps.append(cal_expected_value(ps[i], ns[i], sum(ps), sum(ns), False))
	
	chi_result = sst.chi.pdf(cal_chi_square_helper(ps, ns, pps, nps), 3)
	
	return chi_result < compare_value

"""
This method is used to calculate the error for one node.
	
Key arguments:
cal_list -- is node list of the child node to calculate error rate.
classification_key -- is the name of the concept.
	
return the error for the node.
"""
def cal_node_error(cal_list, concept_string):
	result = calculate_stat(cal_list, concept_string)
	
	return (1 - (1.0 * max(result.values())/len(cal_list)))
		
"""
This method is called to calculate error information.

Key arguments:
classification_key -- is the name of the concept.
list_to_cal -- is the list of all child node list.
	
return the error rate for validation samples.
"""
def cal_error(concept_string, list_to_cal):
	result = 0
	sample_num = 0
	
	for item in list_to_cal:
		sample_num += len(item) 
		
	for item in list_to_cal:
		result += (cal_node_error(item, concept_string) * len(item)/sample_num)
			
	return result	