#!/usr/bin/python

import helper
import sample
import copy

"""
This class is node class which contains the node in decision tree.
"""
class Node:
	"""
	Constructor
	Keyword arguments:
	attribute_list -- is the attributes list for the input data.
	found_attribute --  is the attributes list used so far for classification.
	parent_property -- is the catalog from the parent.
	current_list 
	concept_string -- is the attribute name used for concept defination.
	"""
	def __init__(self, attribute_list, found_attribute, parent_property, current_list, concept_string):
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
	
	"""
	Calculate the positive and negative sample numbers.
	"""
	def calculate_stat(self):
		for item in self.current_list:
			if item.getValue(self.concept_string) is "+":
				self.positive += 1
			else:
				self.negative += 1

	"""
	This method is used to calculate which attribute to choose.
	"""
	def calculate_new_attribute(self):
		temp_list = list(set(self.attribute_list) - set(self.found_attribute))
		temp_list.remove(self.concept_string)

		if len(temp_list) == 0:
			return False;

		for attr in temp_list:
			ini_gain = self.parent_entropy
			cat_list = {}

			for item in self.current_list:
				if item.getValue(attr) in cat_list.keys():
					cat_list[item.getValue(attr)].append(item)
				else:
					cat_list[item.getValue(attr)] = [item]
			
			for sublist in cat_list.values():
				ini_gain -= (len(sublist)/len(self.current_list) * helper.get_set_entropy(sublist, self.concept_string))
			
			if ini_gain > self.cal_gain:
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
			self.child_list[key] = Node(self.attribute_list, new_attribute_list, key, self.cat_list_final[key], self.concept_string)

	"""
	This method is called to calculate all children nodes.
	"""
	def runChildren(self):
		for child in self.child_list.values():
			child.run()

	"""
	This method is used to check if the current samples are pure
	"""
	def isPure(self):
		temp_property = self.current_list[0].getValue(self.concept_string)
		
		for item in self.current_list:
			if temp_property != item.getValue(self.concept_string):
				return False
		
		return True

	"""
	This method is called to calculate this node.
	"""
	def run(self):
		#check if the sample is pure, if it is pure, just end it
		self.calculate_stat()

		if self.isPure():
			return
		
		if self.calculate_new_attribute() == False:
			return
		
		self.preChildren()

		self.runChildren()

