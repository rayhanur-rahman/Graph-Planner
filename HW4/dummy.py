from itertools import combinations, chain

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class Node:
    def __init__(self, name):
        self.name = name
        self.mutex = []
        self.goals = []
        return


def checkMutexInSet(list):
    for item1 in list:
        for item2 in list:
            if checkMutex(item1, item2): return True
    return False

def checkForGoals(list, goals):
    numberOfGoalsAchieved = 0
    for item in goals:
        for elem in list:
            if item in elem.goals: numberOfGoalsAchieved += 1
    if numberOfGoalsAchieved == len(goals): return True
    else: return False

def checkMutex(elem1, elem2):
    if elem1 == elem2: return False
    if elem1 in elem2.mutex or elem2 in elem1.mutex: return True
    else: return False

noh = Node('no-op@-hungry')
nod = Node('no-op@-dinner')
nocl = Node('no-op@clean')
eat = Node('eat')
clean = Node('clean')

nocl.mutex.extend([noh, nod, eat, clean])
nocl.goals.extend(['c'])
noh.mutex.extend([[eat]])
noh.goals.extend(['h'])
nod.mutex.extend([eat])
nod.goals.extend(['d'])
eat.mutex.extend([clean, nocl, nod, noh])
eat.goals.extend(['d', 'h'])
clean.mutex.extend([nocl])
clean.goals.extend(['c'])

set = powerset([noh, nod, nocl, eat, clean])

for item in set:
    if not checkMutexInSet(item):
        if checkForGoals(item, goals=['d', 'h', 'c']):
            for elem in item:
                print(elem.name)


