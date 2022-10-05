import binaryTree
import contextlib

r = False
with contextlib.suppress(Exception):
    from rich.console import Console
    r = True

if r:
    console = Console()
    console


color = input("Enter Color: ").lower()
while color not in ["red", "green"]:
    color = input("Enter Color: ")

n = int(input("Enter Number of Nodes: "))

v = []
if color == "green":
    v.extend(iter(range(2, 2*n+1, 2)))
elif color == "red":
    v.extend(iter(range(1, 2*n+1, 2)))

nodes = [None if x is None else binaryTree.Node(x) for x in v]
root = binaryTree.constructBinaryTree(nodes)

if r:
    console.print("Binary Tree: ", style="bold italic underline magenta")
else:
    print("Binary Tree: ")

root.print(locals=input("Print Locals? (y/n): ") == "y")
if r:
    console.print("\nBFS Traversal: ", style="bold red italic")
else:
    print("\nBFS Traversal: ")
root.BFS()
if r:
    console.print("\nDFS Traversal: ", style="bold yellow italic")
else:
    print("\nDFS Traversal: ")
root.DFS()
print("\n")

x = int(input("Enter the Node number to display state: "))
nodes[x-1].state()


nodes[1].DLS(46,int(input("Enter level")))