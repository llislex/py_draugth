class Player:
    def __init__(self):
        print self

    def set_board(self, brd):
        raise NotImplementedError("abstract player " + str(brd))

    def play(self):
        raise NotImplementedError("abstract player resign")
        return None

    def set_opponent_move(self, move):
        pass


class Game:
    def __init__(self, brd, player_a, player_b):
        self.board = brd.clone()
        self.player = [player_a, player_b]
        player_a.set_board(brd)
        player_b.set_board(brd)
        self.current_player = 0
        self.moves = []

    def step(self):
        move = self.player[self.current_player].play()
        if move is not None:
            self.board.apply_move(move)
            self.moves.append(move)
            self.current_player = 1 - self.current_player
            self.player[self.current_player].set_opponent_move(move)
        return move

    def show(self):
        print self.board
        print len(self.moves) / 2 + 1, self.moves[-1]

    def __str__(self):
        st = ""
        for i in xrange(0, len(self.moves)):
            if i % 2 == 0:
                st += str(i / 2 + 1)+". "+str(self.moves[i])+" "
            else:
                st += str(self.moves[i])
        return st
