	Decision Tree Calculation Version 1.0 	2/6/2014

Description:
  This software is used to calculate the decision tree for promotor DNA
sequence. It can read the data from training.txt file and use them to train
ID algorithm. After training, it use the algorithm to classify validation
samples and try to calculate the accuracy.

Contact Information:
  Author: 		Lin Sun
  E-mail:		sun@unm.edu
  Published date:	2/9/2014

Contents:
  main.py
  reader.py
  sample.py
  node.py
  validation.py
  helper.py
  README.txt
  training.txt
  validation.txt

Instruction:
  1. The main method for this application is main.py. If you want to run_build_tree this
application, just type command as follow:
	$python main.py <training_file> <validation_file> <confidence> <splitting_mode>
where training_file is the name of file to train the algorithm and validation_file 
is the name of file to validate the ID algorithm. confidence is the value used for 
chi-square testing. You can input your own value here, like 0.95, 0.99 or even 0.
For splitting_mode, you should input 1 if you want to use misclassification method
for decision tree building. Otherwise, input 2 if you want to use entropy calculation
for attribute decision.
  2. After you run_build_tree the application, it will print the accuracy for your validation
samples.
  3. Besides, there is a runnable file, called runfile. You can just run_build_tree as
  	$./runfile
then you will get the result for different mode and different confidence interval 
value. Then you can open result.txt to check the result value.

Bugs:
  1. For this application, there is no GUI display. So it is not obvious to check 
the tree relationship.
  2. For chi-square calculation, it is not clear whether it works as expected. It
is implemented here, but it did not affect the final result.
