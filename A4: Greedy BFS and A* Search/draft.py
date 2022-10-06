from utils import *


class Graph:
    """
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
        g.get('A') to get a dict of links out of A
        g.get('A', 'B') to get the length of the link from A to B
    """

    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        """Make a digraph into an undirected graph by adding symmetric edges."""
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed:
            self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graph_dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        return links if b is None else links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set(list(self.graph_dict.keys()))
        s2 = {k2 for v in self.graph_dict.values() for k2, v2 in v.items()}
        nodes = s1.union(s2)
        return list(nodes)


def UndirectedGraph(graph_dict=None):
    """Build a Graph where every edge (including future ones) goes both ways."""
    return Graph(graph_dict=graph_dict, directed=False)


class Problem:

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        # TODO
        # Return a list of actions that can be executed in the given state.
        # or Yeild one action at a time
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return any(x is state for x in self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return f"<Node {self.state}>"

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        return Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


def best_first_graph_search(problem, heur, display=False):
    # f = memoize(f, 'f')
    f = heur
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and",
                      len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


greedy_best_first_graph_search = best_first_graph_search     # f(n) = h(n)


def astar_search(problem, h=input("Manhattan or Eculidean"), display=False):

    if h == "Manhattan":
        h = manhattan_distance
    elif h == "Eculidean":
        h = distance

    # h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h((n.state[0], n.state[1]), (problem.goal[0], problem.goal[1])), display)


class GraphProblem(Problem):
    """The problem of searching a graph from one node to another."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def find_min_edge(self):
        """Find minimum value of edges."""
        m = np.inf
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)

        return m

    def z(self, node):
        """h function is straight-line distance from a node's state to goal."""
        if locs := getattr(self.graph, 'locations', None):
            if type(node) is str:
                return int(distance(locs[node], locs[self.goal]))

            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return np.inf

# Maze Application
# 3x3 Maze


states = [(x, y) for x in range(1, 4) for y in range(1, 4)]
barriers = int(input("Enter the number of barriers: "))
barrier_states = [tuple(
    map(int, input("Enter the barrier state: ").split())) for _ in range(barriers)]

goal_state = tuple(map(int, input("Enter the goal state: ").split()))
initial_state = tuple(map(int, input("Enter the initial state: ").split()))

graph = UndirectedGraph({s: {} for s in states})
for (x, y) in states:
    if (x, y) not in barrier_states:
        if x < 3:
            graph.connect((x, y), (x + 1, y), distance=int(
                input(f"Enter the distance between ({x}, {y}) and ({x + 1}, {y}): ")))

        if y > 1:
            graph.connect((x, y), (x, y - 1), distance=int(
                input(f"Enter the distance between ({x}, {y}) and ({x}, {y - 1}): ")))

graph.locations = {s: s for s in states}

print("A Star Search")
problem = GraphProblem(initial_state, goal_state, graph)
node = astar_search(problem)
print(initial_state, end='')
print(node.solution())
print("Path Cost: ", node.path_cost)


print("Greedy Best First Search")
problem = GraphProblem(initial_state, goal_state, graph)
# Just Check the heuristic function not path cost
node = greedy_best_first_graph_search(problem, lambda n: manhattan_distance((n.state[0], n.state[1]), (problem.goal[0], problem.goal[1])))
print(initial_state, end='')
print(node.solution())
# print the path cost, heuristic function and the total cost
print("Path Cost: ", node.path_cost)


