DC3 v0.1  	02/06/2015
@Auther Matthew letter
mletter1@unme.du

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Description:
    This script takes training data and builds out two decisions trees, one based
    on mis-clasification and the other on info gain.dc3 algorithm was used to produce
    the decision tree.The goal of this project was to implement the Decision Tree algorithm.
    This algorithm was used to classify validation DNA sample data, which were provided
    a machine learning repository. At a high level, the decision tree is built our
    (trained) using the provided training data and then validated using the validation data.
    Since we know the what the class was for each validation DNA sample an error rate
    can be calculated.

    All the training samples have to be read as the first step of building this decision tree.
    A sample data structure was created for this purpose,know as dna.py. A DNA sample object
    was built for each input DNA sample. the dna.py data structure was as a dictionary
    with book keeping. That is, it kept a dictionary of each position of the DNA strand it
    represented as well as having update and delete feature associated with the data structure.
    Each DNA strand, input from the data file, had 57 base positions. In the DNA data
    structure’s dictionary a base a given a key in the structure of Posistion- plus
    the position number. Doing this looking up a value at a position became a trivial
    task. When reading the data it was noted that the last position contained the DNA’s
    classification. This special case value was labeled as Promoter in the dictionary.

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Instruction for operation:

    file include in build:
      /data
      decision_tree.py
      decision_tree_MissClassification
      dna.py
      fileparser.py
      main.py
      output_tree.py
      README.txt
      the main entry point for this application is main.py.
      the program was write for python 2.x.

  execution eamples methods:

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  1:

  python main.py <path to training data> <path to validation data> <confidence>

  ex:
  python main.py data/training.txt data/validation.txt 0.99

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  2:optional

  python main.py -v <path to training data> <path to validation data> <confidence>

  python main.py -v data/training.txt data/validation.txt 0.99

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Bugs:
     unknown potential bug as there was no variation in classification with varied confidence.
     more validation test would be required to confirm or ignore this
