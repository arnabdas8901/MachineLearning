#######################################################
## Script: Perceptron Learner
## Argument: 1. data : Input training data file
##           2. output : file to write error rate per 100 iteration
##			 3. maxIteration : Maximum iteration number as termination criterion
## Output: Writes error rate per 100 iteration in tsv file
## Aspect: write output for constant and annealing learning rate
## owner: Arnab Das
## date: 27/11/2019
####################################################### 

###Imports
import os
import csv
import sys
import argparse

###Declaring perser for cmmand line arguments
prsr = argparse.ArgumentParser()
prsr.add_argument('--data', required=True)
prsr.add_argument('--output', required=True)
prsr.add_argument('--maxIteration', required=True, default= 100, type =int)

###Parsing argments
args = prsr.parse_args()


### Checking and removing existing file
if os.path.isfile(args.output):
	print("Removing existing file")
	os.remove(args.output)

###Initialising some variable
data_list = []
num_attribute = 0
eta = 1
newEta = eta


###Weight class
class weights:
	#weight = []
	def __init__(self,length):
		self.weight = []
		for iter in range(length+1):
			self.weight.append(round(0,4))

	def get_weight(self):
		return self.weight

	def set_weight(self,grad,eta):
		index = 0 
		for weights in self.weight:
			self.weight[index] = (float(self.weight[index]) + eta*grad[index])
			index +=1 

### Instance class for each data point
class instance:
	data_inst = []
		
	def set_attrib(self, row):
		self.data_inst = []
		self.data_inst.append(1)
		for attbs in row :
			self.data_inst.append(attbs)
		
### Function to read data file from command line argument --data		
def read_DataFile():
	with open(args.data) as data_file:
		data = csv.reader(data_file, delimiter='	')
		for row in data:
			data_list.append(row)
	data_file.close()		


###Function to calculate hypothesis output for each data point
def calculate_output(weight, data_attr):
	output = 0
	index = 0  
	for wt in weight:
		output += (float(weight[index]) * float(data_attr[index]))
		index = index + 1

	return output	


###Function to calculate error for each data point
def calculate_error(data_attr,output):
	dataClass = data_attr[0]
	return (1 if dataClass == "A" else 0) - (1 if output >0 else 0)


### Function to calculate stochastic gradient for each data point and summing to get batch gradient
def calculate_gradient( gradList,data_attr, error):
	index = 0
	for grads in gradList:
		gradList[index] = gradList[index] + error * float(data_attr[index])
		index += 1

### Function for data write for csv file and console
def	data_writer(errorList):
	with open(args.output,'a+',newline='') as op:
		cursor = csv.writer(op,delimiter = "	")
		cursor.writerows([errorList])
	op.close()	




###Read the data file and calculate the number of training data and attribute
print("Reading training data file ")
read_DataFile()
attb_data = []
for cols in data_list[0]:
	if len(cols)>0:
		attb_data.append(cols)

num_attribute=(len(attb_data)-1)

### Creating weight list and initialising
weightObj = weights(num_attribute)
weightObjAnneal = weights(num_attribute)
iteration = 0
errorRate_list = []
errorRate_list_anneal = []
first_iter = True

print("Iterating in batch mode")
while iteration <= args.maxIteration :
	### Instantiating data instance
	inst = instance()
	errorRate = 0
	errorRateAnneal	= 0

	###Initialising gradient
	grad = [0] * len(weightObj.get_weight())
	gradAnneal = [0] * len(weightObj.get_weight())

	###Lopping over entire data set
	for row in data_list:
		inst.set_attrib(row[1:])
		hypothesis_op = calculate_output(weightObj.get_weight(),inst.data_inst)
		hypothesis_op_anneal = calculate_output(weightObjAnneal.get_weight(),inst.data_inst)
		error = calculate_error(row,hypothesis_op)
		error_anneal = calculate_error(row,hypothesis_op_anneal)
		if error != 0:
			errorRate +=1
		if error_anneal != 0:
			errorRateAnneal +=1		
		calculate_gradient(grad,inst.data_inst,error)
		calculate_gradient(gradAnneal,inst.data_inst,error_anneal)

	weightObj.set_weight(grad,eta)
	newEta = eta/(iteration+1) 
	weightObjAnneal.set_weight(gradAnneal, newEta)
	errorRate_list.append(errorRate)
	errorRate_list_anneal.append(errorRateAnneal)

	if  first_iter == False and iteration % 100 == 0:
		data_writer(errorRate_list)
		data_writer(errorRate_list_anneal)
		errorRate_list = []
		errorRateAnneal = []

	iteration += 1
	first_iter = False

print("processing finished")	

