import minimax_player
import board


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

white_player = minimax_player.MinimaxPlayerA(1)
black_player = minimax_player.MinimaxPlayerA(-1)
white_player.set_board(b)
move_number = 1

while True:
    white_move = white_player.play()
    if white_move is None:
        print "black win"
        break

    white_player.apply_own_move()
    b.apply_move(white_move)
    print b
    print move_number, white_move

    if move_number != 1:
        black_player.apply_enemy_move(white_move)
    else:
        black_player.set_board(b)

    black_move = black_player.play()
    if black_move is None:
        print "white win"
        break

    white_player.apply_enemy_move(black_move)

    black_player.apply_own_move()
    b.apply_move(black_move)
    print b
    print move_number, white_move, black_move
    move_number += 1




