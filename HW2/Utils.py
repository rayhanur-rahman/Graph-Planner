import random, math


class Node:

    def __init__(self, name):
        self.name = name
        self.arcs = []
        self.domains = []
        self.domainConstraint = []
        self.explored = []
        self.value = None
        return


def processInput(file):
    file = open(file, 'r')
    vars = []
    varInput = False
    constraintsInput = False
    for line in file:
        line = line.strip()
        if line == 'VARS':
            varInput = True
            continue
        if line == 'ENDVARS':
            varInput = False
            continue
        if line == 'CONSTRAINTS':
            constraintsInput = True
            continue
        if line == 'ENDCONSTRAINTS':
            constraintsInput = False
            continue

        if varInput:
            tokens = line.split(' ')
            # print(tokens)
            node = Node(tokens[0])
            for token in tokens[2:]:
                node.domains.append(int(token))
            # node.domains.extend(tokens[2:])
            vars.append(node)
        if constraintsInput:
            if line[0:7] == 'Alldiff':
                sentence = line[8:-1].replace(' ', '')
                tokens = sentence.split(',')
                tokens.insert(0, '!=')
                nodes = []
                for index in range(1, len(tokens)):
                    node = next(node for node in vars if node.name == tokens[index])
                    nodes.append(node)

                for index_i in range(0, len(nodes)):
                    for index_j in range(0, len(nodes)):
                        if index_i != index_j:
                            nodes[index_i].arcs.append({
                                'pair': (nodes[index_i], nodes[index_j]),
                                'order': tokens[0]
                            })
            else:
                tokens = line.split(' ')
                # print(tokens)
                nodes = []
                constantFound = False
                constant = None
                directionalOperators = ['>1']
                reversedirectionalOperators = ['<1']
                for index in range(1, len(tokens)):
                    nodeList = [node for node in vars if node.name == tokens[index]]
                    if len(nodeList) > 0:
                        nodes.append(nodeList[0])
                    else:
                        constantFound = True
                        constant = int(tokens[index])

                if not constantFound:
                    for index_i in range(0, len(nodes)):
                        for index_j in range(0, len(nodes)):
                            if index_i != index_j:
                                if tokens[0] not in directionalOperators:
                                    nodes[index_i].arcs.append({
                                        'pair': (nodes[index_i], nodes[index_j]),
                                        'order': tokens[0]
                                    })
                                else:
                                    operatorIndex = directionalOperators.index(tokens[0])
                                    if index_i < index_j:
                                        nodes[index_i].arcs.append({
                                            'pair': (nodes[index_i], nodes[index_j]),
                                            'order': tokens[0]
                                        })
                                    if index_i > index_j:
                                        nodes[index_i].arcs.append({
                                            'pair': (nodes[index_i], nodes[index_j]),
                                            'order': reversedirectionalOperators[operatorIndex]
                                        })
                else:
                    for node in nodes:
                        node.domainConstraint.append({
                            'order': tokens[0],
                            'value': constant
                        })

    file.close()
    return vars


def applyDomainConstraints(nodes):
    for node in nodes:
        if len(node.domainConstraint) > 0:
            for constraint in node.domainConstraint:
                if constraint['order'] == '=':
                    node.value = constraint['value']
                    node.domains = []
                    node.domains.append(node.value)


def isConsistent(x, y, order):
    if order == '!=': return x != y
    if order == '=': return x == y
    if order == '>1': return x == y + 1
    if order == '<1': return x == y - 1
    if order == '<>1': return math.fabs(x - y) == 1


def revise(arc):
    revised = False
    node1 = arc['pair'][0]
    node2 = arc['pair'][1]
    order = arc['order']
    consistentValueFound = 0
    toBeRemoved = []
    for ix in node1.domains:
        for iy in node2.domains:
            if isConsistent(ix, iy, order): consistentValueFound += 1
        if consistentValueFound == 0:
            toBeRemoved.append(ix)
            revised = True
        consistentValueFound = 0
    for item in toBeRemoved:
        node1.domains.remove(item)
    return revised


def ac3(nodes):
    queue = []

    for node in nodes:
        for arc in node.arcs:
            queue.append(arc)

    while len(queue) > 0:
        arc = queue.pop(0)
        node1 = arc['pair'][0]
        node2 = arc['pair'][1]

        if revise(arc):
            if len(node1.domains) == 0:
                print('False')
                continue
            for arc in node1.arcs:
                if arc['pair'][1] != node2:
                    queue.append(arc)


def filterSingleDomainNodes(nodes):
    newNodes = []

    for node in nodes:
        if len(node.domains) == 1:
            node.value = node.domains[0]
        else:
            newNodes.append(node)
    return nodes, newNodes


def backtrack(stack, nodes, size, steps):
    if len(stack) == size:
        return

    if len(stack) <= size:
        if len(nodes) > 0:
            node = nodes[0]
        else:
            return

        if len(node.domains) > 0:
            node.value = node.domains.pop(0)
            node.explored.append(node.value)
        else:
            node.domains.extend(node.explored)
            node.explored = []
            node.value = None
            nodes.insert(0, stack.pop(-1))
            if len(stack) <= size:
                steps.append(0)
                backtrack(stack, nodes, size, steps)

        neighboursConsistent = True
        for arc in node.arcs:
            nextNode = arc['pair'][1]
            order = arc['order']
            if nextNode.value == None:
                continue
            if not isConsistent(node.value, nextNode.value, order):
                neighboursConsistent = False

        if neighboursConsistent:
            stack.append(node)
            if len(nodes) > 0: nodes.pop(0)
        else:
            node.value = None

        if len(stack) <= size:
            #steps.append(0)
            backtrack(stack, nodes, size, steps)


def backtrackSearch(nodes):
    applyDomainConstraints(nodes)
    ac3(nodes)
    stack = []
    response = filterSingleDomainNodes(nodes)
    newNodes = response[1]
    newNodes = sorted(newNodes, key=lambda k: len(k.domains), reverse=False)
    size = len(newNodes)
    steps = []
    steps.append(0)
    backtrack(stack, newNodes, size, steps)
    for node in nodes:
        print(f'{node.name}:{node.value}|', end='')
    print('')
    print(f'number of steps: {len(steps)}')
    return nodes


def getNumberOfConflicts(nodes):
    arcs = []
    for node in nodes:
        arcs.extend(node.arcs)

    numberOfConflicts = 0
    conflictedArcs = []
    for arc in arcs:
        node1 = arc['pair'][0]
        node2 = arc['pair'][1]
        order = arc['order']

        x = node1.value
        y = node2.value

        if x is not None and y is not None:
            if not isConsistent(x, y, order):
                numberOfConflicts += 1
                conflictedArcs.append(arc)
        else:
            continue
    return [numberOfConflicts, conflictedArcs]


def localSearch(nodes):
    applyDomainConstraints(nodes)
    ac3(nodes)
    filteredNodes = filterSingleDomainNodes(nodes)[1]

    seed = random.randint(0, 99999)
    random.seed(seed)
    print(f'RPG seed is set to {seed}. The possibility to get to the solution depends on the seed for some problems.')
    print(f'If you have not got to the solution, run it again a few times.')
    for node in nodes:
        node.value = node.domains[random.randint(0, len(node.domains) - 1)]

    isSolutionFound = False
    for index in range(0, 20):
        if isSolutionFound: break
        response = getNumberOfConflicts(nodes)
        conflictCount = response[0]
        conflictedArcs = response[1]
        if conflictCount == 0:
            print(f'success after {index} tries')
            isSolutionFound = True
        else:
            if conflictCount < 20:
                x = 1
            # print(f'searching locally: {conflictCount}')
            node = None
            while (True):
                arc = conflictedArcs[random.randint(0, len(conflictedArcs) - 1)]
                node = arc['pair'][0]
                if node in filteredNodes:
                    break
                else:
                    continue

            conflictMatrix = [500000] * len(node.domains)
            min = 10000
            minIndex = None
            for index in range(0, len(node.domains)):
                node.value = node.domains[index]
                conflictMatrix[index] = getNumberOfConflicts(nodes)[0]
                newConflictedArcs = getNumberOfConflicts(nodes)[1]
                if conflictMatrix[index] < min:
                    min = conflictMatrix[index]
                    minIndex = index

            node.value = node.domains[minIndex]

    if isSolutionFound:
        for node in nodes:
            print(f'{node.name}:{node.value}|', end='')
        print('')
    else:
        print(f'no solution found, found {conflictCount} conflicts')
        for arc in newConflictedArcs:
            print(f'({arc["pair"][0].name}, {arc["pair"][1].name})|', end='')
    return nodes
