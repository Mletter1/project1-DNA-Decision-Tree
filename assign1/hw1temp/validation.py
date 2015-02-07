#!/usr/bin/python

import reader
import helper
import node

"""
This file is used to validate the ID algorithm
"""

class Validate:
	"""
	Constructor.
	
	key arguments:
	file_name -- is the name of file for validation.
	root_node -- is the root_node node for training algorithm.
	classification_key -- is the name of attribute for concept defination.
	"""
	def __init__(self, file_name, root, concept_string):
		self.reader = reader.readFile(file_name)
		self.reader.read_file_content()
		self.root = root
		self.result_map = {}
		self.result_map[root] = self.reader.content
		self.sample_num = len(self.reader.content)
		self.concept_string = concept_string
	
	"""
	This method is called to check if all list is pure.
	
	return true if the list only contains promoters or non-promoters. Otherwise, return false.
	"""	
	def check_pure(self):
		for item in self.result_map.values():
			if helper.isPure(item, self.concept_string) is False:
				return False
		
		return True
		
	"""
	This method is called to check which group should be used for run.
	
	return the node for run.
	"""
	def cal_classified_group(self):
		temp_value = -1
		temp_key = None
		
		for item in self.result_map.keys():
			temp = helper.get_set_entropy(self.result_map[item], self.concept_string)

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
			if(item.get_value(key.pre_attribute) in temp_map1.keys()):
				temp_map1[item.get_value(key.pre_attribute)].append(item)
			else:
				temp_map1[item.get_value(key.pre_attribute)] = [item]
				temp_map2[item.get_value(key.pre_attribute)] = node.Node(None, None, None, None, None, None, None)
		
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
		
		if(len(key_to_cal.child_list) == 0):
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
		result = helper.calculate_stat(cal_list, self.concept_string)
		
		return (1 - (1.0 * max(result.values())/len(cal_list)))
		
	"""
	This method is called to calculate error information.
	
	return the error rate for validation samples.
	"""
	def cal_error(self):
		result = 0
		
		for item in self.result_map.values():
			result += (self.cal_node_error(item) * len(item)/self.sample_num)
			
		return result			