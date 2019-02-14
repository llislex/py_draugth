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
    for i in xrange(0, len(board.dot)):
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
        for m0 in rules.play(board, turn):
            b0 = board.clone()
            rules.apply(b0, turn, m0)
            l1 = root.append(MoveWeight(m0, 99))
            for m1 in rules.play(b0,-turn):
                b1 = board.clone(b0)
                rules.apply(b1, turn, m1)
                l2 = l1.append(MoveWeight(m1, -99))
                if len(m1) > 2 and depth > 0:
                    add_ply(l2, b1, rules, turn, depth - 1)
                else:
                    e = evaluate(b1, turn)
                    l2.value.set_weight(e)
    else:
        for child in root.child:
            b0 = board.clone()
            rules.apply(0, child.value.move)
            add_ply(child, b0, rules, turn, depth, min_weight)


max_value = 100


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

def indent(level):
    result = ''
    for i in xrange(0, level):
        result += ' '
    return result

def store_move(move, level):
    return indent(level)+move+'\n'
    

def is_hit(move):
    return len(move) > 2
    
num_nodes = 0
    
def build_game_tree(root, level, board, rules, turn, depth):
    #print "build_game_tree", level, depth
    global num_nodes
    if depth > 0:
        for m0 in rules.play(board, turn):
            b0 = board.clone()
            rules.apply(b0, turn, m0)
            new_depth = depth if is_hit(m0) else depth - 1
            num_nodes = num_nodes + 1
            root = build_game_tree(root + store_move(m0, level), level + 1, b0, rules, -turn, new_depth)
    return root

        
