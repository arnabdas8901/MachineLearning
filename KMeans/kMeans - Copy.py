#######################################################
## Script: kNN Learner with IB2 case base 
## Argument: 1. data   : Input training data file
##           2. output : File to write missclassification error for [2-10]NN and IB2 casebase for 4NN
## Output: Writes missclassification error [2-10]NN and IB2 casebase for 4NN in tsv file
## Limitation: i)Input features must be numerical, no preprocessing of input feature
##             ii) A typical weight based labelling used for estimating label, not generic  
## owner: Arnab Das, Israt Nowshin, Saiyudh Mannan
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

### Identifying data output derectory
directory = os.path.dirname(args.output)

### Identifying file name
dataFileName = os.path.basename(args.data)
baseName = dataFileName.split(".")[0]

### Creating output filename format
outputFileName_Proto=baseName+"-Proto"+".tsv"
outputFileName_Progr=baseName+"-Progr"+".tsv"


### Checking and removing existing file
if os.path.isfile(os.path.join(directory,outputFileName_Proto)):
	print("Removing existing Proto file")
	os.remove(os.path.join(directory,outputFileName_Proto))

if os.path.isfile(os.path.join(directory,outputFileName_Progr)):
	print("Removing existing Progr file")
	os.remove(os.path.join(directory,outputFileName_Progr))	


###Initialising some variable
data_list = []
instance_list = []
prototype_List = []
centre_List = []

### Function to read data file from command line argument --data		
def read_DataFile():
	with open(args.data) as data_file:
		data = csv.reader(data_file, delimiter='	')
		for row in data:
			if any(row):
				data_list.append(row)
	data_file.close()


### Function for data write for csv file and console
def	data_writer(targetList,prop,outputFile):
	with open(outputFile,'a+',newline=prop) as op:
		cursor = csv.writer(op,delimiter = "	")
		cursor.writerows([targetList])
	op.close()


# Class for each instance
class instance:
	attb1 = 0
	attb2 = 0
	def __init__(self,dataPoint):
		self.attb1 = float(dataPoint[1])
		self.attb2 = float(dataPoint[2])

	

class prototype:
	attb1 = 0
	attb2 = 0
	cluster_list = []

	def __init__(self,dataPoint):
		self.attb1 = dataPoint[0]
		self.attb2 = dataPoint[1]
		self.cluster_list = []

	def getDist(self, inst):
		return ((self.attb1 - inst.attb1)**2 + (self.attb2 - inst.attb2)**2)**0.5

	def getSqrErr(self):
		totErr = 0
		for points in self.cluster_list:
			totErr = totErr + self.getDist(points)**2
		return totErr

	def updateCluster(self,inst):
		self.cluster_list.append(inst)
		
	def updatePrototype(self):
		sumAttb1 = 0
		sumAttb2 = 0

		for points in self.cluster_list:
			sumAttb1 = sumAttb1 + points.attb1
			sumAttb2 = sumAttb2 + points.attb2

		self.attb1 = sumAttb1/len(self.cluster_list)
		self.attb2 = sumAttb2/len(self.cluster_list)
		self.cluster_list = []

	def getPrototype(self):
		return str(self.attb1) + "," + str(self.attb2)


#reading input data
print("Reading input data")
read_DataFile()

#converting data to instance list
print("Processing data")
for data in data_list:
	instance_list.append(instance(data))


#initialising prototypes
prototype_List.append(prototype([2.75,3]))
prototype_List.append(prototype([3.25,0]))
#prototype_List.append(prototype([0,3]))

for prots in prototype_List:
	centre_List.append(prots.getPrototype())
	

#processing
print("Moving prototypes/cluster centres")
previous_SqrErr = 0
squareError = 0
while True :
	previous_SqrErr = squareError
	squareError = 0
	data_writer(centre_List,"",os.path.join(directory,outputFileName_Proto))	
	centre_List = []

	for inst in instance_list:
		dist_dict = {}

		for prots in prototype_List:
			dist_dict.update({prots.getDist(inst):prots})

		nearestProt = sorted(dist_dict.items(), key = lambda x: x[0])[0][1]
		nearestProt.updateCluster(inst)

	for prots in prototype_List:
		squareError = squareError + prots.getSqrErr()
		for insts in prots.cluster_list:
			print(insts.attb1, insts.attb2)
		print ("-------------")	
		prots.updatePrototype()
		centre_List.append(prots.getPrototype())

	data_writer([squareError],"",os.path.join(directory,outputFileName_Progr))

	if abs(squareError - previous_SqrErr) < 0.5 :
		break
		
print("Data Written to appropriate files")
print("Process finished")


		

