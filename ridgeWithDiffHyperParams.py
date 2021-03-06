#!/usr/bin/env python
from numpy.linalg import inv, solve, matrix_rank,norm
import numpy as np
from sklearn.linear_model import Ridge
import sys, os
from random import shuffle, randint

def ridge(xTrain, yTrain,alpha):
	testMatrix = np.zeros((xTrain.shape[0],xTrain.shape[1]+1))
	for i,x in enumerate(xTrain):
		testMatrix[i] = np.append(1,x)
	regression = Ridge(alpha=alpha, normalize=True)
	return regression.fit(testMatrix,yTrain).coef_

def predict(W, x):
	"""
	Predict the class y of a single set of attributes
	:param W:	DxK Least squares weight matrix
	:param x:	1xD matrix of attributes for testing
	:return:	List of 0's and 1's. Index with 1 is the class of x
	"""
	x = np.append(1, x)		# augment test vector

	# Solve W'*x
	values = list(np.dot(W,x))

	# Find maxima of values
	winners = [i for i, x in enumerate(values) if x == max(values)] # indexes of maxima
	# Flip a coin to decide winner
	# if only one winner, it will be chosen by default
	index = randint(0,len(winners)-1)
	winner = winners[index]

	y = [0 for x in values] 	# initalize list with all zeros
	y[winner] = 1 				# set winner
	return y

def fixLabels(y):
	"""
	Fixes labels so they fit our methods
	:param y:	List of numbers cooresponding to class of each
	:return:	Matrix of 0/1 lists.
				Index in list with 1 is class of the cooresponding data
				Example: [0 1 2] => [[1 0 0], [0 1 0], [0 0 1]]
	"""
	newY = []
	for i in range(len(y)):
		# Each list is the size of the largest class number
		size = max(y)
		temp = [0 for j in range(size + 1)]	# initalize list with zeroes
		temp[y[i]] = 1
		newY.append(temp)	# add to matrix
	return np.matrix(newY)

def test(a,b, split,alpha):
	"""
	Runs the linear least squares classifier
	:param a:	All the data
	:param b:	All the classes corresponding to data
	:param split: 	Where to split data for training
					Ex: 40 trains with 40% and tests with 60%
	"""

	# Build weight vector from training data
	#W = train(a[:split],b[:split])
	W = ridge(a[:split],b[:split],alpha)
	# Build test sets
	x = a[split:]
	y = b[split:]

	total = y.shape[0]
	i = 0
	hits = 0
	# Predict the class of each xi, and compare with given class
	for i in range(total):
		prediction = predict(W,x[i])
		actual = list(y[i].A1)
		if prediction == actual:
			#print 'Prediction success: Predicted : {} Actual: {}'.format(prediction, actual)
			hits += 1
		#else:
			#print 'Prediction failed: Predicted : {} Actual: {}'.format(prediction, actual)
		accuracy = hits/float(total)*100
	print "Accuracy = " + str(accuracy) + "%", "(" + str(hits) + "/" + str(total) + ")" + " while alpha = " + str(alpha)

def usage():
	return 'usage: %s <data file> \n' % os.path.basename( sys.argv[ 0 ] )

def readFile(fileName,head,data,classes):
	f = open(fileName) # open data file
	try:
		# parse file
		for line in f:
			if line == "\n" or line == "": continue # skip empty lines
			line = line.strip("\n").split(",")		# split line
			if head:
				# Convert raw data to floats and add to data list
				data.append(map(lambda x: float(x), line[0:]))
				# Add class to list
				classes.append(line[0])
			else:
				# Convert raw data to floats and add to data list
				data.append(map(lambda x: float(x), line[:-1]))
				# Add class to list
				classes.append(line[-1])

	finally:
		f.close()

def formatData(fileName,head):
	data = []
	classes = []
	readFile(fileName,head,data,classes)

	# Convert class names to a number
	classes = map(lambda x: list(set(classes)).index(x), classes)

	# Final preperations for attributes and classes
	x = np.matrix(data)
	y = fixLabels(classes)
	return (x,y)

def main():
	# Check command-line arguments
	if len(sys.argv) < 2:
		print usage()
		sys.exit(1)
	# The head flag means the class is at the beginning of each line in the data file
	# Default is at the end of each line
	head = False
	if "--head" in sys.argv:
		head = True

	(xTrain,yTrain) = formatData(sys.argv[1],head)
	size = xTrain.shape[0]
	splitAfterTrainingSet = xTrain.shape[0]

	(xTest,yTest) = formatData(sys.argv[2], head)
	size += xTest.shape[0]
	size -= 1 #substract 1 as the array starts from zero

	x = np.concatenate((xTrain,xTest))
	y = np.concatenate((yTrain,yTest))

	# scale data so it fits in range (0,1)
	for i in range(size):
		x[i] = x[i] / x.max()

	alphaLasso = [1e-15, 1e-10, 1e-8, 1e-5,1e-4, 1e-3,1e-2, 1, 5, 10]
	for alpha in alphaLasso:
		test(x,y,splitAfterTrainingSet,alpha)

# Python doesnt call main() by default
if __name__ == "__main__":
	main()
