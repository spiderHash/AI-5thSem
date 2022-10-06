# State Space Tree
# Decantion Problem

class Node:
    def __init__(self, state, parent=None, limit=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.limit = limit
        

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent

    def getState(self):
        return self.state

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self.state)


def constructStateSpaceTree(initialState, goalState, actions):
    root = Node(initialState)
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node.state == goalState:
            return node
        for action in actions:
            child = Node(action(node.state), node)
            node.addChild(child)
            queue.append(child)
    return None


def printPath(node):
    if node is None:
        return
    printPath(node.getParent())
    print(f" Parent : {node.getParent()}", end=" ")
    print(node.getState())

def printNode(node):
    if not Node:
        print(f"Sate is {node.state}")
        print(f"Parnt : {node.parent.state}")
        print(f"Level is: {node.limit}")

# def isGoal():
#     return (2, 0) or (2, 1) or (2, 2) or (2, 3) or (2, 4)

# def main():
#     initialState = (0, 0)
#     goalState = [(2, 0), (4, 2)]
#     actions = [lambda state: (4, state[1]), lambda state: (state[0], 3), lambda state: (0, state[1]), lambda state: (state[0], 0), lambda state: (
#         state[0] - min(state[0], 3 - state[1]), state[1] + min(state[0], 3 - state[1])), lambda state: (state[0] + min(state[1], 4 - state[0]), state[1] - min(state[1], 4 - state[0]))]
#     for goal in goalState:
#         node = constructStateSpaceTree(initialState, goal, actions)
#         if node is not None:
#             printPath(node)
#             print()

# if __name__ == "__main__":
#     main()


# fuction S that returns the list of successors of a given state
def nextState(state):
    return [lambda state: (4, state[1]), lambda state: (state[0], 3), lambda state: (0, state[1]), lambda state: (state[0], 0), lambda state: (
        state[0] - min(state[0], 3 - state[1]), state[1] + min(state[0], 3 - state[1])), lambda state: (state[0] + min(state[1], 4 - state[0]), state[1] - min(state[1], 4 - state[0]))]


# Search Algorithms

# Breadth First Search
def BFS(initialState, goalState, actions):
    root = Node(initialState)
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node.state == goalState:
            return node
        for action in actions:
            child = Node(action(node.state), node)
            node.addChild(child)
            queue.append(child)
    return None

# Depth First Search




def DFS(initialState, goalState, actions):
    explored = set()
    root = Node(initialState)
    stack = [root]
    while stack:
        node = stack.pop()
        if node.state == goalState:
            return node
        if (currentState:=node.state) not in explored:
            explored.add(currentState)
            for action in actions:
                child = Node(action(node.state), node)
                node.addChild(child)
                stack.append(child)
    return None

# Depth Limited Search




def DLS(initialState, goalState, actions, limitInp):
    explored = set()
    root = Node(initialState)
    root.limit = 1
    stack = [root]
    while stack:
        node = stack.pop()
        if node.state == goalState:
            return node
        if (currentState:=node.state) not in explored and node.limit < limitInp:
            explored.add(currentState)
            for action in actions:
                child = Node(action(node.state), node)
                child.limit = node.limit + 1
                node.addChild(child)
                stack.append(child)
    return None


    

# Iterative Deepening Search


def IDS(initialState, goalState, actions):
    for limit in range(100):
        node = DLS(initialState, goalState, actions, limit)
        if node is not None:
            return node
    return None

# Get Initial State from User


def getInitialState():
    while True:
        try:
            initial = input("Enter the initial state: ")
            initial = initial.split()
            initial = tuple(map(int, initial))
            if len(initial) != 2:
                print("Invalid Input")
                continue
            if initial[0] > 4 or initial[1] > 3:
                print("Invalid Input")
                continue
            return initial
        except Exception:
            print("Invalid Input")

# Get Goal State from User


def getGoalState():
    while True:
        try:
            goal = input("Enter the goal state: ")
            goal = goal.split()
            goal = tuple(map(int, goal))
            if len(goal) != 2:
                print("Invalid Input")
                continue
            if goal[0] > 4 or goal[1] > 3:
                print("Invalid Input")
                continue
            return goal
        except Exception:
            print("Invalid Input")

# Implementing the Decantion Problem


def main():
    initialState = getInitialState()
    goalState = getGoalState()
    actions = nextState(initialState)
    print("Breadth First Search")
    node = BFS(initialState, goalState, actions)
    if node is not None:
        printPath(node)
        print()
    else:
        print("No Solution")

    print("Depth First Search")
    node = DFS(initialState, goalState, actions)
    if node is not None:
        printPath(node)
        print()
    else:
        print("No Solution")

    print("Depth Limited Search")
    limiit = int(input("Enter the limit: "))
    node = DLS(initialState, goalState, actions, limiit)
    if node is not None:
        printPath(node)
        print()
    else:
        print("No Solution")

    print("Iterative Deepening Search")
    node = IDS(initialState, goalState, actions)
    if node is not None:
        printPath(node)
        print()
    else:
        print("No Solution")


if __name__ == "__main__":
    main()