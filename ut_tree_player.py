import board
import tree
import time


def build_play_tree(node, brd, player, depth):
    if depth > 0:
        n = 0
        for b0, m0 in brd.play(player):
            for b1, m1 in b0.play(-player):
                new_node = node.append((m0, m1))
                n += build_play_tree(new_node, b1, player, depth - 1)
        return n + 1
    return 0


b = board.Board()
b.set_white(i for i in xrange(31, 51))
b.set_black(i for i in xrange(1, 21))

player = 1
#print b
cnt = 0

variants = tree.Tree()
node = variants.append((b, None, None))

start = time.time()
n = build_play_tree(node, b, player, 3)
delta = time.time()-start
print delta, delta/n
print n

#print variants

'''
start = time.time()
for b0, m0 in b.play(player):
    for b1, m1 in b0.play(-player):
        print b1
        print m0, m1
        cnt += 1
delta = time.time()-start
print delta, delta/cnt
print cnt
'''