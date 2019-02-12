import game_rules
import game_board


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


def add_ply(root, board, rules, turn, depth=1, min_weight=None):
    if root.terminal():
        if min_weight is not None:
            if root.value.weight < min_weight:
                return
        for h0, m0 in rules.play(board, turn):
            b0 = rules.modify_board(board, h0, m0)
            l1 = root.append(MoveWeight(m0 if h0 is None else h0, 999))
            for h1, m1 in rules.play(b0,-turn):
                b1 = rules.modify_board(b0, h1, m1)
                l2 = l1.append(MoveWeight(m1 if h1 is None else h1, -999))
                if h1 is not None and depth > 0:
                    add_ply(l2, b1, rules, turn, depth - 1)
                else:
                    e = evaluate(b1, turn)
                    l2.value.set_weight(e)
    else:
        for child in root.child:
            if type(child.value.move[0]) is tuple:
                b0 = rules.modify_board(board, child.value.move, None)
                add_ply(child, b0, rules, turn, depth, min_weight)
            else:
                b0 = rules.modify_board(board, None, child.value.move)
                add_ply(child, b0, rules, turn, depth, min_weight)


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
