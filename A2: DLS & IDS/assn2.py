import binaryTree
import contextlib
import random

start = int(input("Enter Start: "))
stop = int(input("Enter Stop: "))
v = random.sample(range(start,stop),int(input("Enter no of nums to generate: ")))

nodes = [None if x is None else binaryTree.Node(x) for x in v]
root = binaryTree.constructBinaryTree(nodes)

root.print(locals=input("Print Locals? (y/n): ") == "y")

goal = int(input("enter Goal: "))
source = int(input("Enter Source Node Number: "))
lev = int(input("Level Limit"))
nodes[source-1].DLS(goal,lev-1)
print("\n##################################################\nIDS: ")
nodes[0].IDS(goal,lev-1)