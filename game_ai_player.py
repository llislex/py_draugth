import game_rules
import game_board
import re

class TextNode:
    def __init__(self, root_lines, index):
        self.root_lines = root_lines
        self.index = index
        line = root_lines[index]
        self.level, self.move, self.weight = move_from_str(line)
       
    def next(self):
        next_index = self.index + 1
        if next_index < len(self.root_lines):
            return TextNode(self.root_lines, next_index)
        else:
            return None

    def child(self):
        n = self.next()
        while n is not None and n.level > self.level:
            if n.level == self.level + 1:
                yield n
            n = n.next()
            
    def terminal(self):
        n = self.next()
        return n is None or n.level != self.level + 1
        
    def set_weight(self, new_weight):
        l, m, w = move_from_str(self.root_lines[self.index])
        st = move_to_str(m, l, new_weight)
        self.root_lines[self.index] = st
        self.weight = new_weight
        
    def __str__(self):
        return indent(self.level) + "m:"+str(self.move)+" w:"+str(self.weight)+" i:" + str(self.index)
        
            
def evaluate(_board):
    result = 0
    for i in range(0, game_board._N):
        c = _board.dot(i)
        if c == 'o':
            result += 1
        elif c == 'O':
            result += 3
        elif c == 'x':
            result -= 1
        elif c == 'X':
            result -= 3
        else:
            continue
    return result

max_value = 100


def maxi(node):
    if node.terminal():
        assert(node.weight is not None)
        return node.weight, []
    result = -max_value
    max_list = []
    for child in node.child():
        v, lst = mini(child)
        child.set_weight(v)
        if v > result:
            max_list = [child.index]
            result = v
        elif v == result:
            max_list.append(child.index)
    return result, max_list


def mini(node):
    if node.terminal():
        return node.weight, []
    result = max_value
    min_list = []
    for child in node.child():
        v, lst = maxi(child)
        child.set_weight(v)
        if v < result:
            min_list = [child.index]
            result = v
        elif v == result:
            min_list.append(child.index)
        result = min(result, v)
    return result, min_list
    
    
def indent(level):
    result = ''
    for i in range(1, level):
        result += ' '
    return result
    
def move_to_str(move, level, eval):
    #return str(level)+indent(level)+" "+move+" "+str(eval)
    return str(level)+" "+move+" "+str(eval)
    
def move_from_str(st):
    #m = re.search("^([-]?[0-9]+)\s+(.+) ([-]?[0-9]+)$", st)
    m = re.search("^([-]?[0-9]+) (.+) ([-]?[0-9]+)$", st)
    if m:
        w = int(m.group(3))
        l = int(m.group(1))
        m = m.group(2)
        return l, m, w
    print(st)
    assert(False)
    return None, None, None
    

def is_hit(move):
    return len(move) > 2
    
def build_game_tree(root, level, board, rules, white_turn, depth):
    if depth > 0:
        for m0 in rules.play(board, white_turn):
            b0 = board.clone()
            rules.apply(b0, m0)
            new_depth = depth if is_hit(m0) else depth - 1
            if new_depth == 0:
                eval = evaluate(board)
            else:
                eval = max_value if white_turn else -max_value
            root = build_game_tree(root + move_to_str(m0, level, eval)+'\n', level + 1, b0, rules, not white_turn, new_depth)
    return root
   
def play_game_tree(board, rules, root_lines, index):
    n = TextNode(root_lines, index)
    b = board.clone()
    rules.apply(b, n.move)
    st = b.save()+'\n'
    for child in n.child():
        st += play_game_tree(b, rules, root_lines, child.index)
    return st