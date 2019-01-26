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

file = open('maze1.txt', 'r')
nodes = []
count = 0
co_ordinate_of_goal = (0,0)
for line in file:
    list = line[0:-1].split(',')
    for index in range(0, len(list)):
        if list[index] != 'G':
            node = Node(f'{count},{index}', index, count, int(list[index]))
        else:
            node = Node(f'{count}:{index}', index, count, 0)
            node.isGoal = True
            co_ordinate_of_goal = (index, count)
        nodes.append(node)
    count += 1

for node in nodes:
    node.distance = math.fabs(co_ordinate_of_goal[0] - node.x) + math.fabs(co_ordinate_of_goal[1] - node.y)
    if node.stepSize > 0:
        if node.x + node.stepSize < count:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x + node.stepSize and item.y == node.y),
                'cost': node.stepSize
            })
        if node.y + node.stepSize < count:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x and item.y == node.y + node.stepSize),
                'cost': node.stepSize
            })
        if node.x - node.stepSize >= 0:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x - node.stepSize and item.y == node.y),
                'cost': node.stepSize
            })
        if node.y - node.stepSize >= 0:
            node.neighbours.append({
                'node': next(item for item in nodes if item.x == node.x and item.y == node.y - node.stepSize),
                'cost': node.stepSize
            })

    # for node in node.neighbours:
    #     print(f'{node["node"].name} {node["cost"]} ', end='')
    # print('')

print('BFS ###########')
queue = []
trail = Trail()
trail.list.append(nodes[0])
queue.append({
    'trail': trail,
    'etd': nodes[0].distance
})

stateExplored = 0

while len(queue) > 0:
    poppedItem = queue.pop(0)
    stateExplored += 1

    if poppedItem['trail'].list[-1].isGoal:
        for t in poppedItem["trail"].list:
            print(f'{t.name}')
        break

    for item in poppedItem['trail'].list[-1].neighbours:
        if item['node'] not in poppedItem['trail'].list:
            newTrail = Trail()
            newTrail.list.extend(poppedItem['trail'].list)
            newTrail.list.append(item['node'])
            newTrail.cost = poppedItem['trail'].cost + item['cost']
            queue.append({
                'trail': newTrail,
                'etd': item['node'].distance
            })
print(f'State Explored: {stateExplored}')

print('DFS ###########')
explored = []
stateExplored = []
path = []
path.append(nodes[0])

def DFS(searchPath):
    peekedItem = searchPath[-1]
    stateExplored.append(0)
    if peekedItem.isGoal:
        for x in searchPath:
            print(f'{x.name}')
        return

    x = [item for item in peekedItem.neighbours if item['node'] not in searchPath and item['node'] not in explored]
    if len(x) > 0:
        searchPath.append(x[0]['node'])
        DFS(searchPath)
    else:
        explored.append(peekedItem)
        searchPath.pop(-1)
        DFS(searchPath)


DFS(path)
print(f'State Explored: {len(stateExplored)}')

print('GFS ###########')
explored = []
stateExplored = []
path = []
path.append(nodes[0])

def GFS(searchPath):
    peekedItem = searchPath[-1]
    stateExplored.append(0)
    if peekedItem.isGoal:
        for x in searchPath:
            print(f'{x.name}')
        return

    x = [item for item in peekedItem.neighbours if item['node'] not in searchPath and item['node'] not in explored]

    for element in x:
        element['etd'] = element['node'].distance

    x = sorted(x, key=lambda k: k['etd'])

    if len(x) > 0:
        searchPath.append(x[0]['node'])
        GFS(searchPath)
    else:
        explored.append(peekedItem)
        searchPath.pop(-1)
        GFS(searchPath)


GFS(path)
print(f'State Explored: {len(stateExplored)}')


print('A* ###########')
explored = []
stateExplored = []
path = []
path.append(nodes[0])

def Astar(searchPath):
    peekedItem = searchPath[-1]
    stateExplored.append(0)
    if peekedItem.isGoal:
        for x in searchPath:
            print(f'{x.name}')
        return

    x = [item for item in peekedItem.neighbours if item['node'] not in searchPath and item['node'] not in explored]

    for element in x:
        element['etd'] = element['node'].distance + element['cost']

    x = sorted(x, key=lambda k: k['etd'])

    if len(x) > 0:
        searchPath.append(x[0]['node'])
        Astar(searchPath)
    else:
        explored.append(peekedItem)
        searchPath.pop(-1)
        Astar(searchPath)


Astar(path)
print(f'State Explored: {len(stateExplored)}')

print('Unique Paths ########')
trail = Trail()
trail.list.append(nodes[0])
stateExplored = []

def trailSearch(trail):
    stateExplored.append(0)
    if len(trail.list[-1].neighbours) == 0:
        print(f'Cost: {trail.cost}, Path: ', end='')
        for item in trail.list[0:-1]:
            print(f'{item.name} ->', end=' ')
        print('G')
        return

    for item in trail.list[-1].neighbours:
        if item['node'] not in trail.list:
            newTrail = Trail()
            newTrail.list.extend(trail.list)
            newTrail.list.append(item['node'])
            newTrail.cost = trail.cost + item['cost']
            trailSearch(newTrail)


trailSearch(trail)
print(f'State Explored: {len(stateExplored)}')


