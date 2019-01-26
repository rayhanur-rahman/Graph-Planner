import math

class Node:

    def __init__(self, name, x, y, stepSize):
        self.name = name
        self.trail = []
        self.neighbours = []
        self.distance = 0
        self.x = x
        self.y = y
        self.isGoal = False
        self.stepSize = stepSize
        return

class Trail:

    def __init__(self):
        self.list = []
        self.cost = 0
        return

file = open('maze6.txt', 'r')
nodes = []
count = 0
co_ordinate_of_goal = (0,0)
for line in file:
    list = line[0:-1].split(',')
    for index in range(0, len(list)):
        if list[index] != 'G':
            node = Node(f'{count}-{index}', index, count, int(list[index]))
        if list[index] == 'G':
            node = Node(f'{count}-{index}', index, count, 0)
            node.isGoal = True
            co_ordinate_of_goal = (index, count)
        nodes.append(node)
    count += 1

for node in nodes:
    node.distance = math.pow(co_ordinate_of_goal[0] - node.x, 2) + math.pow(co_ordinate_of_goal[1] - node.y, 2)
    node.distance = math.sqrt(node.distance)
    print(f'{node.name} {node.stepSize} {node.distance:.2f}:', end=' ')
    if node.stepSize > 0:
        if node.x + node.stepSize < count:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x + node.stepSize and item.y == node.y),
                'cost': node.stepSize
            })
        if node.x - node.stepSize >= 0:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x - node.stepSize and item.y == node.y),
                'cost': node.stepSize
            })
        if node.y + node.stepSize < count:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x and item.y == node.y + node.stepSize),
                'cost': node.stepSize
            })
        if node.y - node.stepSize >= 0:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x and item.y == node.y - node.stepSize),
                'cost': node.stepSize
            })

    for node in node.neighbours:
        print(f'{node["node"].name} {node["cost"]} ', end='')
    print('')

trail = Trail()
trail.list.append(nodes[0])

def astar(trail):
    if len(trail.list[-1].neighbours) == 0:
        if trail.list[-1].isGoal == True:
            print(f'{trail.cost}: ', end='')
            for item in trail.list:
                print(f'{item.name} =>', end=' ')
            print('')
            return

    options = []

    for item in trail.list[-1].neighbours:
        if item['node'] not in trail.list:
            options.append({
                'node': item['node'],
                'cost': item['cost'],
                'etd': item['node'].distance + item['cost']
            })

    options = sorted(options, key=lambda k: k['etd'])

    for item in options:
        newTrail = Trail()
        newTrail.list.extend(trail.list)
        newTrail.list.append(item['node'])
        newTrail.cost = trail.cost + item['cost']
        astar(newTrail)

astar(trail)

