import board
import tree

def print_hits(variants):
    for variant in variants:
        for step in variant[:-1]:
            print step[0],"x",
        print variant[-1][0]

def print_moves(variants):
    for variant in variants:
        print variant[0], "-", variant[1]

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
print_moves(b.moves(1))
b._apply_move(b.moves(1)[0])
print b
'''



