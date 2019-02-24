import Utils, math, random, sys

sys.setrecursionlimit(10000)

if len(sys.argv) == 3:
    choice = sys.argv[1]
    nodes = Utils.processInput(sys.argv[2])
    count = 20
    file = open('output-{0}-{1}.txt'.format(choice, sys.argv[2][0:-3]), 'w')

if len(sys.argv) == 4:
    choice = sys.argv[1]
    nodes = Utils.processInput(sys.argv[3])
    count = int(sys.argv[2])
    file = open('output-{0}-{1}.txt'.format(choice, sys.argv[3][0:-3]), 'w')

file.write('author: md rayhanur rahman | email: mrahman@ncsu.edu\n')

if choice == 'BACKTRACK': Utils.backtrackSearch(nodes, file)
if choice == 'MINCONFLICTS': Utils.localSearch(nodes, count, file)
