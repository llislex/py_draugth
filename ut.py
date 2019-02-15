import game_board
import game_rules
import random
import game_ai_player
import time
import threading


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
        self.tree = game_ai_player.build_game_tree(self.tree, 1, self.board, self.rules, self.turn, self.depth)
        end = time.time()
        self.tooktime = end - start

N = 8
b = game_board.Board(N)
b.initial()
rules = game_rules.Rules(N)


#def build_game_tree(root, level, board, rules, turn, depth):
'''
start = time.time()
st =  game_ai_player.build_game_tree('', 0, b, rules, 1, 8)
end = time.time()
print "tree size", len(st), "bytes", "took time", end - start, "sec"
print "tree nodes", game_ai_player.num_nodes, "average tree size", len(st)/game_ai_player.num_nodes
print "average move calc time", (end-start) / game_ai_player.num_nodes
'''

turn = 1
threads = []
for mx in rules.play(b, turn):
    bx = b.clone()
    rules.apply(bx, turn, mx)
    a_move = game_ai_player.store_move(mx, 0, game_ai_player.max_value)
    tx = GameTreeBuilder(bx, rules, -turn, a_move, 1)
    threads.append(tx)
    tx.start()
    
for tx in threads:
    tx.join()
    print tx.tree
    
for tx in threads:    
    print "tree size", len(tx.tree), "bytes", "took time", tx.tooktime, "sec"
    print ""