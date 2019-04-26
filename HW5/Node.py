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


def visitTree(node):
    # print(f'{node.name} ### {len(node.data)}')
    isPureNode = False

    for prob in node.probabilityIndex:
        if prob == 1:
            isPureNode = True

    if len(node.unprocessedAttributes) == 0 or len(node.data) == 0 or isPureNode == True:
        numberOfClasses = Utils.retrieveSet(node.data, 'class')
        Utils.computeStatistics(node, numberOfClasses)
        return

    numberOfClasses = Utils.retrieveSet(node.data, 'class')
    Utils.computeStatistics(node, numberOfClasses)

    splits = []
    for item in node.unprocessedAttributes:
        response = Utils.getBestSplitCategorical(node.data, item)
        # response = Utils.getBestSplitCategoricalLambdaAssociation(node.data, item)
        splits.append(response[0])

    splits.sort(key=lambda k: k['averageEntropy'])
    bestAttribute = splits[0]
    node.attribute['name'] = bestAttribute['attribute']
    node.processedAttributes.append(node.attribute)

    ranges = Utils.retrieveSet(node.data, bestAttribute['attribute'])
    for item in ranges:
        child = Node('')
        child.parent = node
        child.split = {
            'attribute': node.attribute['name'],
            'value': item,
        }
        child.name = child.parent.name + '|' + child.split['attribute'] + ':' + str(child.split['value'])
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
        visitTree(child)
    return

def visiTreeForTest(node, example, predictionMatrix):
    if len(node.children) == 0:
        maxProbability = -sys.maxsize
        maxProbabilityIndex = None
        for pIndex in range(0, len(node.probabilityIndex)):
            if node.probabilityIndex[pIndex] > maxProbability:
                maxProbability = node.probabilityIndex[pIndex]
                maxProbabilityIndex = pIndex
        predictedClass = node.classIndex[maxProbabilityIndex]

        if predictedClass == example['class']:
            predictionMatrix.append((example['class'], predictedClass, True))
        else:
            predictionMatrix.append((example['class'], predictedClass, False))

        return

    else:
        exampleAttributeValue = example[node.attribute['name']]
        for child in node.children:
            if child.split['value'] == exampleAttributeValue:
                visiTreeForTest(child, example, predictionMatrix)
                return

        maxProbability = -sys.maxsize
        maxProbabilityIndex = None
        for pIndex in range(0, len(node.probabilityIndex)):
            if node.probabilityIndex[pIndex] > maxProbability:
                maxProbability = node.probabilityIndex[pIndex]
                maxProbabilityIndex = pIndex
        predictedClass = node.classIndex[maxProbabilityIndex]

        if predictedClass == example['class']:
            predictionMatrix.append((example['class'], predictedClass, True))
        else:
            predictionMatrix.append((example['class'], predictedClass, False))

    return





