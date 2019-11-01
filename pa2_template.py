'''
In PA 2, you might finish the assignment with only built-in types of Python 3.
However, one may choose to use higher level libraries such as numpy and scipy.
Add your code below the TO-DO statement and include necessary import statements.
'''

import sys
import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OrdinalEncoder

def main():
    
    '''
    Get the first command line argument of the program.
    For example, sys.argv[1] could be a string such as 'breast_cancer.csv' or 'titanic_train.csv'
    '''
    szDatasetPath = sys.argv[1]

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
    for featCol, feature in enumerate(listColUniqueVals, 0):
        if(featCol == len(listColUniqueVals) - 1):
            # skip the final row as it is the class label
            break

        # get all possible class labels
        labels = listColUniqueVals[-1]
        
        # calculate the level 1 decision tree for the feature & compute the training error
        computeDecisionTree(feature, listData, featCol, labels)

    # Construct a full decision tree on the dataset and compute the training error
    # TO-DO: add your code here
    

    return None

# compute the level 1 decision tree and display the error rate
def computeDecisionTree(feature, data, featCol, labels):
    # get the index of our class label
    classIndex = len(data[0]) - 1

    # dictionary of dictionaries for each class label
    catDicts = {}
    
    # get a feature split count for each class label of the dataset
    for label in labels:
        # initialize our dictionary to track label occurences for the feature split
        catDict = initDict(feature)

        # count all occurences of the label class for our feature split in our dataset
        countLabelOccurences(catDict, data, featCol, classIndex, label)

        # add the computed mapping to our cumulative dictionary
        catDicts[label] = catDict

    # generate the level 1 decision tree using our calculated dictionaries
    labelMap = generateDecisionTree(catDicts, feature, labels)

    # compute the error rate of the level 1 decision tree
    errorRate = calcErrorRate(labelMap, catDicts, feature, len(data))

    # print our level 1 decision tree error rates
    print("Feature [" + str(featCol) + "]")
    #for dict_a in catDicts:
    #    print("\tlabel: " + dict_a)
    #    print("\t\t" + str(catDicts[dict_a]))

    #print(labelMap)
    print("\tError Rate: " + str(errorRate) + "\n")
        
# calculate the error rate for the level 1 decision tree
def calcErrorRate(labelMap, catDicts, feature, dataCount):
    # count of correctly classified training samples
    correctCount = 0

    # loop through all categories of the current feature
    for cat in feature:
        # get the correct label for the category
        correctLabel = labelMap[cat]

        # get the number of correctly predicted samples and add them to our count
        correctCount += catDicts[correctLabel][cat]

    # calculate the percentage of correctly classified samples
    correctRate = correctCount/dataCount

    # calculate the error rate as 1 - the correct percentage
    return 1 - correctRate    

# compute the level 1 decision tree    
def generateDecisionTree(catDicts, feature, labels):
    # our level 1 decision tree
    labelMap = {}

    # loop through all categories of our feature split
    for cat in feature:
        # used to find the class with highest count for each split
        maxLabel = None
        maxCount = -1
        
        # loop through each class label dictionary and find the label with highest count
        for label in labels:
            # get the count for the current label's category
            count = catDicts[label][cat]

            # find the max count
            if(count > maxCount):
                # store the max count & corresponding label
                maxLabel = label
                maxCount = count 

        # store the maxLabel in our decision tree for the category
        labelMap[cat] = maxLabel

    # return our computed level 1 decision tree
    return labelMap

# count the number of occurences of the class of interest for the split feature
def countLabelOccurences(catDict, data, featCol, classIndex, labelVal):
    # loop through all samples
    for sample in data:
        # find the actual label of the current sample
        curLabel = sample[classIndex]

        # if the class label is our class of interest, we count its feature value
        if(curLabel == labelVal):
            # find the category value for the feature of our sample
            curCategory = sample[featCol]

            # count the occurence of the category value for our class of interest's feature
            catDict[curCategory] += 1

# split our feature on every categorical label and return a zeroed
# mapping from split value to count
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
