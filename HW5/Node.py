import Utils, sys

class Node:
    def __init__(self, name):
        self.name = name
        self.attribute = {}
        self.split = None  # information of the best split so far
        self.parent = None
        self.children = []  # list of Nodes
        self.data = []
        self.processedAttributes = []
        self.unprocessedAttributes = []
        self.classIndex = []
        self.probabilityIndex = []
        return


def visitTree(node, target, criteria):

    # if there is no data or all the data are either 0 or 1 or the node is a leaf
    # then stop this recursion

    isPureNode = False

    for prob in node.probabilityIndex:
        if prob == 1:
            isPureNode = True

    if len(node.unprocessedAttributes) == 0 or len(node.data) == 0 or isPureNode == True:
        numberOfClasses = Utils.retrieveSet(node.data, target)
        Utils.computeStatistics(node, numberOfClasses, target)
        return

    # find the best attribute for split
    numberOfClasses = Utils.retrieveSet(node.data, target)
    Utils.computeStatistics(node, numberOfClasses, target)

    splits = []
    for item in node.unprocessedAttributes:
        if criteria == '0': response = Utils.getBestAttributeEntropy(node.data, item, target)
        elif criteria == '2': response = Utils.getBestAttributeGini(node.data, item, target)
        elif criteria == '1': response = Utils.getBestAttributeRegression(node.data, item, target)
        else: response = Utils.getBestAttributeEntropy(node.data, item, target)
        splits.append(response)

    splits.sort(key=lambda k: k['infoLoss'])
    bestAttribute = splits[0]
    node.attribute['name'] = bestAttribute['attribute']
    node.processedAttributes.append(node.attribute)

    # create the children
    ranges = Utils.retrieveSet(node.data, bestAttribute['attribute'])
    for item in ranges:
        child = Node('')
        child.parent = node
        child.split = {
            'attribute': node.attribute['name'],
            'value': item,
        }
        # child.name = child.parent.name + '|' + child.split['attribute'] + ':' + str(child.split['value'])
        child.name = child.split['attribute'] + ':' + str(child.split['value'])
        for attr in node.processedAttributes:
            child.processedAttributes.append(attr)
            if attr['name'] in node.unprocessedAttributes:
                node.unprocessedAttributes.remove(attr['name'])
        for element in node.unprocessedAttributes:
            child.unprocessedAttributes.append(element)
        node.children.append(child)

    for eg in node.data:
        for child in node.children:
            if child.split['value'] == eg[node.attribute['name']]:
                child.data.append(eg)
    node.data = []

    for child in node.children:
        visitTree(child, target, criteria)
    return

def visiTreeForTest(node, example, predictionMatrix, target):
    # if it is leaf then make a decision for the example
    if len(node.children) == 0:
        maxProbability = -sys.maxsize
        maxProbabilityIndex = None
        for pIndex in range(0, len(node.probabilityIndex)):
            if node.probabilityIndex[pIndex] > maxProbability:
                maxProbability = node.probabilityIndex[pIndex]
                maxProbabilityIndex = pIndex
        predictedClass = node.classIndex[maxProbabilityIndex]

        if predictedClass == example[target]:
            predictionMatrix.append((example[target], predictedClass, True))
        else:
            predictionMatrix.append((example[target], predictedClass, False))

        return

    else:
        # else recursively go do the child
        exampleAttributeValue = example[node.attribute['name']]
        for child in node.children:
            if child.split['value'] == exampleAttributeValue:
                visiTreeForTest(child, example, predictionMatrix, target)
                return

        maxProbability = -sys.maxsize
        maxProbabilityIndex = None
        for pIndex in range(0, len(node.probabilityIndex)):
            if node.probabilityIndex[pIndex] > maxProbability:
                maxProbability = node.probabilityIndex[pIndex]
                maxProbabilityIndex = pIndex
        predictedClass = node.classIndex[maxProbabilityIndex]

        if predictedClass == example[target]:
            predictionMatrix.append((example[target], predictedClass, True))
        else:
            predictionMatrix.append((example[target], predictedClass, False))

    return


def printTree(node, depth, outputFileName):
    file = open(outputFileName, 'a')
    depth = depth
    for i in range(0, depth):
        file.write("|--")
        # print('|--', end='')
    if len(node.children) > 0:
        file.write('{0}\n'.format(node.name))
        # print(f'{node.name}')
        depth = depth + 1
    else:
        file.write('{0}\n'.format(node.name))
        # print(f'{node.name}')
    file.close()
    for child in node.children:
        printTree(child, depth, outputFileName)

