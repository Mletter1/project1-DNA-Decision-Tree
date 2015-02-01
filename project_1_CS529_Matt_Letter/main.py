#!/usr/bin/env python
__author__ = 'Matthew Letter'
import sys
import os
import traceback
import optparse
import time
import fileparser
import decision_tree
import printer

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
run the program with training and validation text files and %confidence
"""
def run():
    global options, args
    print "\n" + "***********************************"
    print 'Runnning main script\n'
    #build parser with training data
    parser = fileparser.ParserClass("data/training.txt", 58)

    #parse and objectafy training data
    data = parser.parse_file()

    #debug data

    #run training
    root = decision_tree.DecisionTree(parser.get_attribute_keys(), [], None, data, "isPromotor", sys.argv[3])
    root.run()
    print root.child_list
    print root.positive
    print root.negative


    #print the data
    printing = printer.ShowResult(root)
    printing.run()


    #validate the result
    x = decision_tree.Validate("data/validation.txt", root, "isPromotor")
    x.classification()

    #print accuracy
    print "The accuracy you got is {0}.".format(1 - x.cal_error())

    del parser
    print '\nrun over'
    print "***********************************\n"


"""
determine running params
"""
if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=doc,
                                       version='%prog 0.1')

        parser.add_option('-v', '--verbose', action='store_true', default=False, help='verbose output')
        #get the options and args
        (options, args) = parser.parse_args()

        #determine what to do with the options supplied by the user
        if len(args) > 1 and options.verbose:
            print "opps", options
            print "args", args
            print "start time: " + time.asctime()
            run()
            print "finish time: " + time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - start_time) / 60.0
        elif len(args) < 1:
            parser.error('missing argument <training> <validation> <%val>')
        else:
            run()
        #smoth exit if no exceptions are thrown
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