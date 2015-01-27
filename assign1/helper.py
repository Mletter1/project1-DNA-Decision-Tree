#!/usr/bin/python

import math
import sample

"""
This file provides some basic methods to be used.
"""

"""
This method is used to calculate percentage with numerator and denomator
"""
def getPercent(numerator, denomator):
	return 1.0 * numerator/denomator

"""
This method is used to get product using percentage provided.
"""
def getProduct(percentage):
	return 1.0 * percentage * math.log(percentage, 2)

"""
This method is used to get entroy for specific numeric list
"""
def getEntropy(listtoCal):
	total = sum(listtoCal)
	totalResult = 0.0

	for i in listtoCal:
		totalResult += getProduct(getPercent(i, total))
	
	return 0.0 - totalResult

"""
This method is called to get subset entropy. If the attribute is null, just calculate whole entropy for whole set
"""
def get_set_entropy(listtoCal, attribute):
	if (attribute is None) or (listtoCal is None):
		return -1

	num_list = {}
	
	for item in listtoCal:
		if item.getValue(attribute) in num_list.keys():
			num_list[item.getValue(attribute)] += 1
		else:
			num_list[item.getValue(attribute)] = 1
	
	return getEntropy(num_list.values())

