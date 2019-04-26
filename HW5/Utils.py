import csv, sys, math

def processInput(fileName):
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

    return data, attributes

#data = processInput('w.csv')[0]

def retrieveSet(data, attributeName):
    list = []
    for item in data:
        list.append(item[attributeName])
    return set(list)

def getFromSetByIndex(set, index):
    count = 0
    for item in set:
        if count is index:
            return item
        count = count + 1
    return

def getBestSplitCategorical(list, attributeName):
    list.sort(key=lambda k: k[attributeName])
    unique = retrieveSet(list, 'class')
    ranges = retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item['class'] == getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    bestSplit = {
        'attribute' : attributeName,
        'value' : None,
        'entropy': sys.maxsize,
        'averageEntropy': None
    }

    chunks = []

    averageEntropy = 0

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element['class'] == getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1

        entropy = 0
        total = sum(countMatrix)
        for index in range(0, len(unique)):
            p = (countMatrix[index] + .001)/(total + .001)
            if p == 1 and len(unique) == 1: entropy = entropy - 0
            else: entropy = entropy - p * math.log(p, len(unique))

        if entropy < bestSplit['entropy']:
            bestSplit['value'] = item
            bestSplit['entropy'] = entropy

        chunk = {
            'attribute': attributeName,
            'value': item,
            'entropy': entropy
        }

        averageEntropy = averageEntropy + entropy * (total / len(list))
        chunks.append(chunk)

    bestSplit['averageEntropy'] = averageEntropy
    return bestSplit, chunks

def getBestSplitCategoricalLambdaAssociation(list, attributeName):
    list.sort(key=lambda k: k[attributeName])
    unique = retrieveSet(list, 'class')
    ranges = retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item['class'] == getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    probabilityIndexForAttributeValues = []

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element['class'] == getFromSetByIndex(unique, index):
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
                if element['class'] == classToPredict:
                    if not prediction: predictionError += 1
                else:
                    if prediction: predictionError += 1


    numberOfPredictionErrorWhenAttributeIsIgnored = 1 - (totalMatrix[0]/sum(totalMatrix))
    numberOfPredictionErrorWhenAttributeIsConsidered = predictionError/sum(totalMatrix)
    _lambda = (numberOfPredictionErrorWhenAttributeIsIgnored - numberOfPredictionErrorWhenAttributeIsConsidered)/ (numberOfPredictionErrorWhenAttributeIsIgnored + .001)

    bestSplit = {
        'attribute': attributeName,
        'value': None,
        'entropy': 1 - _lambda,
        'averageEntropy': 1 - _lambda
    }

    chunks = []

    return bestSplit, chunks

def getBestSplitCategoricalGiniIndex(list, attributeName):
    list.sort(key=lambda k: k[attributeName])
    unique = retrieveSet(list, 'class')
    ranges = retrieveSet(list, attributeName)

    totalMatrix = [0] * len(unique)
    for item in list:
        for index in range(0, len(unique)):
            if item['class'] == getFromSetByIndex(unique, index):
                totalMatrix[index] = totalMatrix[index] + 1

    bestSplit = {
        'attribute' : attributeName,
        'value' : None,
        'entropy': sys.maxsize,
        'averageEntropy': None
    }

    chunks = []

    averageEntropy = 1

    for item in ranges:
        countMatrix = [0] * len(unique)
        for element in list:
            if element[attributeName] == item:
                for index in range(0, len(unique)):
                    if element['class'] == getFromSetByIndex(unique, index):
                        countMatrix[index] = countMatrix[index] + 1

        entropy = 0
        total = sum(countMatrix)
        for index in range(0, len(unique)):
            p = (countMatrix[index] + .001)/(total + .001)
            if p == 1 and len(unique) == 1: entropy = entropy - 0
            else: entropy = entropy - p * p

        if entropy < bestSplit['entropy']:
            bestSplit['value'] = item
            bestSplit['entropy'] = entropy

        chunk = {
            'attribute': attributeName,
            'value': item,
            'entropy': entropy
        }

        averageEntropy = averageEntropy - entropy
        chunks.append(chunk)

    bestSplit['averageEntropy'] = averageEntropy
    return bestSplit, chunks


def computeStatistics(node, numberOfClasses):
    classMatrix = [''] * len(numberOfClasses)
    probabilityIndex = [0] * len(numberOfClasses)
    classMatrixIndex = 0
    for item in numberOfClasses:
        classMatrix[classMatrixIndex] = item
        classMatrixIndex = classMatrixIndex + 1
    totalMatrix = [0] * len(numberOfClasses)
    for item in node.data:
        for index in range(0, len(numberOfClasses)):
            if item['class'] == getFromSetByIndex(numberOfClasses, index):
                totalMatrix[index] = totalMatrix[index] + 1
    total = sum(totalMatrix)
    for index in range(0, len(probabilityIndex)):
        probabilityIndex[index] = (totalMatrix[index] + .001) / (total + .001)
    node.classIndex = classMatrix
    node.probabilityIndex = probabilityIndex
    return

def calCulateFMeasure(predictioMatrix):
    classes = []
    predictedClasses = []
    outcome = []
    for item in predictioMatrix:
        classes.append(item[0])
        predictedClasses.append(item[1])
        outcome.append(item[2])

    uniqueClasses = set(classes)

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


    accuracy = (TP[1] + TN[1]) / (TP[1] + FP[1] + TN[1] + FN[1] + .001)
    precision = TP[1] / (TP[1] + FP[1] + .001)
    recall = TP[1] / (TP[1] + FN[1] + .001)
    f1score = (2 * precision * recall) / (precision + recall + .001)
    return [TP[1], TN[1], FP[1], FN[1], accuracy, precision, recall, f1score]