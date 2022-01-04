import game_board


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


def is_hit(move):
    return len(move) > 2


def negamax(board, rules, white_turn, depth, alpha, beta):
    if depth == 0:
        return evaluate(board) if white_turn else -evaluate(board)
    result = -max_value
    for m0 in rules.play(board, white_turn):
        b0 = rules.transformed_board(board, m0)
        new_depth = depth if is_hit(m0) else depth - 1
        evaluation = negamax(b0, rules, not white_turn, new_depth, -beta, -alpha)
        result = max(result, -evaluation)
        alpha = max(alpha, result)
        if alpha >= beta:
            break
    return result

