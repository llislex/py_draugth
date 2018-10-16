class Node:
    def __init__(self, value, owner=None):
        self.value = value
        self.owner = owner
        self.parent = None
        self.child = []
        self.level = 0

    def append(self, value):
        n = Node(value, self.owner)
        self.owner.add(n, self)
        return n

    def nodes_number(self):
        result = 1
        for c in self.child:
            result += c.nodes_number()
        return result

    def end_points(self):
        if len(self.child) == 0:
            yield self
        for c in self.child:
            for sub_end_point in c.end_points():
                yield sub_end_point

    def __iter__(self):
        it = self
        while it:
            yield it
            it = it.parent
        raise StopIteration

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class Tree:
    def __init__(self):
        self.root = None

    def append(self, value, parent=None):
        if parent:
            parent.owner = self
            return parent.append(value)
        else:
            self.root = Node(value, self)
            return self.root

    def add(self, node, parent):
        node.owner = self
        if parent:
            assert node not in parent.child
            parent.child.append(node)
            node.level = parent.level + 1
        else:
            self.root = node
        node.parent = parent

    def remove(self, node):
        if node.parent:
            node.parent.child.remove(node)
        else:
            self.root = None
        for c in node.child:
            self.remove(c)
        node = None

    def trim_siblings(self, node):
        if node.parent:
            for n in node.parent.child:
                if n != node:
                    self.remove(n)

    def prn(self, node, level, step):
        st = ''
        if node:
            st = ' ' * step * level + str(node) + '\n'
            for c in node.child:
                st += self.prn(c, level + 1, step)
        return st

    def __str__(self):
        return self.prn(self.root, 0, 4)

    def nodes_number(self):
        return self.root.nodes_number()


def search_back(node, value, functor=lambda n, v: n.value == v):
    level = 0
    while node:
        if functor(node, value):
            return level
        node = node.parent
        level += 1
    return -1
