import Utils, Node, sys

if len(sys.argv) == 5:
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
    target = sys.argv[3]
    criteria = sys.argv[4]

    # read all the data from csv
    response = Utils.processInput(trainFile, target)

    root = Node.Node('root')
    root.data = response[0]
    root.unprocessedAttributes = response[1]

    # recursively build the decision tree
    Node.visitTree(root, target, criteria)

    # read the csv file for test
    response = Utils.processInput(testFile, target)

    predictionMatrix = []

    for item in response[0]:
        Node.visiTreeForTest(root, item, predictionMatrix, target)

    outputFileName = 'treeoutput.txt'
    open(outputFileName, 'w').close()
    Node.printTree(root, 0, outputFileName)

    # calculate performance of the learning
    performance = Utils.calculatePerformance(predictionMatrix)
    print(performance)

else:
    print('Invalid input format. Please have a look at the readme file.')


