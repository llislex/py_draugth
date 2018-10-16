import board
import random
b = board.Board()
b.set_white(i for i in xrange(31, 51))
b.set_black(i for i in xrange(1, 21))

player = 1
print b

for move in xrange(0, 100):
    print move
    hits = b.hits(player)
    if hits:
        b._apply_hit(random.choice(hits))
    else:
        moves = b.moves(player)
        if moves:
            b._apply_move(random.choice(moves))
        else:
            print "black" if player > 0 else "white", "win"
            break
    player = -player
    print b
