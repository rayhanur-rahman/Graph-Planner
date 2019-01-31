import math, sys, Utils

choice = sys.argv[1]
response = Utils.processInput(sys.argv[2])
#
# choice = 'BFS'
# response = Utils.processInput('maze1.txt')

nodes = response[0]
filename = response[1][0:-4]

if choice == 'BFS': Utils.BFS(nodes, filename)
if choice == 'DFS': Utils.initDFS(nodes, filename)
if choice == 'BestFirst': Utils.initGFS(nodes, filename)
if choice == 'AStar': Utils.initAStar(nodes, filename)
if choice == 'AllPaths': Utils.findUniquePaths(nodes, filename)
