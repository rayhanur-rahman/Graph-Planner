class Node:

    def __init__(self, name, distance):
        self.name = name
        self.trail = []
        self.neighbours = []
        self.distance = distance
        return

class Trail:

    def __init__(self):
        self.list = []
        self.cost = 0
        return

a = Node('a', 4)
b = Node('b', 3)
c = Node('c', 2)
d = Node('d', 3)
e = Node('e', 2)
f = Node('f', 1)
g = Node('g', 2)
h = Node('h', 1)
i = Node('i', 0)

# a.neighbours.append({
#     'node': b,
#     'cost': 1
# })
# b.neighbours.append({
#     'node': c,
#     'cost': 1
# })
# c.neighbours.append({
#     'node': d,
#     'cost': 1
# })
# c.neighbours.append({
#     'node': e,
#     'cost': 1
# })
# b.neighbours.append({
#     'node': f,
#     'cost': 1
# })
#


a.neighbours.append({
    'node': b,
    'cost': 1
})
a.neighbours.append({
    'node': d,
    'cost': 1
})

b.neighbours.append({
    'node': a,
    'cost': 1
})
b.neighbours.append({
    'node': e,
    'cost': 1
})
b.neighbours.append({
    'node': c,
    'cost': 1
})

c.neighbours.append({
    'node': b,
    'cost': 1
})
c.neighbours.append({
    'node': f,
    'cost': 1
})


d.neighbours.append({
    'node': a,
    'cost': 1
})
d.neighbours.append({
    'node': e,
    'cost': 1
})
d.neighbours.append({
    'node': g,
    'cost': 1
})

e.neighbours.append({
    'node': b,
    'cost': 1
})
e.neighbours.append({
    'node': d,
    'cost': 1
})
e.neighbours.append({
    'node': f,
    'cost': 1
})
e.neighbours.append({
    'node': h,
    'cost': 1
})

f.neighbours.append({
    'node': c,
    'cost': 1
})
f.neighbours.append({
    'node': e,
    'cost': 1
})
f.neighbours.append({
    'node': i,
    'cost': 1
})

g.neighbours.append({
    'node': d,
    'cost': 1
})
g.neighbours.append({
    'node': h,
    'cost': 1
})

h.neighbours.append({
    'node': g,
    'cost': 1
})
h.neighbours.append({
    'node': e,
    'cost': 1
})
h.neighbours.append({
    'node': i,
    'cost': 1
    })

queue = []
trail = Trail()
trail.list.append(a)
queue.append(trail)

while len(queue) > 0:
    poppedItem = queue.pop(0)

    for item in poppedItem.list[-1].neighbours:
        if item['node'] not in poppedItem.list:
            newTrail = Trail()
            newTrail.list.extend(poppedItem.list)
            newTrail.list.append(item['node'])
            newTrail.cost = poppedItem.cost + item['cost']
            queue.append(newTrail)
            if newTrail.list[-1].name == 'i':
                print(f'{newTrail.cost}: ', end="")
                for t in newTrail.list:
                    print(f'{t.name} =>', end=' ')
                print(' ')

print('BFS ###########')
trail = Trail()
trail.list.append(a)

def trailSearch(trail):
    if len(trail.list[-1].neighbours) == 0:
        print(f'{trail.cost}: ', end='')
        for item in trail.list:
            print(f'{item.name} =>', end=' ')
        print('')
        return

    for item in trail.list[-1].neighbours:
        if item['node'] not in trail.list:
            newTrail = Trail()
            newTrail.list.extend(trail.list)
            newTrail.list.append(item['node'])
            newTrail.cost = trail.cost + item['cost']
            trailSearch(newTrail)


trailSearch(trail)

print('DFS ###########')
trail = Trail()
trail.list.append(a)

def greedySearch(trail):
    if len(trail.list[-1].neighbours) == 0:
        print(f'{trail.cost}: ', end='')
        for item in trail.list:
            print(f'{item.name} =>', end=' ')
        print('')
        return

    minNode = None
    minCost = 100
    actualCost = 0
    for item in trail.list[-1].neighbours:
        if item['node'] not in trail.list:
            if item['node'].distance < minCost:
                minNode = item['node']
                minCost = item['node'].distance
                actualCost = item['cost']

    if minNode != None:
        newTrail = Trail()
        newTrail.list.extend(trail.list)
        newTrail.list.append(minNode)
        newTrail.cost = trail.cost + actualCost
        greedySearch(newTrail)


greedySearch(trail)

print('Greedy ###########')
trail = Trail()
trail.list.append(a)

def astar(trail):
    if len(trail.list[-1].neighbours) == 0:
        print(f'{trail.cost}: ', end='')
        for item in trail.list:
            print(f'{item.name} =>', end=' ')
        print('')
        return

    minNode = None
    minCost = 100
    actualCost = 0
    for item in trail.list[-1].neighbours:
        if item['node'] not in trail.list:
            if item['node'].distance + item['cost'] < minCost:
                minNode = item['node']
                minCost = item['node'].distance + item['cost']
                actualCost = item['cost']

    if minNode != None:
        newTrail = Trail()
        newTrail.list.extend(trail.list)
        newTrail.list.append(minNode)
        newTrail.cost = trail.cost + actualCost
        astar(newTrail)


astar(trail)
















