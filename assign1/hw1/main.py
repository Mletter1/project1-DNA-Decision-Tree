#!/usr/bin/python

import node
import reader
import validation
import sys

"""
This file is the main file for this project, if you run_build_tree this file, you can get the decision tree printed.
"""
#read the file first
reading = reader.readFile(sys.argv[1], 58)
content = reading.read_file_content()

#calculate the data
root = node.Node(reading.get_attributes(), [], None, content, "isPromotor", sys.argv[3])
root.run()

#validate the result
x = validation.Validate(sys.argv[2], root, "isPromotor")
x.classification()

#print accuracy
print "The accuracy you got is {0}.".format(1- x.cal_error())