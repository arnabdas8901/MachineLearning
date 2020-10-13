#######################################################
## Script: kNN Learner with IB2 case base 
## Argument: 1. data   : Input training data file
##           2. output : File to write missclassification error for [2-10]NN and IB2 casebase for 4NN
## Output: Writes missclassification error [2-10]NN and IB2 casebase for 4NN in tsv file
## Limitation: i)Input features must be numerical, no preprocessing of input feature
##             ii) A typical weight based labelling used for estimating label, not generic  
## owner: Arnab Das
## date: 05/01/2019
#######################################################

###Imports
import os
import csv
import sys
import math
import argparse

###Declaring perser for cmmand line arguments
prsr = argparse.ArgumentParser()
prsr.add_argument('--data', required=True)
prsr.add_argument('--output', required=True)

###Parsing argments
args = prsr.parse_args()


### Checking and removing existing file
if os.path.isfile(args.output):
	print("Removing existing file")
	os.remove(args.output)


###Initialising some variable
data_list = []
instance_list = []
caseBase = []
otherInst = []
fourNN_caseBase = []
error_List = [0,0,0,0,0]

### Function to read data file from command line argument --data		
def read_DataFile():
	with open(args.data) as data_file:
		data = csv.reader(data_file, delimiter='	')
		for row in data:
			if any(row):
				data_list.append(row)
	data_file.close()


### Function for data write for csv file and console
def	data_writer(targetList,prop):
	with open(args.output,'a+',newline=prop) as op:
		cursor = csv.writer(op,delimiter = "	")
		cursor.writerows([targetList])
	op.close()


# Class for each instance
class instance:
	label = ''
	attb1 = 0
	attb2 = 0
	def __init__(self,dataPoint):
		self.label = dataPoint[0]
		self.attb1 = float(dataPoint[1])
		self.attb2 = float(dataPoint[2])

	def getDist(self, inst):
		return ((self.attb1 - inst.attb1)**2 + (self.attb2 - inst.attb2)**2)**0.5

# function to estimate label based on case base and particular weight function using KNN technique
def estimateLabel_learn(inst, caseBase,k):
	weights = {}
	dist_Dict = {}
	for case in caseBase:
		dist_Dict.update({case.getDist(inst):case})
	distances = sorted(dist_Dict.items() , key=lambda x: x[0])[:k]
	max_dist = distances[-1][0]
	min_dist = distances[0][0]

	for tups in distances:
		weight = 1 if max_dist == min_dist else (max_dist - tups[0])/(max_dist- min_dist)
		weights[tups[1].label] = weights.get(tups[1].label, 0) + weight

	estimatedLabel = sorted(weights.items() , reverse=True, key=lambda x: x[1])[0][0]
	return estimatedLabel


#reading input data
print("Reading input data")
read_DataFile()

#converting data to instance list
print("Processing data")
for data in data_list:
	instance_list.append(instance(data))

#Processing
print("Creating case base using IB2")
iterator= 0 	
for k in [2,4,6,8,10]:
	caseBase = []
	otherInst = []
	# Logic for creating case base
	for inst in instance_list:
		if len(caseBase) == 0 :
			caseBase.append(inst)

		else:
			estimatedLabel = estimateLabel_learn(inst,caseBase,k)

			if inst.label == estimatedLabel:
				otherInst.append(inst)
			else:
				caseBase.append(inst)
	if k== 4:
		fourNN_caseBase = caseBase
				
	# Logic for testing		
	for tInst in otherInst:
		testlabel = estimateLabel_learn(tInst,caseBase,k)
		if tInst.label != testlabel:
			error_List[iterator] = error_List[iterator] +1

	iterator = iterator + 1
			
# writing date in output file
print("Writing output")
data_writer(error_List,"")
for cases in fourNN_caseBase :
	data_writer([cases.label,cases.attb1,cases.attb2],"")

print("Process Finished")	
