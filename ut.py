import game_board
import game_rules
import random
import game_ai_player
import time
import threading


b = game_board.Board()
b.initial()
print b
print list(b.units(True))
print list(b.units(False))

rules = game_rules.Rules(game_board._n)
for mx in rules.play(b, True):
    bx = rules.transformed_board(b, mx)
    print bx
    

'''
class GameTreeBuilder(threading.Thread):
    def __init__(self, board, rules, turn, m0, depth):
        threading.Thread.__init__(self)
        self.depth = depth
        self.board = board
        self.rules = rules
        self.turn = turn
        self.tree = m0
        self.tooktime = 0

    def run(self):
        start = time.time()
        self.tree = game_ai_player.build_game_tree(self.tree, 2, self.board, self.rules, self.turn, self.depth)
        end = time.time()
        self.tooktime = end - start

N = 8
b = game_board.Board(N)
b.initial()
rules = game_rules.Rules(N)
depth = 4
turn = 1
threads = []
game_tree = '0 x 42\n'
for mx in rules.play(b, turn):
    bx = b.clone()
    rules.apply(bx, mx)
    a_move = game_ai_player.move_to_str(mx, 1, -game_ai_player.max_value)+'\n'
    tx = GameTreeBuilder(bx, rules, -turn, a_move, depth-1)
    threads.append(tx)
    tx.start()
    
for tx in threads:
    tx.join()
    game_tree += tx.tree
    
for tx in threads:    
    print "tree size", len(tx.tree), "bytes", "took time", tx.tooktime, "sec"
    print ""

tt0 = time.time()
game_tree_lines = game_tree.splitlines()
tt1 = time.time()
n = game_ai_player.TextNode(game_tree_lines, 0)
r, move_list = game_ai_player.maxi(n)
tt2 = time.time()
print "result", r
print "split", tt1-tt0, "sec"
print "minimax", tt2-tt1, "sec"

for move_index in move_list:
    print game_ai_player.TextNode(game_tree_lines, move_index)


for ln in game_tree_lines:
    print ln
'''