#!/usr/bin/env python
__author__ = 'Matthew Letter'
import sys
import os
import traceback
import optparse
import time
import fileparser
import decision_tree
import output_tree
import decision_tree_Missclassification

doc = """
SYNOPSIS

    main [-h,--help] [-v,--verbose] [--version] <training.txt> <validate.txt> <%confidence>

DESCRIPTION

    This is the main entry point for the ID3 python script used to create a decision tree for
    DNA. this file

EXAMPLES
    print out help message:
        main -h
    Run the ID3 algorithm with verbose output
        main -v training.txt validation.txt 0.95

EXIT STATUS

    0 no issues
    1 unknown error
    2 improper params

AUTHOR

    Name Matthew Letter mletter1@unm.edu

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    v0.1
"""

"""
run_build_tree the program with training and validation text files and %confidence
"""


def run():
    print "\n" + "***********************************"
    print 'Runnning main script\n'
    # build parser with training data
    parser = fileparser.ParserClass("data/training.txt", 58)

    # parse and objectafy training data
    data = parser.parse_file()

    # debug data

    #run_build_tree training
    tree_information_gain = decision_tree.DecisionTree(parser.get_attribute_keys(), [], None, data, "Promoter",
                                                       float(args[2]))
    tree_information_gain.run_build_tree()

    #print tree_information_gain.child_list
    print "positive dna # ", tree_information_gain.positive
    print "negative dna # ", tree_information_gain.negative
    print "confidence ", args[2]

    #run_build_tree training
    tree_missclassification = decision_tree_Missclassification.DecisionTreeMissclassification(
        parser.get_attribute_keys(), [], None, data, "Promoter", float(args[2]))
    tree_missclassification.run_build_tree()

    print
    print "info gain tree"
    #print the data
    printing = output_tree.ShowResult(tree_information_gain)
    printing.run()
    print
    print "misclassification error tree"
    printing = output_tree.ShowResult(tree_missclassification)
    printing.run()
    print
    print

    #validate the result for misclassification
    x = decision_tree_Missclassification.ValidateMissclassification("data/validation.txt", tree_missclassification,
                                                                    "Promoter")
    x.run()
    print "The accuracy for misclassification error is {0}%.".format(x.calculate_full_error_of_run())


    #validate the result for info gain
    y = decision_tree.Validate("data/validation.txt", tree_information_gain, "Promoter")
    y.run()
    #print accuracy
    print "The accuracy for information gain is {0}%.".format(y.calculate_full_error_of_run())

    del parser
    print '\nrun_build_tree over'
    print "***********************************\n"

def run_quite():
    parser = fileparser.ParserClass("data/training.txt", 58)

    # parse and objectafy training data
    data = parser.parse_file()

    # debug data

    #run_build_tree training
    tree_information_gain = decision_tree.DecisionTree(parser.get_attribute_keys(), [], None, data, "Promoter",
                                                       float(args[2]))
    tree_information_gain.run_build_tree()

    #run_build_tree training
    tree_missclassification = decision_tree_Missclassification.DecisionTreeMissclassification(
        parser.get_attribute_keys(), [], None, data, "Promoter", float(args[2]))
    tree_missclassification.run_build_tree()

    #validate the result for misclassification
    x = decision_tree_Missclassification.ValidateMissclassification("data/validation.txt", tree_missclassification,
                                                                    "Promoter")
    x.run()
    print "The accuracy for misclassification error is {0}%.".format(x.calculate_full_error_of_run())


    #validate the result for info gain
    y = decision_tree.Validate("data/validation.txt", tree_information_gain, "Promoter")
    y.run()
    #print accuracy
    print "The accuracy for information gain is {0}%.".format(y.calculate_full_error_of_run())

    del parser



"""
determine running params
"""
if __name__ == '__main__':
    global options, args
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=doc,
                                       version='%prog 0.1')

        parser.add_option('-v', '--verbose', action='store_true', default=False, help='verbose output')
        # get the options and args
        (options, args) = parser.parse_args()

        # determine what to do with the options supplied by the user
        if len(args) > 1 and options.verbose:
            print "options ", options
            print "args", args
            print "start time: " + time.asctime()
            run()
            print "finish time: " + time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - start_time) / 60.0
        elif len(args) < 1:
            parser.error('missing argument <training> <validation> <%val>')
        else:
            run_quite()
        # smo0th exit if no exceptions are thrown
        sys.exit(0)

    except KeyboardInterrupt, e:  # Ctrl-C
        raise e
    except SystemExit, e:  # sys.exit()
        raise e
    except Exception, e:  # unknown exception
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)