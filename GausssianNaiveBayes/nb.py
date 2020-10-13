#######################################################
## Script: Gaussian Naive Bayes Learner
## Argument: 1. data   : Input training data file
##           2. output : File to write Gaussian params for each feature and missclassification error 
## Output: Writes Gaussian params for each feature and data missclassification error in tsv file
## Limitation: Input features must be numerical, no preprocessing of input feature 
## owner: Arnab Das, Israt Nowshin, Saiyudh Mannan
## date: 18/12/2019
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
data_gaussian_list = {}
uniqueue_class = ()
attr_num = 0
missclassificationErr = 0

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

### Function to process input data and to find feature count and unique class label
def process_InputData(inputData):
	class_list = []
	### identifyng class of data and unique class
	for row in inputData:
		class_list.append(row[0])
	global uniqueue_class	
	uniqueue_class = set(class_list)

	### identifying attribute number
	attb_data = []
	for cols in inputData[0]:
		if len(cols)>0:
			attb_data.append(cols)
	global attr_num		
	attr_num=(len(attb_data)-1)



def calculate_gaussian_prop(subData, totalDataCount):
	gausProp = []
	classCounter = len(subData)
	for feature in range(attr_num):
		mean = sum([float(row[feature]) for row in subData])/classCounter
		var = sum([(float(row[feature])-mean)**2 for row in subData])/(classCounter-1)
		gausProp.append(mean)
		gausProp.append(var)
	gausProp.append(classCounter/totalDataCount)	

	return gausProp	

print("Reading input data")
read_DataFile()

print("Processing data")
process_InputData(data_list)

print("Identifying Gaussian distribution (mean and variance) for features for each class")
for value in sorted(uniqueue_class):
	sub_data_list = []
	for row in data_list:
		if row[0] == value:
			sub_data_list.append(row[1:])
	data_gaussian_list[value]=(calculate_gaussian_prop(sub_data_list,len(data_list)))

print("Classifying input data")
for rows in data_list:
	mlClass = {}
	for keys,value in data_gaussian_list.items():
		pfc = 1
		for cols in range(attr_num):
			pfc= pfc* ((2 * math.pi * value[2*cols + 1])**-0.5) * math.exp(-((float(rows[cols+1]) - value[2*cols])**2)    /    (2*value[2*cols + 1]))
		mlClass[keys] = pfc*value[-1]	
	if rows[0]  != sorted(mlClass.items() , reverse=True, key=lambda x: x[1])[0][0]:
		missclassificationErr += 1


print("Writing output")
for key,value in data_gaussian_list.items():
	data_writer(value,"\n") 
data_writer([missclassificationErr],"")
print("Process Finished")
