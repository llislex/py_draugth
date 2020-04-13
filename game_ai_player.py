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


def build_game_tree(board, rules, white_turn, depth):
    result = -max_value if white_turn else max_value
    for m0 in rules.play(board, white_turn):
        b0 = rules.transformed_board(board, m0)
        new_depth = depth if is_hit(m0) else depth - 1
        evaluation = build_game_tree(b0, rules, not white_turn, new_depth) if new_depth > 0 else evaluate(board)
        result = max(result, evaluation) if white_turn else min(result, evaluation)
    return result


def get_evaluated_moves(board, rules, white_turn, depth):
    result = -max_value if white_turn else max_value
    evaluated = []
    for m0 in rules.play(board, white_turn):
        b0 = rules.transformed_board(board, m0)
        new_depth = depth if is_hit(m0) else depth - 1
        evaluation = build_game_tree(b0, rules, not white_turn, new_depth) if new_depth > 0 else evaluate(board)
        result = max(result, evaluation) if white_turn else min(result, evaluation)
        evaluated.append((b0, m0, evaluation))
    return result, evaluated
