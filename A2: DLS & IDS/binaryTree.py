import contextlib
import math
import sys

with contextlib.suppress(Exception):
    from rich import print


class Node:

    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
        self.level = None
        self.actions = []

    def print(self, level=0, locals=False):
        if self.right:
            self.right.print(level + 1, locals)
        if locals:
            print("   " * 5 * level, end="")
        else:
            print("   " * level, end="")
        if locals:
            print(
                f"Data: {str(self.data)} \n{'   ' * 5 * level}Left: {self.left.data if self.left else 'None'} \n{'   ' * 5 * level}Right: {self.right.data if self.right else 'None'} \n{'   ' * 5 * level}Parent: {self.parent.data if self.parent else 'None'}"
            )
        else:
            print(f"{self.data}")

        if self.left:
            self.left.print(level + 1, locals)

    def __repr__(self) -> str:
        return f"Data: {str(self.data)} \nLeft: {self.left.data if self.left else 'None'} \nRight: {self.right.data if self.right else 'None'} \nParent: {self.parent.data if self.parent else 'None'}\nActions: {self.actions}"

    def state(self):
        print(self)

    def BFS(self):
        if self is None:
            return
        queue = [self]
        while queue:
            node = queue.pop(0)
            print(node.data, end="->")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def DFS(self):
        if self is None:
            return
        print(self.data, end="->")
        if self.left:
            self.left.DFS()
        if self.right:
            self.right.DFS()

    def DLS(self, goal, lev):
        if self is None or goal is None:
            return
        if self.level > lev:
            return
        else:
            if self.data == goal:
                print(self.data)
                print("Found")
                sys.exit()
                return
            print(self.data, end='->')
            if self.left:
                self.left.DLS(goal, lev)
            if self.right:
                self.right.DLS(goal, lev)

    def IDS(self, goal, level):
        l = 0
        for l in range(level + 2):
            print(f"\nLevel: {l+1}")
            self.DLS(goal, l)
            print("\n")


def constructBinaryTree(
        nodes):  # sourcery skip: instance-method-first-arg-name
    for i in range(len(nodes)):
        node = nodes[i]
        if node is not None:
            with contextlib.suppress(Exception):
                node.left = nodes[2 * i + 1]
                nodes[2 * i + 1].parent = node
                node.actions.append(f"Left: {node.left.data}")
            with contextlib.suppress(Exception):
                node.right = nodes[2 * i + 2]
                nodes[2 * i + 2].parent = node
                node.actions.append(f"Right: {node.right.data}")

            node.level = int(math.log(i + 1, 2))
    return nodes[0] if nodes else None


if __name__ == '__main__':
    print("This is a module for AI Assn1.")
    print("Please run assn1.py instead.")
    exit(1)
