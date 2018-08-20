import tree
from tree import Node
from tree import Tree

n = Node(1)
t = Tree()
t.add(n, None)
n1 = n.append(2)
n.append(3)
n.append(4)
n1.append(5)
n1.append(6)
n2 = n1.append(7)
n2.append(8)
n2.append(9)

print t
print '------'

print tree.search_back(n2, 3)
print tree.search_back(n2, 1)

t.remove(n)

print t
