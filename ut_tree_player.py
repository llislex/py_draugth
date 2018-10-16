import board
import tree
import time
import random


class MoveWeight:
    def __init__(self, move, weight):
        self.move = move
        self.weight = weight

    def set_weight(self, weight):
        self.weight = weight

    def __str__(self):
        return str(self.move)+", " + str(self.weight)

    def __repr__(self):
        return self.__str__()


def choose_move(node):
    print node
    for node1 in node.child:
        if node.value.weight == node1.value.weight:
            print node1.value
            return node1
    print node
    print node.child
    assert false


def evaluate_board(board, player):
    result = 0
    for n in xrange(1, len(board.dot)):
        if board.empty(n):
            continue
        v = 3 if board.dam(n) else 1
        result += v if board.owned_by(player, n) else -v
    return result


def build_play_tree(node0, brd, player, depth):
    if depth > 0:
        max_list = []
        for b0, m0 in brd.play(player):
            node1 = node0.append(MoveWeight(m0, 100500))
            min_list = []
            for b1, m1 in b0.play(-player):
                node2 = node1.append(MoveWeight(m1, 2000))
                new_depth = depth - 1 if m1.move else 1
                v = build_play_tree(node2, b1, player, new_depth)
                node2.value.set_weight(v)
                min_list.append(v)
            min_value = min(min_list)
            node1.value.set_weight(min_value)
            max_list.append(min_value)
        max_value = max(max_list)
        node.value.set_weight(max_value)
        return max_value
    result = evaluate_board(brd, player)
    node.value.set_weight(result)
    return result


b = board.Board()
b.set_white(i for i in xrange(31, 51))
b.set_black(i for i in xrange(1, 21))

player = 1
cnt = 0

variants = tree.Tree()
node = variants.append(MoveWeight(None, 0))

start = time.time()
build_play_tree(node, b, player, 2)
delta = time.time()-start
print delta
print '------------------------'

while len(node.child) > 0:
    n1 = choose_move(node)
    b.apply_move(n1.value.move)

    variants.trim_siblings(n1)
    print variants.nodes_number()
    print n1.value.move
    print b

    opponent_move_index = 0
    for no in n1.child:
        print opponent_move_index, no.value.move
        opponent_move_index += 1

    opponent_move_index = input(">")
    n2 = n1.child[opponent_move_index]
    b.apply_move(n2.value.move)
    variants.trim_siblings(n2)
    print variants.nodes_number()
    print n2.value.move
    print b
    node = n2
    node.value.set_weight(n1.value.weight)
