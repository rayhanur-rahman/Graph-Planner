from itertools import combinations, chain
import sys

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class State:
    def __init__(self, name, truth_value):
        self.name = name
        self.truth_value = truth_value
        return

class Action:
    def __init__(self, name):
        self.name = name
        self.req = []
        self.effect = []
        return

class Node:
    def __init__(self, index, type, name):
        self.index = index
        self.type = type
        self.name = name
        self.truth_value = None
        self.children = []
        self.mutex = []

def process_input(file_name):

    states = []
    actions = []
    init = []
    goal = []

    file = open(file_name, 'r')

    current_action = None

    for line in file:
        if line.startswith('INIT') or line.startswith('GOAL'):
            parsed_states = line[5:].strip().split(',')
            for item in parsed_states:
                state = State(item[1:], item[0])
                if not any(x.name == state.name and x.truth_value == state.truth_value for x in states):
                    states.append(state)

                if line.startswith('INIT'): init.append(state)
                if line.startswith('GOAL'): goal.append(state)

        if line.startswith('ACTION'):
            parsed_action = line[7:].strip()
            action = Action(parsed_action)
            current_action = action
            actions.append(action)

        if line.startswith('PRECOND') or line.startswith('EFFECT'):
            parsed_states = None
            if line.startswith('PRECOND'): parsed_states = line[8:].strip().split(',')
            if line.startswith('EFFECT'): parsed_states = line[7:].strip().split(',')

            for item in parsed_states:
                if len(item) > 0:
                    state = State(item[1:], item[0])
                    if not any(x.name == state.name and x.truth_value == state.truth_value for x in states):
                        states.append(state)

                    if line.startswith('PRECOND'):
                        current_action.req.append(state)
                    if line.startswith('EFFECT'):
                        current_action.effect.append(state)

    return init, goal, states, actions

# get the states which are precondition of an action
def check_for_req(action, planning_graph, index):
    if len(action.req) == 0: return True
    states_in_given_layer = [x for x in planning_graph if x.index == index and x.type == 'state']
    for item in action.req:
        if not any(x.name == item.name and x.truth_value == item.truth_value for x in states_in_given_layer):
            return False
    return True

def is_actions_mutex(action1, action2):
    is_mutex = False
    if action1 == action2: return is_mutex

    action1_effects = [x for x in action1.children if x.type == 'state' and x.index == action1.index+1]
    action1_causes = [x for x in action1.children if x.type == 'state' and x.index == action1.index]
    action2_effects = [x for x in action2.children if x.type == 'state' and x.index == action2.index + 1]
    action2_causes = [x for x in action2.children if x.type == 'state' and x.index == action2.index]

    # inconsistent effect: see the CSC520 Lecture 17
    if len(action2_effects) > 0 and len(action1_effects) > 0:
        for elem1 in action1_effects:
            for elem2 in action2_effects:
                if elem1.name == elem2.name and elem1.truth_value != elem2.truth_value:
                    is_mutex = True
                    return is_mutex
    # competing nodes
    if len(action2_causes) > 0 and len(action1_causes) > 0:
        for elem1 in action1_causes:
            for elem2 in action2_causes:
                if elem1 in elem2.mutex or elem2 in elem1.mutex:
                    is_mutex = True
                    return is_mutex
    # interference
    if len(action2_causes) > 0 and len(action1_effects) > 0:
        for elem1 in action1_effects:
            for elem2 in action2_causes:
                if elem1.name == elem2.name and elem1.truth_value != elem2.truth_value:
                    is_mutex = True
                    return is_mutex

    # interference
    if len(action2_effects) > 0 and len(action1_causes) > 0:
        for elem1 in action1_causes:
            for elem2 in action2_effects:
                if elem1.name == elem2.name and elem1.truth_value != elem2.truth_value:
                    is_mutex = True
                    return is_mutex

    return is_mutex

def is_states_mutex(state1, state2):
    is_mutex = False
    # negated literlas
    if state1.name == state2.name and state1.truth_value != state2.truth_value:
        is_mutex = True
        return is_mutex

    state1_causes = [x for x in state1.children if x.type == 'action' and x.index == state1.index - 1 and state1.index > 0]
    state2_causes = [x for x in state2.children if x.type == 'action' and x.index == state2.index - 1 and state2.index > 0]

    # inconsistent support
    if len(state2_causes) > 0 and len(state1_causes) > 0:
        for elem1 in state1_causes:
            for elem2 in state2_causes:
                if elem1 != elem2 or 1==1:
                    if not is_actions_mutex(elem1, elem2):
                        return False
                    else:
                        is_mutex = True

    return is_mutex

# check if all goal states are not mutex in current layer
def is_goal_reached(goal, planning_graph, index):
    number_of_goal_state_mutex_found = 0
    number_of_goal_state_found = 0
    for item in goal:
        if any(x.name == item.name and x.type == 'state' and x.index == index and x.truth_value == item.truth_value \
               for x in planning_graph):
            number_of_goal_state_found += 1
            goal_state = next(x for x in planning_graph if x.name == item.name and x.type == 'state' and x.index == index and x.truth_value == item.truth_value)
            for element in goal:
                next_goal_state = [x for x in planning_graph if
                                  x.name == element.name and x.type == 'state' and x.index == index and x.truth_value == element.truth_value]
                if len(next_goal_state) > 0:
                    if next_goal_state[0] in goal_state.mutex:
                        number_of_goal_state_mutex_found += 1
                        break

    if number_of_goal_state_mutex_found == 0 and number_of_goal_state_found == len(goal):
        return True
    else:
        return False

# get only the states that are goal nodes, discard other states
def extract_goals(goal, planning_graph, index):
    goal_states = []
    if is_goal_reached(goal, planning_graph, index):
        for item in goal:
            if any(x.name == item.name and x.type == 'state' and x.index == index and x.truth_value == item.truth_value \
                   for x in planning_graph):
                goal_state = next(x for x in planning_graph if
                                  x.name == item.name and x.type == 'state' and x.index == index and x.truth_value == item.truth_value)
                goal_states.append(goal_state)
    return goal_states

# find if there is at least one mutex in a set of actions
def check_mutex_in_set(list_of_actions):
    for item1 in list_of_actions:
        for item2 in list_of_actions:
            if is_action_pair_mutex(item1, item2):
                return True
    return False

# check of actions generate goal states in the next layer
def check_if_actions_meets_goals(actions, goals):
    for goal in goals:
        goal_found = False
        for action in actions:
            if any(x.name == goal.name and x.truth_value == goal.truth_value and x.index \
                   == action.index + 1 and x.type == 'state' for x in action.children):
                goal_found = True
        if not goal_found: return False

    return True

def is_action_pair_mutex(elem1, elem2):
    if elem1 == elem2:
        return False
    if elem1 in elem2.mutex or elem2 in elem1.mutex:
        return True
    else:
        return False

# a recursive backward search from goal nodes to init nodes. if successful, then returns true
def backward_search(init, goal, limit):
    goal_states = goal
    reverse_planning_graph = []

    for item in goal_states:
        reverse_planning_graph.append(item)

    states_in_current_layer = [x for x in reverse_planning_graph if
                               x.index == limit and x.type == 'state']
    actions_in_prior_layer = []
    for state in states_in_current_layer:
        causes = [x for x in state.children if x.type == 'action' and x.index == state.index - 1]
        for cause in causes:
            if cause not in actions_in_prior_layer:
                actions_in_prior_layer.append(cause)

    solution_found = 0
    options_actions = []
    options_states = []
    powerset_of_actions = powerset(actions_in_prior_layer)
    for actions in powerset_of_actions:
        if len(actions) > 0:
            if not check_mutex_in_set(actions):
                if check_if_actions_meets_goals(actions, goal_states):
                    solution_found += 1
                    options_actions.append(actions)
                    states_in_prior_layer = []
                    for action in actions:
                        causes = [x for x in action.children if
                                  x.type == 'state' and x.index == action.index]
                        for cause in causes:
                            if cause not in actions_in_prior_layer:
                                states_in_prior_layer.append(cause)
                    options_states.append(states_in_prior_layer)


    if solution_found > 0:
        for i in range(0, solution_found):
            reverse_planning_graph.extend(options_actions[i])
            reverse_planning_graph.extend(options_states[i])
            goal_states = [x for x in reverse_planning_graph if
                           x.type == 'state' and x.index == limit - 1]

            count = 0
            for item in init:
                init_found = False
                for goal in goal_states:
                    if (item.name == goal.name and item.truth_value == goal.truth_value):
                        init_found = True
                if init_found:
                    count += 1

            if count == len(init) and limit == 1:
                return True
            else:
                if limit > 1:
                    return backward_search(init, goal_states, limit - 1)
                else:
                    continue
    else:
        return False

# similar to backward_search, it just saves the relevant actions and states
def generate_reverse_planning_graph(init, goal, planning_graph, limit, init_states, init_actions):
    goal_states = extract_goals(goal, planning_graph, limit)
    reverse_planning_graph = []

    for item in goal_states:
        reverse_planning_graph.append(item)

    init_entered = False
    for reverese_index in range(limit, 0, -1):
        if len(init_states) > 0 and len(init_actions) > 0 and not init_entered:
            reverse_planning_graph.extend(init_states)
            reverse_planning_graph.extend(init_actions)
            goal_states = [x for x in reverse_planning_graph if
                           x.type == 'state' and x.index == reverese_index - 1]
            init_entered = True
            continue

        states_in_current_layer = [x for x in reverse_planning_graph if
                                   x.index == reverese_index and x.type == 'state']
        actions_in_prior_layer = []
        for state in states_in_current_layer:
            causes = [x for x in state.children if x.type == 'action' and x.index == state.index - 1]
            for cause in causes:
                if cause not in actions_in_prior_layer:
                    actions_in_prior_layer.append(cause)

        solution_found = 0
        powerset_of_actions = powerset(actions_in_prior_layer)
        for actions in powerset_of_actions:
            if len(actions) > 0:
                if not check_mutex_in_set(actions):
                    if check_if_actions_meets_goals(actions, goal_states):
                        solution_found += 1
                        reverse_planning_graph.extend(actions)
                        states_in_prior_layer = []
                        for action in actions:
                            causes = [x for x in action.children if
                                      x.type == 'state' and x.index == action.index]
                            for cause in causes:
                                if cause not in actions_in_prior_layer:
                                    states_in_prior_layer.append(cause)
                        reverse_planning_graph.extend(states_in_prior_layer)
                        break

        if solution_found > 0:
            goal_states = [x for x in reverse_planning_graph if
                           x.type == 'state' and x.index == reverese_index - 1]

            count = 0
            for item in init:
                init_found = False
                for goal in goal_states:
                    if (item.name == goal.name and item.truth_value == goal.truth_value):
                        init_found = True
                if init_found:
                    count += 1

            if count == len(init) and reverese_index == 1:
                return [True, reverse_planning_graph]
            else:
                continue
        else:
            return [False, reverse_planning_graph]

# from the goal nodes, first we need to select a subset of actions which are non mutex and can
# lead to the init states. This method will try each possible subset in the penultimate layer and
# then try to reach the init. If success it returns true and returns the set of action through
# which we managed to get to the init state via backward search
def extract_solution(init, goal, planning_graph, limit):
    goal_states = extract_goals(goal, planning_graph, limit)
    reverse_planning_graph = []

    for item in goal_states:
        reverse_planning_graph.append(item)

    states_in_current_layer = [x for x in reverse_planning_graph if
                               x.index == limit and x.type == 'state']
    actions_in_prior_layer = []
    for state in states_in_current_layer:
        causes = [x for x in state.children if x.type == 'action' and x.index == state.index - 1]
        for cause in causes:
            if cause not in actions_in_prior_layer:
                actions_in_prior_layer.append(cause)

    solution_found = 0
    options_actions = []
    options_states = []
    powerset_of_actions = powerset(actions_in_prior_layer)
    for actions in powerset_of_actions:
        if len(actions) > 0:
            if not check_mutex_in_set(actions):
                if check_if_actions_meets_goals(actions, goal_states):
                    solution_found += 1
                    options_actions.append(actions)
                    states_in_prior_layer = []
                    for action in actions:
                        causes = [x for x in action.children if
                                  x.type == 'state' and x.index == action.index]
                        for cause in causes:
                            if cause not in actions_in_prior_layer:
                                states_in_prior_layer.append(cause)
                    options_states.append(states_in_prior_layer)

    found = False
    if solution_found > 0:
        for i in range(0, solution_found):
            reverse_planning_graph.extend(options_actions[i])
            reverse_planning_graph.extend(options_states[i])
            goal_states = [x for x in reverse_planning_graph if
                           x.type == 'state' and x.index == limit - 1]
            if backward_search(init, goal_states, limit - 1):
                return [True, options_states[i], options_actions[i]]
            else:
                for item in options_actions[i]: reverse_planning_graph.remove(item)
                for item in options_states[i]: reverse_planning_graph.remove(item)

    if not found:
        return [False, [], []]

# the overall graph-plan algorithm
def generate_planner(init, goal, actions):
    MAX_DEPTH = sys.maxsize
    planning_graph = []

    # create nodes from the init states
    for item in init:
        node = Node(0, 'state', item.name)
        node.truth_value = item.truth_value
        planning_graph.append(node)

    # it is basically an infinite loop, will termiate if goal is found or no-good is reached
    limit = None
    reverse_planning_graph = None
    for index in range(0,MAX_DEPTH):
        # generate states in current layer
        states_in_current_layer = [x for x in planning_graph if x.index == index and x.type == 'state']

        # generate persistent actions in the next layer, the name of those layers
        # starts with no-op with layer index
        for item in states_in_current_layer:
            state_node = Node(index+1, 'state', item.name)
            state_node.truth_value = item.truth_value
            planning_graph.append(state_node)

            action_node = Node(index, 'action', 'no-op-{0}@{1}{2}'.format(index, item.truth_value, item.name))
            state_node.children.append(action_node)
            action_node.children.append(state_node)
            item.children.append(action_node)
            action_node.children.append(item)
            planning_graph.append(action_node)

        # generate actions in the next layer
        # those actions must satisfy the preconditions in the current layer
        for item in actions:
           if check_for_req(item, planning_graph, index):
               node = Node(index, 'action', item.name)

               for req in item.req:
                   req_state = [x for x in planning_graph if
                                x.index == index and x.type == 'state' and x.name == req.name and x.truth_value == req.truth_value][0]
                   req_state.children.append(node)
                   node.children.append(req_state)

               for effect in item.effect:
                   effect_states = [x for x in planning_graph if
                                   x.index == index+1 and x.type == 'state' and x.name == effect.name and x.truth_value == effect.truth_value]
                   if len(effect_states) > 0:
                       effect_states[0].children.append(node)
                       node.children.append(effect_states[0])
                   else:
                       state_node = Node(index+1, 'state', effect.name)
                       state_node.truth_value = effect.truth_value
                       node.children.append(state_node)
                       state_node.children.append(node)
                       planning_graph.append(state_node)

               planning_graph.append(node)

        # generate states and actions of prior, current and next layers
        actions_in_current_layer = [x for x in planning_graph if x.index == index and x.type == 'action']
        states_in_prior_layer = [x for x in planning_graph if x.index == index - 1 and x.type == 'state']
        actions_in_prior_layer = [x for x in planning_graph if x.index == index - 1 and x.type == 'action']
        states_in_next_layer = [x for x in planning_graph if x.index == index + 1 and x.type == 'state']

        # calculate mutex between states and actions
        for item1 in states_in_current_layer:
            for item2 in states_in_current_layer:
                if item1 != item2:
                    if is_states_mutex(item1, item2):
                        if item2 not in item1.mutex: item1.mutex.append(item2)
                        if item1 not in item2.mutex: item2.mutex.append(item1)

        for item1 in actions_in_current_layer:
            for item2 in actions_in_current_layer:
                if item1 != item2:
                    if is_actions_mutex(item1, item2):
                        if item2 not in item1.mutex: item1.mutex.append(item2)
                        if item1 not in item2.mutex: item2.mutex.append(item1)

        for item1 in states_in_next_layer:
            for item2 in states_in_next_layer:
                if item1 != item2:
                    if is_states_mutex(item1, item2):
                        if item2 not in item1.mutex: item1.mutex.append(item2)
                        if item1 not in item2.mutex: item2.mutex.append(item1)

        # keep record of the mutex counts and current and prior layers
        mutex_count_current_layer = 0
        mutex_count_prior_layer = 0
        for item in states_in_prior_layer:
            mutex_count_prior_layer += len(item.mutex)
        for item in actions_in_prior_layer:
            mutex_count_prior_layer += len(item.mutex)
        for item in states_in_current_layer:
            mutex_count_current_layer += len(item.mutex)
        for item in actions_in_current_layer:
            mutex_count_current_layer += len(item.mutex)

        # goal test
        if is_goal_reached(goal, planning_graph, index):
            limit = index
            # if by doing a recursive backward search, init state can be reached that means we have
            # got a plan
            response = extract_solution(init, goal, planning_graph, limit)
            if response[0]:
                # generate the reverse planning graph where only relevant actions and states will
                # be kept
                reverse_planning_graph = generate_reverse_planning_graph(init, goal, planning_graph, limit, response[1], response[2])[1]
                break
            else:
                # if goal is reached but actions are interfering with one another, apply
                # no good test --> mutex count, state count and action count
                # will hit a plateu
                if len(states_in_current_layer) == len(states_in_prior_layer) and \
                        len(actions_in_current_layer) == len(actions_in_prior_layer) and \
                        mutex_count_current_layer == mutex_count_prior_layer:
                    print('no goal reached')
                    break
                else:
                    continue
        else:
            # no good test --> mutex count, state count and action count
            # will hit a plateu
            if len(states_in_current_layer) == len(states_in_prior_layer) and \
                len(actions_in_current_layer) == len(actions_in_prior_layer)and \
                    mutex_count_current_layer == mutex_count_prior_layer:
                print('no goal reached')
                break

    print('#################################################')
    print('-------------------------------------------------')
    print('|List of States, Actions and Mutex in each layer|')
    print('-------------------------------------------------')
    for i in range(0,limit+1):
        print('\nLayer {0}:\n'.format(i))
        print('states:')
        for node in planning_graph:
            if node.index == i and node.type == 'state':
                print('name: {0}{1}'.format(node.truth_value, node.name), end=' | mutexes: ')
                for item in node.mutex:
                    print('{0}{1}'.format(item.truth_value, item.name), end=', ')
                print('| total: {0}'.format(len(node.mutex)), end='')
                print('')
        print('\nactions:')
        for node in planning_graph:
            if node.index == i and node.type == 'action':
                print('name: {0}'.format(node.name), end=' | mutexes: ')
                for item in node.mutex:
                    print('{0}'.format(item.name), end=', ')
                print('| total: {0}'.format(len(node.mutex)), end='')
                print('')
        print('********************************************')
    print('#################################################')
    return reverse_planning_graph, limit


if len(sys.argv) == 2:
    response = process_input(sys.argv[1]) # parse the input file, generate states, actions
    init = response[0]
    goal = response[1]
    states = response[2]
    actions = response[3]

    print('############################')
    print('----------------------------')
    print('|List of States and Actions|')
    print('----------------------------')

    print('Init:', end=' ')
    for state in init:
        print('{0}{1}'.format(state.truth_value, state.name), end=', ')

    print('\nGoal:', end=' ')
    for state in goal:
        print('{0}{1}'.format(state.truth_value, state.name), end=', ')


    print('\nAll States:', end=' ')
    for state in states:
        print('{0}{1}'.format(state.truth_value, state.name), end=', ')

    print('\nActions: ', end=' ')
    for action in actions:
        print('{0}'.format(action.name), end=', ')
    print('\n############################')

    response = generate_planner(init, goal, actions) # run the graph-plan algorithm
    solution = response[0]
    limit = response[1]

    if solution != None:
        print('\n#####')
        print('------')
        print('|Plan|')
        print('------')
        for i in range(0, limit):
            print('layer {0}'.format(i), end=': ')
            for node in solution:
                if not node.name.startswith('no-op') and node.type == 'action' and node.index == i:
                   print('{0}'.format(node.name), end=', ')
            print('')
        print('######')

else:
    print('illegal input')