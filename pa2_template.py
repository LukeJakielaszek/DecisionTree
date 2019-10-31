'''
In PA 2, you might finish the assignment with only built-in types of Python 3.
However, one may choose to use higher level libraries such as numpy and scipy.
Add your code below the TO-DO statement and include necessary import statements.
'''

import sys
import csv

def main():
    
    '''
    Get the first command line argument of the program.
    For example, sys.argv[1] could be a string such as 'breast_cancer.csv' or 'titanic_train.csv'
    '''
    #szDatasetPath = sys.argv[1]
	# Comment out the following line and uncomment the above line in your final submission
    szDatasetPath = 'breast_cancer.csv'

    '''
    Read the data from the csv file
    listColNames[j] stores the jth column name
    listData[i][:-1] are the features of the ith example
    listData[i][-1] is the target value of the ith example
    '''
    listColNames = [] # The list of column names
    listData = [] # The list of feature vectors of all the examples
    nRow = 0
    with open(szDatasetPath) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        for row in csvReader:
            if 0 == nRow:
                listColNames = row
            else:
                listData.append(row)
            nRow += 1

    '''
    Scan the data and store the unique values of each column.
    listColUniqueVals[j] stores a list of unique values of the jth column
    '''
    listColUniqueVals = [[] for i in range(len(listColNames))]
    for example in listData:
        for i in range(len(example)):
            if example[i] not in listColUniqueVals[i]:
                listColUniqueVals[i].append(example[i])

    # For each feature, compute the training error of a one-level decision tree
    # TO-DO: add your code here
    for featCol, feature in enumerate(listColUniqueVals, 0):
        if(featCol == len(listColUniqueVals) - 1):
            # skip the final row as it is the class label
            break

        # get all possible class labels
        labels = listColUniqueVals[-1]
        
        # calculate the level 1 decision tree for the feature
        computeDecisionTree(feature, listData, featCol, labels)

    # Construct a full decision tree on the dataset and compute the training error
    # TO-DO: add your code here

    return None

# compute the level 1 decision tree
def computeDecisionTree(feature, data, featCol, labels):
    # get the index of our class label
    classIndex = len(data[0]) - 1

    catDicts = {}
    
    # get a feature split count for each class label of the dataset
    for label in labels:
        # create a split for the feature to track label occurences
        catDict = initDict(feature)

        # count all occurences of the label class for our feature split in our dataset
        countLabelOccurences(catDict, data, featCol, classIndex, label)

        catDicts[label] = catDict


    labelMap = generateDecisionTree(catDicts, feature, labels)

    errorRate = calcErrorRate(labelMap, catDicts, feature, len(data))

    print("Feature [" + str(featCol) + "]")
    for dict_a in catDicts:
        print("\tlabel: " + dict_a)
        print("\t\t" + str(catDicts[dict_a]))

    print(labelMap)
    print("Error Rate: " + str(errorRate) + "\n")
        
# calculate the error rate for the level 1 decision tree
def calcErrorRate(labelMap, catDicts, feature, dataCount):
    correctCount = 0

    for cat in feature:
        # get the correct label
        correctLabel = labelMap[cat]

        correctCount += catDicts[correctLabel][cat]
    correctRate = correctCount/dataCount

    return 1 - correctRate    
    
# compute the level 1 decision tree    
def generateDecisionTree(catDicts, feature, labels):
    labelMap = {}
    
    for cat in feature:
        # used to find the class with highest count for each split
        maxLabel = None
        maxCount = -1
        
        # loop through each class label
        for label in labels:
            count = catDicts[label][cat]
            if(count > maxCount):
                maxLabel = label
                maxCount = count 

        labelMap[cat] = maxLabel

    return labelMap

# count the number of occurences of the class of interest for the split feature
def countLabelOccurences(catDict, data, featCol, classIndex, labelVal):
    # get the index with class decision
    for sample in data:
        # find the label of the current sample
        curLabel = sample[classIndex]

        # count the occurence of the positive class
        if(curLabel == labelVal):
            # find the value of the feature of index for our sample
            curCategory = sample[featCol]

            # count the occurence of the positive class for that category
            catDict[curCategory] += 1

# split our feature on every categorical label
def initDict(feature):
    # dictionary to store the split feature counts
    catDict = {}

    # loop through each categorical value in the feature    
    for cat in feature:
        # initialize the count to 0
        catDict[cat] = 0

    # return our initialized split
    return catDict    

if __name__ == '__main__':

    main()
