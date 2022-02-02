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


# negamax algorithm
def build_game_tree(board, rules, white_turn, depth, alpha, beta):
    if depth == 0:
        return evaluate(board) if white_turn else -evaluate(board)
    result = -max_value
    for m0 in rules.play(board, white_turn):
        b0 = rules.transformed_board(board, m0)
        new_depth = depth if is_hit(m0) else depth - 1
        result = max(result, -build_game_tree(b0, rules, not white_turn, new_depth, -beta, -alpha))
        # print('move', m0, 'eval', result, alpha)
        alpha = max(alpha, result)
        # print(b0)
        if alpha >= beta:
            break
    return result


def get_evaluated_moves(board, rules, white_turn, depth, alpha, beta):
    if depth == 0:
        return evaluate(board) if white_turn else -evaluate(board)
    result = -max_value
    evaluated = []
    for m0 in rules.play(board, white_turn):
        b0 = rules.transformed_board(board, m0)
        new_depth = depth if is_hit(m0) else depth - 1
        result = max(result, -build_game_tree(b0, rules, not white_turn, new_depth, -beta, -alpha))
        alpha = max(alpha, result)
        evaluated.append((b0, m0, result))
        if alpha >= beta:
            break
    return result, evaluated
