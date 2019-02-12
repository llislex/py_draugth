import tree
import game_board


_backward = [0, 1]
_forward = [2, 3]
_all_directions = [0, 1, 2, 3]
_vector = [[-1, 1], [1, 1], [-1, -1], [1, -1]]


class BoardGeometry:
    def __init__(self, size):
        self.d = size / 2
        self.D = size
        assert(size >= 4)
        assert(size % 2 == 0)

    def col_index(self, n):
        return (n - 1) % self.d

    def row(self, n):
        return (n - 1) / self.d

    def col(self, n):
        return self.col_index(n) * 2 + 1 - (self.row(n) % 2)

    def number(self, _col, _row):
        i = _col / 2
        return _row * self.d + i + 1

    def near(self, n, direction):
        c = self.col(n) + _vector[direction][0]
        if 0 <= c < self.D:
            r = self.row(n) + _vector[direction][1]
            if 0 <= r < self.D:
                return self.number(c, r)
        return 0


class Rules:
    def __init__(self, board_size):
        g = BoardGeometry(board_size)
        self.way = [[0, 0, 0, 0]]
        for i in xrange(1, board_size * board_size / 2 + 1):
            self.way.append([g.near(i, 0), g.near(i, 1), g.near(i, 2), g.near(i, 3)])
        self.dam_target_white = [i for i in xrange(1, g.d + 1)]
        self.dam_target_black = [g.d * g.D - i for i in xrange(0, g.d)]

    def _hit(self, board, player, n, direction):
        n1 = self.way[n][direction]
        if n1 > 0 and board.owned_by(-player, n1):
            n2 = self.way[n1][direction]
            if n2 > 0 and board.empty(n2):
                return n2, n1
        return None, None

    def _dam_hit(self, board, player, n, direction):
        n1 = self.way[n][direction]
        while n1 > 0 and board.empty(n1):
            n1 = self.way[n1][direction]
        if n1 > 0 and board.owned_by(-player, n1):
            result = []
            n2 = self.way[n1][direction]
            while n2 > 0 and board.empty(n2):
                result.append(n2)
                n2 = self.way[n2][direction]
            return result, n1
        return [], None

    def _hit_way(self, board, player, n, way_point):
        ways = 0
        for direction in _all_directions:
            h, t = self._hit(board, player, n, direction)
            if h and tree.search_back(way_point, t, lambda node, v: node.value[1] == v) < 0:
                wp = way_point.append((h, t))
                sub_ways = self._hit_way(board, player, h, wp)
                ways += sub_ways + 1
                if sub_ways == 0:
                    way_point.owner.value.append(wp)
        return ways

    def _hit_dam_way(self, board, player, n, way_point):
        ways = 0
        for direction in _all_directions:
            hit_list, t = self._dam_hit(board, player, n, direction)
            if hit_list and tree.search_back(way_point, t, lambda node, v: node.value[1] == v) < 0:
                final_wp = []
                final_iteration = True
                for h in hit_list:
                    wp = way_point.append((h, t))
                    sub_ways = self._hit_dam_way(board, player, h, wp)
                    ways += sub_ways + 1
                    if sub_ways == 0:
                        final_wp.append(wp)
                    else:
                        final_iteration = False
                if final_iteration:
                    way_point.owner.value += final_wp
                else:
                    ways -= len(final_wp)
                    for wp in final_wp:
                        wp.owner.remove(wp)
        return ways

    @staticmethod
    def _majority(way_point):
        if len(way_point.owner.value) > 0:
            max_level = max(node.level for node in way_point.owner.value)
            return filter(lambda n: n.level == max_level, way_point.owner.value)
        return []

    def hits(self, board, player):
        result = []
        way_point = tree.Tree().append((0, 0))
        way_point.owner.value = []
        for i in board.units(player):
            wp = way_point.append((i, -1))
            if board.dam(i):
                self._hit_dam_way(board, player, i, wp)
            else:
                self._hit_way(board, player, i, wp)
        for variant in self._majority(way_point):
            hit_path = []
            for step in variant:
                if step.value[0] > 0:
                    hit_path.insert(0, step.value)
            result.append(hit_path)
        return result

    def _move(self, board, player, n):
        directions = _forward if player > 0 else _backward
        for d in directions:
            x = self.way[n][d]
            if x > 0 and board.empty(x):
                yield x

    def _dam_move(self, board, n):
        for d in _all_directions:
            x = self.way[n][d]
            while x > 0 and board.empty(x):
                yield x
                x = self.way[x][d]

    def moves(self, board, player):
        result = []
        for i in board.units(player):
            if board.dam(i):
                for j in self._dam_move(board, i):
                    result.append([i, j])
            else:
                for j in self._move(board, player,i):
                    result.append([i, j])
        return result

    # input m - [ from, to]
    def apply_move(self, board, m):
        s = board.dot[m[0]]
        board.set(game_board.empty, m[0])
        board.dot[m[0]] = game_board.empty
        if s == game_board.white and m[1] in self.dam_target_white:
            s = game_board.white_dam
        if s == game_board.black and m[1] in self.dam_target_black:
            s = game_board.black_dam
        board.set(s, m[1])

    def apply_hit(self, board, hit_path):
        self.apply_move(board, (hit_path[0][0], hit_path[-1][0]))
        for step in hit_path[1:]:
            board.set(game_board.empty, step[1])

    def play(self, board, player):
        hit_list = self.hits(board, player)
        if len(hit_list) > 0:
            for h in hit_list:
                yield h, None
        else:
            moves_list = self.moves(board, player)
            if len(moves_list):
                for m in moves_list:
                    yield None, m
            else:
                raise StopIteration()

    def modify_board(self, board, h, m):
        b0 = board.clone()
        if h is not None:
            self.apply_hit(b0, h)
        elif m is not None:
            self.apply_move(b0, m)
        return b0