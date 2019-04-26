import Utils, Node

# response = Utils.processInput('Mushroom_train.csv')
response = Utils.processInput('SpectHeart_train.csv')
# response = Utils.processInput('w.csv')



root = Node.Node('root')
root.data = response[0]
root.unprocessedAttributes = response[1][0:-1]
Node.visitTree(root)

# response = Utils.processInput('Mushroom_test.csv')
response = Utils.processInput('SpectHeart_test.csv')
# response = Utils.processInput('wtest.csv')


testData = response[0]

predictionMatrix = []
for item in testData:
    Node.visiTreeForTest(root, item, predictionMatrix)

x = Utils.calCulateFMeasure(predictionMatrix)
print(x)