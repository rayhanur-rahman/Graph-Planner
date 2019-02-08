import Utils, math, random, sys

sys.setrecursionlimit(999999)

# nodes = Utils.processInput('Class_v.txt')
# nodes = Utils.processInput('Map_v.txt')
# nodes = Utils.processInput('Map_u.txt')
# nodes = Utils.processInput('Sudoku_v2.txt')
nodes = Utils.processInput('Sudoku_v.txt')
# nodes = Utils.processInput('Zebra.txt')


Utils.backtrackSearch(nodes)

for node in nodes:
    if node.name == 'Englishman': node.value = 3
    if node.name == 'Spaniard': node.value = 4
    if node.name == 'Ukranian': node.value = 2
    if node.name == 'Norwegian': node.value = 1
    if node.name == 'Japanese': node.value = 5
    if node.name == 'Fox': node.value = 1
    if node.name == 'Dog': node.value = 4
    if node.name == 'Zebra': node.value = 5
    if node.name == 'Snail': node.value = 3
    if node.name == 'Horse': node.value = 2
    if node.name == 'Chesterfields': node.value = 2
    if node.name == 'LuckyStrike': node.value = 4
    if node.name == 'Parliaments': node.value = 5
    if node.name == 'Winstons': node.value = 3
    if node.name == 'Kools': node.value = 1
    if node.name == 'Milk': node.value = 3
    if node.name == 'Coffee': node.value = 5
    if node.name == 'Tea': node.value = 2
    if node.name == 'OrangeJuice': node.value = 4
    if node.name == 'Water': node.value = 1
    if node.name == 'Red': node.value = 3
    if node.name == 'Green': node.value = 5
    if node.name == 'Ivory': node.value = 4
    if node.name == 'Yellow': node.value = 1
    if node.name == 'Blue': node.value = 2

# x = Utils.getNumberOfConflicts(nodes)
# i = 1

# for node in nodes:
#     c = True
#     for arc in node.arcs:
#         nextNode = arc['pair'][1]
#         order = arc['order']
#         if nextNode.value == None:
#             continue
#         if not Utils.isConsistent(node.value, nextNode.value, order):
#             c = False
#         print(f'{c}')