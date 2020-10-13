#######################################################
## Script: Decision tree maker
## Argument: 1. data : Input training data file
##           2. output : file to write output data
## Output: Writes decision tree in xml file
## Limitation: can't handle missing attribute
## owner: Arnab Das, Israt Nowshin, Saiyudh Mannan
## date: 16/11/2019
####################################################### 


###Imports
import os
import csv
import sys
import argparse
import math
import xml.etree.ElementTree as ET
from collections import Counter


###Declaring perser for cmmand line arguments
prsr = argparse.ArgumentParser()
prsr.add_argument('--data', required=True)
prsr.add_argument('--output', required=True)

###Parsing argments
args = prsr.parse_args()


###Initialising variable for data set
data_list = []

### Function to read data file from command line argument --data		
def read_DataFile():
	with open(args.data) as data_file:
		data = csv.reader(data_file, delimiter=',')
		for row in data:
			if any(row):
				data_list.append(row)
	data_file.close()

### creates the root element of the output xml 
def createRoot():
	global tree
	root=ET.Element("tree")
	tree=ET.ElementTree(root)
	root.set("entropy",str(data_entropy))
	return root

### calculates entropy for a subset of data
def calculate_Entropy(subset):
	subsetLen = len(subset)
	subsetClassList = [lcol[-1] for lcol in subset]
	uniqueClass = list(Counter(subsetClassList).keys())
	groupCount = list(Counter(subsetClassList).values())
	classCount = len(uniqueClass)
	entropy = 0.0
	if classCount == 1:
		return entropy
	for i in range(classCount):
		p = float(groupCount[i])/subsetLen
		entropy = entropy - p*math.log(p,logbase)
	return entropy	

#################################################
## This function performs following operations
## 1. calculate entropy for the subset
## 2. Based on entropy decides leaf node or not
## 3. Choses best fit attribute for next node based on max information gain
## 4. loops over all attribute unique values, sort them according to subset entropy 
##     and calls itself recursively with shorted subset
## 5. adds noes in output xml document
#################################################

def chooseNode(subsetIn,attNames,tempNode):
	gain = 0.0
	setEntropy = calculate_Entropy(subsetIn)

	if setEntropy == 0.0 or len(subsetIn[0]) == 1:
		tempNode.text = str(subsetIn[0][-1])
	else:
		node=0	
		for eachAtt in range(len(subsetIn[0])-1):
			nodeName=eachAtt
			totalEntropy= 0.0
			attribGain = 0.0
			for eachClass in list(Counter([col[eachAtt] for col in subsetIn]).keys()):
				subset = []
				for row in subsetIn:
					if row[eachAtt] == eachClass:
						subset.append(row)		
				partialEntropy=calculate_Entropy(subset)
				totalEntropy = 	totalEntropy+(float(len(subset))/dataSetCount)*partialEntropy
			attribGain=data_entropy- totalEntropy
			if attribGain > gain:
				node = nodeName
				gain = attribGain

		splitList = list(Counter([col[node] for col in subsetIn]).keys())

		branchList = []

		for eachClass in splitList:
			subset = []
			for row in subsetIn:
				if row[node] == eachClass:
					subset.append(row)
			newset = [rows[:node]+rows[node+1:] for rows in subset]
			branchList.append([eachClass,calculate_Entropy(newset)])

		branchList.sort(key = lambda x: x[1])

		counter = 0
		for eachClass in [i[0] for i in branchList]:
			#print("featre=",attNames[node])
			#print("value=",eachClass)
			subset = []
			for row in subsetIn:
				if row[node] == eachClass:
					subset.append(row)
			newset = [rows[:node]+rows[node+1:] for rows in subset]
			nd = ET.Element("node")
			nd.set("entropy",str(branchList[counter][1]))
			nd.set("feature",str(attNames[node]))
			nd.set("value",str(eachClass))
			tempNode.append(nd)
			chooseNode(newset,attNames[:node]+attNames[node+1:],nd)
			counter+=1			



####main script
print("Reading training data")
read_DataFile()
dataSetCount = len(data_list)
logbase = len(list(Counter([col[-1] for col in data_list]).keys()))
data_entropy = calculate_Entropy(data_list)

print("Creating xml output root element")
root=createRoot()

attCount = len(data_list[0])-1

### list to hold attribute names
attNameList = []
for cnt in range(attCount):
	attNameList.append("att"+str(cnt))
print("Creating decision tree")	
chooseNode(data_list,attNameList,root)

### writing output
print("Writing output file")
myFile = open(args.output,'w')
myFile.write(ET.tostring(root).decode())
print("Execution complete")
