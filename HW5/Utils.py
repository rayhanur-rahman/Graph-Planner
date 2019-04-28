import csv, sys, math

def processInput(fileName, target):
    file = open(fileName, 'r')
    csv_reader = csv.reader(file, delimiter=',')

    data = []
    index = 0
    attributes = []

    for line in csv_reader:
        dictionary = {}
        if index == 0:
            for item in line:
                attributes.append(item)
        else:
            rowIndex = 0
            for item in line:
                dictionary[attributes[rowIndex]] = item
                rowIndex += 1

            data.append(dictionary)
        index += 1

    if target in attributes:
        attributes.remove(target)

    return data, attributes


# return unique list, discarding duplicates
def retrieveSet(data, attributeName):
    list = []
    for item in data:
        list.append(item[attributeName])
    return sorted(set(list), reverse= True)

# as set is not indexable. we need to iterate get the element in a particular index
def getFromSetByIndex(set, index):
    count = 0
    for item in set:
        if count is index:
            return item
        count = count + 1
    return

# calculate infogain using entropy
def getBestAttributeEntropy(list, attributeName, target):
    list.sort(key=lambda k: k[attributeName])
    unique = retrieveSet(list, target)
    ranges = retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item[target] == getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    bestSplit = {
        'attribute' : attributeName,
        'infoLoss': None
    }

    totalEntropy = 0

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element[target] == getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1

        entropy = 0
        total = sum(countMatrix)
        for index in range(0, len(unique)):
            p = (countMatrix[index] + .00001)/(total + .00001)
            if p == 1 and len(unique) == 1: entropy = entropy - 0
            else: entropy = entropy - p * math.log(p, len(unique))

        totalEntropy = totalEntropy + entropy * (total / len(list))

    bestSplit['infoLoss'] = totalEntropy
    return bestSplit

# using categorical regression as the selection criteria
def getBestAttributeRegression(list, attributeName, target):
    list.sort(key=lambda k: k[attributeName])
    unique = retrieveSet(list, target)
    ranges = retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item[target] == getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    probabilityIndexForAttributeValues = []

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element[target] == getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1
        probabilityIndexForAttributeValues.append(countMatrix)

    predictionError = 0
    for index in range(0, len(ranges)):
        for element in list:
            if element[attributeName] == getFromSetByIndex(ranges, index):
                classToPredict = getFromSetByIndex(unique, 0)
                probability = probabilityIndexForAttributeValues[index][0]/sum(probabilityIndexForAttributeValues[index])
                prediction = None
                if probability > 0.5: prediction = True
                else: prediction = False
                if element[target] == classToPredict:
                    if not prediction: predictionError += 1
                else:
                    if prediction: predictionError += 1


    numberOfPredictionErrorWhenAttributeIsIgnored = 1 - (totalMatrix[0]/sum(totalMatrix))
    numberOfPredictionErrorWhenAttributeIsConsidered = predictionError/sum(totalMatrix)
    _lambda = (numberOfPredictionErrorWhenAttributeIsIgnored - numberOfPredictionErrorWhenAttributeIsConsidered)/ (numberOfPredictionErrorWhenAttributeIsIgnored + .00001)

    bestSplit = {
        'attribute': attributeName,
        'infoLoss': 1 - _lambda
    }

    return bestSplit

def getBestAttributeGini(list, attributeName, target):
    list.sort(key=lambda k: k[attributeName])
    unique = retrieveSet(list, target)
    ranges = retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item[target] == getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    bestSplit = {
        'attribute' : attributeName,
        'infoLoss': None
    }

    totalGini = 1

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element[target] == getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1

        gini = 0
        total = sum(countMatrix)
        for index in range(0, len(unique)):
            p = (countMatrix[index] + .00001)/(total + .00001)
            if p == 1 and len(unique) == 1: gini = gini - 0
            else: gini = gini - p * p

        totalGini = totalGini - gini

    bestSplit['infoLoss'] = totalGini
    return bestSplit

# calculate the ratio of class = 0 and class = 1 of all the datasets in a node
def computeStatistics(node, numberOfClasses, target):
    classMatrix = [''] * len(numberOfClasses)
    probabilityIndex = [0] * len(numberOfClasses)
    classMatrixIndex = 0
    for item in numberOfClasses:
        classMatrix[classMatrixIndex] = item
        classMatrixIndex = classMatrixIndex + 1
    totalMatrix = [0] * len(numberOfClasses)
    for item in node.data:
        for index in range(0, len(numberOfClasses)):
            if item[target] == getFromSetByIndex(numberOfClasses, index):
                totalMatrix[index] = totalMatrix[index] + 1
    total = sum(totalMatrix)
    for index in range(0, len(probabilityIndex)):
        probabilityIndex[index] = (totalMatrix[index] + .00001) / (total + .00001)
    node.classIndex = classMatrix
    node.probabilityIndex = probabilityIndex
    return

# calculate confusion matrix, recall , precision and f-measure
def calculatePerformance(predictioMatrix):
    classes = []
    predictedClasses = []
    outcome = []
    for item in predictioMatrix:
        classes.append(item[0])
        predictedClasses.append(item[1])
        outcome.append(item[2])

    uniqueClasses = sorted(set(classes), reverse= True)

    TP = [0] * len(uniqueClasses)
    TN = [0] * len(uniqueClasses)
    FP = [0] * len(uniqueClasses)
    FN = [0] * len(uniqueClasses)

    for uniqueClassIndex in range(0, len(uniqueClasses)):
        for index in range(0, len(predictedClasses)):
            if classes[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) and \
                    predictedClasses[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == True:
                TP[uniqueClassIndex] += 1
            if classes[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) and \
                    predictedClasses[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == True:
                TN[uniqueClassIndex] += 1
            if classes[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and predictedClasses[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == False:
                FP[uniqueClassIndex] += 1
            if classes[index] == getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and predictedClasses[index] != getFromSetByIndex(uniqueClasses, uniqueClassIndex) \
                    and outcome[index] == False:
                FN[uniqueClassIndex] += 1


    accuracy = (TP[0] + TN[0]) / (TP[0] + FP[0] + TN[0] + FN[0] + .00001)
    precision = TP[0] / (TP[0] + FP[0] + .00001)
    recall = TP[0] / (TP[0] + FN[0] + .00001)
    f1score = (2 * precision * recall) / (precision + recall + .00001)
    return {
        'true positive': TP[0],
        'true negative': TN[0],
        'false positive': FP[0],
        'false negative': FN[0],
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f-measure': f1score
    }
