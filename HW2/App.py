import Utils, math, random, sys

print(f'author: md rayhanur rahman | email: mrahman@ncsu.edu\n')

sys.setrecursionlimit(10000)

# nodes = Utils.processInput('Class_v.txt')
# nodes = Utils.processInput('Map_v.txt')
# nodes = Utils.processInput('Map_u.txt')
# nodes = Utils.processInput('Sudoku_v2.txt')
# nodes = Utils.processInput('Sudoku_v.txt')
# nodes = Utils.processInput('Zebra.txt')


# Utils.localSearch(nodes)
# Utils.backtrackSearch(nodes)


choice = sys.argv[1]
nodes = Utils.processInput(sys.argv[2])

if choice == 'bs': Utils.backtrackSearch(nodes)
if choice == 'ls': Utils.localSearch(nodes)

