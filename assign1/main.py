#/usr/bin/python

import node
import reader
import sys
import printer

"""
This file is the main file for this project, if you run_build_tree this file, you can get the decision tree printed.
"""
#read the file first
reading = reader.readFile(sys.argv[1])
content = reading.read_file_content()

#calculate the data
root = node.Node(reading.get_attributes(), [], None, content, "isPromotor")
root.run()

print root.child_list
print root.positive
print root.negative
#print the data
printing = printer.ShowResult(root)
printing.run()
