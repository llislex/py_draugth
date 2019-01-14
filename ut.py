import game_board
import game_rules
import random
import tree

def print_hits(variants):
    for variant in variants:
        for step in variant[:-1]:
            print step[0],"x",
        print variant[-1][0]

def print_moves(variants):
    for variant in variants:
        print variant[0], "-", variant[1]


N = 8
b = game_board.Board(N)


b.load("""
 . x . .
. . x .
 . . . .
. . . .
 . . . .
. . o .
 . . . .
. o . .
""")


'''
b.load("""
 . . .
. . . 
 x . X
. o o 
 o . .
. . . 
""")
'''
print b

print list(b.units(1))
print list(b.units(-1))

r = game_rules.Rules(N)
player = -1


for i in xrange(0, 5):
    hits = r.hits(b, player)
    print i
    print hits
    if len(hits) > 0:
        h = random.choice(hits)
        r.apply_hit(b, h)
        print b, h
    else:
        moves = r.moves(b, player)
        print moves
        if len(moves) > 0:
            m = random.choice(moves)
            r.apply_move(b, m)
            print b, m
    player = -player

'''
# ut 1
b = board.Board()
b.set_white([46])
b.set_black([41, 32, 33, 34, 22, 23, 24, 12, 13, 14])

print b

wp = tree.Tree().append((46, -1))
wp.owner.value = []

#num = b.hit_way(-1, 46, wp)
num = b.hit_dam_way(-1, 46, wp)

print "num", num
print wp.owner

print wp.owner.value

wp.owner.value = b.majority(wp)
print wp.owner.value
'''

'''
# ut 2

b = board.Board()
b.set(board._white_dam, 50)
#b.set_white([46, 47])
#b.set_white_dam([48])
b.set_black([41, 32, 33, 34, 22, 23, 24, 12, 13, 14])
# b.set(board.b, [23, 13, 24])
print b

print_hits(b.hits(1))
print_moves(b.moves(1))
'''


# ut 3
'''
b = board.Board()
b.set(board._white_dam, 50)
#b.set_white([46, 47])
#b.set_white_dam([48])
b.set_black([41, 32, 33, 34, 22, 23, 24, 12, 13, 14])
# b.set(board.b, [23, 13, 24])
print b

h = b.hits(1)
print_hits(h)
b._apply_hit(h[0])
print b
'''
'''
print_moves(b.moves(1))
b._apply_move(b.moves(1)[0])
print b
'''



