import minimax_player
import board
import game


b = board.Board()
b.load("""
 x x x x x
x x x x x 
 x x x x x
x x x x x 
 . . . . .
. . . . . 
 o o o o o
o o o o o 
 o o o o o
o o o o o  
""")

white_player = minimax_player.AI0(1)
black_player = minimax_player.AI0(-1)

g = game.Game(b, white_player, black_player)

while g.step() is not None:
    g.show()
print "White won" if g.current_player == -1 else "Black won"
print g
print g.board




