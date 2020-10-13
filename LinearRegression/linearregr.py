###Imports
import os
import csv
import sys
import argparse

###Declaring perser for cmmand line arguments
prsr = argparse.ArgumentParser()
prsr.add_argument('--data', required=True)
prsr.add_argument('--learningRate', required=True, default= 0.0001, type=float)
prsr.add_argument('--threshold', required=True, default= 0.0001, type=float)

###Parsing argments
args = prsr.parse_args()

### Identifying data source derectory
directory = os.path.dirname(args.data)

### Identifying file name
dataFileName = os.path.basename(args.data)
baseName = dataFileName.split(".")[0]

### Creating output filename format
outputFileName="solution_"+baseName+"_eta"+str(args.learningRate)+"_thres"+str(args.threshold)+".csv"	


### Checking and removing existing file
if os.path.isfile(os.path.join(directory,outputFileName)):
	print("Removing existing file")
	os.remove(os.path.join(directory,outputFileName))

###Initialising some variable
data_list = []
train_data_length = 0
num_attribute = 0
eta = float(args.learningRate)


###Weight class
class weights:
	weight = []
	def __init__(self,length):
		for iter in range(length+1):
			self.weight.append(round(0,4))

	def get_weight(self):
		return self.weight

	def set_weight(self,grad):
		index = 0 
		for weights in self.weight:
			self.weight[index] = float(self.weight[index]) + eta*grad[index]
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
		data = csv.reader(data_file, delimiter=',')
		for row in data:
			data_list.append(row)
	data_file.close()		


###Function to calculate hypothesis output for each data point
def calculate_output(weight, data_attr):
	output = 0
	index = 0  
	for wt in weight:
		output += (float(weight[index]) * float(data_attr[index]))
		index +=1

	return output	


###Function to calculate error for each data point
def calculate_error(data_attr,output):
	y = data_attr[-1]
	return float(y) - float(output)


### Function to calculate stochastic gradient for each data point and summing to get batch gradient
def calculate_gradient( data_attr, error):
	index = 0
	for grads in grad:
		grad[index] = grad[index] + error * float(data_attr[index])
		index +=1

### Function for data write for csv file and console
def	data_writer(itr, weights, sqrErr):
	roundedWeight=[]
	roundedWeight.append(itr)
	for weight in weights:
		roundedWeight.append(format(weight,'.4f'))
	roundedWeight.append(sqrErr)

	with open(os.path.join(directory,outputFileName),'a+',newline='') as op:
		cursor = csv.writer(op, dialect='excel')
		consoleWrite = csv.writer(sys.stdout)
		cursor.writerows([roundedWeight])
		consoleWrite.writerows([roundedWeight])
	op.close()	




###Read the data file and calculate the number of training data and attribute
read_DataFile()	
train_data_length=len(data_list)
num_attribute=(len(data_list[0])-1)

### Creating weight list and initialising
weightObj = weights(num_attribute)
iteration = 0
square_Error = 0

while True :
	### Instantiating data instance
	inst = instance()

	### Initialising square error 
	previous_sqr_error = square_Error
	square_Error = 0

	###Initialising gradient
	grad = [0] * len(weightObj.get_weight())

	###Lopping over entire data set
	for row in data_list:
		inst.set_attrib(row[:-1])
		hypothesis_op = calculate_output(weightObj.get_weight(),inst.data_inst)
		error = calculate_error(row,hypothesis_op)
		square_Error += float(error**2)
		calculate_gradient(inst.data_inst,error)

	data_writer(iteration, weightObj.weight, format(round(square_Error,4),'.4f'))
	weightObj.set_weight(grad)
	iteration += 1

	###Condition to get out of the infinite loop
	if abs(previous_sqr_error - square_Error) < float(args.threshold):
		break




