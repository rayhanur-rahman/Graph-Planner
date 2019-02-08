import math, sys

def getHeuristics(Cx, Cy, Gx, Gy, step, max, count):
    # it calculates heuristics
    # Cx, Cy: x,y co ordinate of current position
    # Gx, Gy: x,y co ordinate of goal
    # step: step size at the current position
    # max: maximum step size found in the maze
    # the dimension of the maze

    # heuristic is the sum of step size and minimum of (minimum number of horizontal movements and vertical movements
    # to the goal) of the neighbours
    # minimum number of horizontal/vertical movements can be estimated by the maximum step size in the maze

    options = [] # get list of reachable adjacent neighbours
    if Cx + step < count: options.append((Cx + step, Cy))
    if Cx - step >= 0: options.append((Cx - step, Cy))
    if Cy + step < count: options.append((Cx, Cy + step))
    if Cy - step >= 0: options.append((Cx, Cy - step))

    # find the node from the neighbours who has the minimum of horizontal + vertical movements to goal
    minHop = 1000000

    for option in options:
        hop_x = math.fabs(Gx - option[0]) / max
        hop_y = math.fabs(Gy - option[1]) / max
        if minHop > hop_y + hop_x:
            minHop = hop_x + hop_y

    # add 1 because reaching that node needs one step as well
    return minHop + 1


class Node:

    def __init__(self, name, x, y, stepSize):
        self.name = name
        self.trail = []  # the nodes already visited to reach this node
        self.neighbours = []
        self.distance = 0  # the estimated distance towards goal, will be used as a heuristic for informed such
        self.x = x  # co-ordinates
        self.y = y
        self.isGoal = False
        self.stepSize = stepSize  # the distance from this node to neighbour nodes
        return


# list of nodes explored along a path
class Trail:

    def __init__(self):
        self.list = []  # list of nodes from a to b
        self.cost = 0  # total cost so far from a to b
        return


def processInput(filename):
    # this function will generate graph from the maze input file
    file = open(filename, 'r')
    nodes = []
    count = 0
    maxStepSize = -1
    co_ordinate_of_goal = (0, 0)
    # assigning (x,y) to nodes
    # counting maximum step size
    # determining which node is goal
    for line in file:
        list = line[0:-1].split(',')
        for index in range(0, len(list)):
            if list[index] != 'G':
                if maxStepSize < int(list[index]): maxStepSize = int(list[index])
                node = Node(f'{count},{index}', index, count, int(list[index]))
            else:
                node = Node(f'{count},{index}', index, count, 0)
                node.isGoal = True
                co_ordinate_of_goal = (index, count)
            nodes.append(node)
        count += 1

    # assigning neighbours to each node
    # assigning heuristics to each node
    for node in nodes:
        node.distance = getHeuristics(node.x, node.y, co_ordinate_of_goal[0], co_ordinate_of_goal[1], node.stepSize, maxStepSize, count)
        # print(f'{node.name} {node.stepSize} {node.distance:.2f}:', end=' ')
        if node.stepSize > 0:
            if node.x + node.stepSize < count:
                node.neighbours.append({
                    'node': next(item for item in nodes if item.x == node.x + node.stepSize and item.y == node.y),
                    'cost': 1
                })
            if node.y + node.stepSize < count:
                node.neighbours.append({
                    'node': next(item for item in nodes if item.x == node.x and item.y == node.y + node.stepSize),
                    'cost': 1
                })
            if node.x - node.stepSize >= 0:
                node.neighbours.append({
                    'node': next(item for item in nodes if item.x == node.x - node.stepSize and item.y == node.y),
                    'cost': 1
                })
            if node.y - node.stepSize >= 0:
                node.neighbours.append({
                    'node': next(item for item in nodes if item.x == node.x and item.y == node.y - node.stepSize),
                    'cost': 1
                })

        # for item in node.neighbours:
        #     print(f'{item["node"].name} ', end='')
        # print('')

    return [nodes, filename]


def BFS(nodes, filename):
    file = open(f'{filename}-bfs-solution.txt', 'w')
    print(f'BFS ###########\nSolution is in {filename}-bfs-solution.txt')
    queue = []
    trail = Trail()
    trail.list.append(nodes[0])
    queue.append({
        'trail': trail
    })

    stateExplored = 0

    while len(queue) > 0:
        poppedItem = queue.pop(0)
        stateExplored += 1
        # print(f'Exploring: {poppedItem["trail"].list[-1].name}')

        if poppedItem['trail'].list[-1].isGoal:
            stateExplored -= 1
            for item in poppedItem["trail"].list:
                print(f'({item.name})', end=' ')
                file.write(f'{item.name}\n')
            print('')
            break

        atLeastOneNeighbourFound = False
        for item in poppedItem['trail'].list[-1].neighbours:
            if item['node'] not in poppedItem['trail'].list:
                atLeastOneNeighbourFound = True
                newTrail = Trail()
                newTrail.list.extend(poppedItem['trail'].list)
                newTrail.list.append(item['node'])
                newTrail.cost = poppedItem['trail'].cost + item['cost']
                queue.append({
                    'trail': newTrail                })
        if atLeastOneNeighbourFound == False:
            stateExplored -= 1
    file.write(f'State Explored: {stateExplored}')
    file.close()


def initDFS(nodes, filename):
    print('DFS ###########')
    print(f'Solution is in {filename}-dfs-solution.txt')
    file = open(f'{filename}-dfs-solution.txt', 'w')
    explored = []
    stateExplored = []
    path = []
    path.append(nodes[0])
    DFS(path, explored, stateExplored, file)
    file.write(f'State Explored: {len(stateExplored)}')
    file.close()
    return


def DFS(searchPath, explored, stateExplored, file):
    peekedItem = searchPath[-1]
    stateExplored.append(0)
    # print(f'Exploring: {peekedItem.name}')
    if peekedItem.isGoal:
        stateExplored.pop(0)
        for item in searchPath:
            print(f'({item.name})', end=' ')
            file.write(f'{item.name}\n')
        print('')
        return

    neighbours = [item for item in peekedItem.neighbours if item['node'] not in searchPath and item['node'] not in explored]
    if len(neighbours) > 0:
        searchPath.append(neighbours[0]['node'])
        DFS(searchPath, explored, stateExplored, file)
    else:
        stateExplored.pop(0)
        explored.append(peekedItem)
        searchPath.pop(-1)
        DFS(searchPath, explored, stateExplored, file)


def initGFS(nodes, filename):
    print('Best First Search ###########')
    print(f'Solution is in {filename}-bestfirst-solution.txt')
    file = open(f'{filename}-bestfirst-solution.txt', 'w')
    explored = []
    stateExplored = []
    path = []
    path.append(nodes[0])
    GFS(path, explored, stateExplored, file)
    file.write(f'State Explored: {len(stateExplored)}')
    file.close()
    return

def GFS(searchPath, explored, stateExplored, file):
    peekedItem = searchPath[-1]
    stateExplored.append(0)
    # print(f'Exploring: {peekedItem.name}')
    if peekedItem.isGoal:
        stateExplored.pop(0)
        for item in searchPath:
            print(f'({item.name})', end=' ')
            file.write(f'{item.name}\n')
        print('')
        return

    neighbours = [item for item in peekedItem.neighbours if item['node'] not in searchPath and item['node'] not in explored]

    for element in neighbours:
        element['etd'] = element['node'].distance # being greedy, just select the node which is estimated nearest

    neighbours = sorted(neighbours, key=lambda k: k['etd'])

    if len(neighbours) > 0:
        searchPath.append(neighbours[0]['node'])
        GFS(searchPath, explored, stateExplored, file)
    else:
        stateExplored.pop(0)
        explored.append(peekedItem)
        searchPath.pop(-1)
        GFS(searchPath, explored, stateExplored, file)


def initAStar(nodes, filename):
    print('A* ###########')
    print(f'Solution is in {filename}-astar-solution.txt')
    file = open(f'{filename}-astar-solution.txt', 'w')
    explored = []
    stateExplored = []
    path = []
    path.append(nodes[0])
    Astar(path, explored, stateExplored, file)
    file.write(f'State Explored: {len(stateExplored)}')
    file.close()
    return

def Astar(searchPath, explored, stateExplored, file):
    peekedItem = searchPath[-1]
    stateExplored.append(0)
    # print(f'Exploring: {peekedItem.name}')
    if peekedItem.isGoal:
        stateExplored.pop(0)
        for item in searchPath:
            print(f'({item.name})', end=' ')
            file.write(f'{item.name}\n')
        print('')
        return

    neighbours = [item for item in peekedItem.neighbours if item['node'] not in searchPath and item['node'] not in explored]

    for element in neighbours:
        # applying f(n) = g(n) + h(n)
        element['etd'] = element['cost']+ element['node'].distance

    # sort to find which has the lowest f(n)
    neighbours = sorted(neighbours, key=lambda k: k['etd'])

    if len(neighbours) > 0:
        searchPath.append(neighbours[0]['node'])
        Astar(searchPath, explored, stateExplored, file)
    else:
        stateExplored.pop(0)
        explored.append(peekedItem)
        searchPath.pop(-1)
        Astar(searchPath, explored, stateExplored, file)


def findUniquePaths(nodes, filename):
    print('All Unique Paths ########')
    print(f'Solution is in {filename}-all-paths-solution.txt')
    file = open(f'{filename}-all-paths-solution.txt', 'w')
    trail = Trail()
    trail.list.append(nodes[0])
    stateExplored = []
    trailSearch(trail, stateExplored, file)
    file.write(f'State Explored: {len(stateExplored)}')
    file.close()
    return

def trailSearch(trail, stateExplored, file):
    stateExplored.append(0)
    # print(f'Exploring: {trail.list[-1].name}')
    if trail.list[-1].isGoal:
        stateExplored.pop(0)
        file.write(f'Cost: {trail.cost}, Path: ')
        for item in trail.list[0:-1]:
            file.write(f'({item.name}) => ')
        file.write('G\n')
        return

    atLeastOneNeighbourFound = False
    for item in trail.list[-1].neighbours:
        if item['node'] not in trail.list:
            atLeastOneNeighbourFound = True
            newTrail = Trail()
            newTrail.list.extend(trail.list)
            newTrail.list.append(item['node'])
            newTrail.cost = trail.cost + item['cost']
            trailSearch(newTrail, stateExplored, file)
    if atLeastOneNeighbourFound == False:
        stateExplored.pop(0)

