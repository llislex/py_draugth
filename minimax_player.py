import random
import tree
import time

max_value = 1000


def maxi(node):
    if node.terminal():
        assert(node.value.weight is not None)
        return node.value.weight
    result = -max_value
    for child in node.child:
        v = mini(child)
        child.value.set_weight(v)
        result = max(result, v)
    return result


def mini(node):
    if node.terminal():
        return node.value.weight
    result = max_value
    for child in node.child:
        v = maxi(child)
        child.value.set_weight(v)
        result = min(result, v)
    return result


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


def evaluate(_board, player):
    result = 0
    for i in xrange(1, len(_board.dot)):
        if _board.empty(i):
            continue
        v = 3 if _board.dam(i) else 1
        result += v if _board.owned_by(player, i) else -v
    return result


def add_ply(root, _board, player, depth=1, min_weight=None):
    if root.terminal():
        if min_weight is not None:
            if root.value.weight < min_weight:
                return
        for b0, m0 in _board.play(player):
            l1 = root.append(MoveWeight(m0, 999))
            for b1, m1 in b0.play(-player):
                l2 = l1.append(MoveWeight(m1, -999))
                if m1.hit and depth > 0:
                    add_ply(l2, b1, player, depth - 1)
                else:
                    e = evaluate(b1, player)
                    l2.value.set_weight(e)
    else:
        for child in root.child:
            b0 = _board.clone(child.value.move)
            add_ply(child, b0, player)


class MinimaxPlayerA:
    def __init__(self, player):
        self.player = player
        self.default_depth = 2
        self.next_move = None
        self._board = None
        self.variants = None
        self.root = None

    def set_board(self, brd):
        self._board = brd.clone()
        self.variants = tree.Tree()
        self.root = self.variants.append(MoveWeight(None, evaluate(self._board, self.player)))

    def play_tree_trim(self):
        trim_list = []
        for child in self.root.child:
            if child.value.weight < self.root.value.weight:
                trim_list.append(child)
        for it in trim_list:
            self.root.owner.remove(it)

    def play(self):
        start_time = time.time()
        self.play_tree_trim()
        if self.root.terminal():
            add_ply(self.root, self._board, self.player, self.default_depth)
        elif self.root.child[0].value.move.move:
            self.variants.trim_siblings(random.choice(self.root.child))
            add_ply(self.root, self._board, self.player,  self.default_depth, self.root.value.weight)
        evaluation = maxi(self.root)
        self.root.value.set_weight(evaluation)
        if self.root.terminal():
            return None
        self.default_depth = 1
        self.next_move = max(self.root.child, key=lambda x: x.value.weight)
        end_time = time.time()
        print
        print self.next_move, end_time - start_time, "sec"
        return self.next_move.value.move

    def apply_own_move(self):
        self._board.apply_move(self.next_move.value.move)
        self.variants.trim_siblings(self.next_move)

    def apply_enemy_move(self, move):
        n = next(x for x in self.next_move.child if x.value.move == move)
        self._board.apply_move(move)
        self.next_move = None
        self.variants.trim_siblings(n)
        self.root = n
