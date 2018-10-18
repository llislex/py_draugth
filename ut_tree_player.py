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
    for node1 in node.child:
        if node.value.weight <= node1.value.weight:
            print node1.value
            return node1
    print node
    print node.child
    return None


def evaluate_board(board, player):
    result = 0
    for n in xrange(1, len(board.dot)):
        if board.empty(n):
            continue
        v = 3 if board.dam(n) else 1
        result += v if board.owned_by(player, n) else -v
    return result


def maxi(node):
    if node.terminal():
        assert(node.value.weight is not None)
        return node.value.weight
    result = -1000
    for child in node.child:
        v = mini(child)
        child.value.set_weight(v)
        result = max(result, v)
    return result


def mini(node):
    if node.terminal():
        return node.value.weight
    result = 1000
    for child in node.child:
        v = maxi(child)
        child.value.set_weight(v)
        result = min(result, v)
    return result


def play_tree_add_ply(root, board, player, level=0, level_limit=1, min_weight=None):
    if root.terminal():
        if min_weight is not None:
            if root.value.weight < min_weight:
                return
        for b0, m0 in board.play(player):
            l1 = root.append(MoveWeight(m0, 999))
            for b1, m1 in b0.play(-player):
                l2 = l1.append(MoveWeight(m1, -999))
                if m1.hit and level < level_limit:
                    play_tree_add_ply(l2, b1, player, level + 1)
                else:
                    e = evaluate_board(b1, player)
                    l2.value.set_weight(e)
    else:
        for child in root.child:
            b0 = board.clone(child.value.move)
            play_tree_add_ply(child, b0, player)


def play_tree_trim(root, min_weight):
    trim_list = []
    for child in root.child:
        if child.value.weight < min_weight:
            trim_list.append(child)
    for it in trim_list:
        root.owner.remove(it)


b = board.Board()
# b.set_white(i for i in xrange(31, 51))
# b.set_black(i for i in xrange(1, 21))
b.load("""
 x x x x x
x x x x x 
 x x x . x
x x x x x 
 . . x . .
. . o . . 
 o o . o o
o o o o o 
 o o o o o
o o o o o
""")

player = 1
cnt = 0

variants = tree.Tree()
node = variants.append(MoveWeight(None, 0))

start = time.time()
play_tree_add_ply(node, b, player, 0, 1)
evaluation = maxi(node)
delta = time.time()-start
print delta, evaluation
play_tree_add_ply(node, b, player, 0, 1, evaluation)
evaluation = maxi(node)
delta = time.time()-start
print delta
print '------------------------'

while True:
    node.value.set_weight(evaluation)
    n1 = choose_move(node)
    if n1 is None:
        print "black win"
        break
    b.apply_move(n1.value.move)

    #print variants
    variants.trim_siblings(n1)
    #print "after trim siblings", variants
    print "evaluation", evaluation
    print "nodes", variants.nodes_number()
    print n1.value.move, n1.value.weight
    print b

    if len(n1.child) == 0:
        print "white win"
        break

    opponent_move_index = 0
    for no in n1.child:
        print opponent_move_index, no.value.move
        opponent_move_index += 1

    opponent_move_index = input(">")
    n2 = n1.child[opponent_move_index]

    #n2 = random.choice(n1.child)

    b.apply_move(n2.value.move)
    variants.trim_siblings(n2)
    print variants.nodes_number(), "end points", variants.end_points_number()
    print n2.value.move
    print b

    play_tree_trim(n2, evaluation)
    #print variants
    print "after trim", variants.nodes_number(), "end points", variants.end_points_number()

    if n2.terminal():
        play_tree_add_ply(n2, b, player)
        evaluation = maxi(n2)
    elif n2.child[0].value.move.move:
        variants.trim_siblings(n2.child[0])
        play_tree_add_ply(n2, b, player, 0, 2, evaluation)
        evaluation = maxi(n2)

    node = n2
    node.value.set_weight(n1.value.weight)


