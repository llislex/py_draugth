import tree

# board size
_D = 10
_d = 5
# state
_empty = 0
_white = 1
_white_dam = 2
_black = -1
_black_dam = -2
# geometry
vector = [[-1, 1], [1, 1], [-1, -1], [1, -1]]


def color(status):
    if status > 0:
        return 1
    if status < 0:
        return -1
    return 0


def col_index(n):
    return (n - 1) % _d


def row(n):
    return (n - 1) / _d


def col(n):
    return col_index(n) * 2 + 1 - (row(n) % 2)


def number(_col, _row):
    i = _col / 2
    return _row * _d + i + 1


def near(n, direction):
    c = col(n) + vector[direction][0]
    if 0 <= c < _D:
        r = row(n) + vector[direction][1]
        if 0 <= r < _D:
            return number(c, r)


def way(n, direction):
    m = near(n, direction)
    if m:
        return [m] + way(m, direction)
    return []


_way = [[],
        [[6], [7, 12, 18, 23, 29, 34, 40, 45], [], []],
        [[7, 11, 16], [8, 13, 19, 24, 30, 35], [], []],
        [[8, 12, 17, 21, 26], [9, 14, 20, 25], [], []],
        [[9, 13, 18, 22, 27, 31, 36], [10, 15], [], []],
        [[10, 14, 19, 23, 28, 32, 37, 41, 46], [], [], []],
        [[], [11, 17, 22, 28, 33, 39, 44, 50], [], [1]],
        [[11, 16], [12, 18, 23, 29, 34, 40, 45], [1], [2]],
        [[12, 17, 21, 26], [13, 19, 24, 30, 35], [2], [3]],
        [[13, 18, 22, 27, 31, 36], [14, 20, 25], [3], [4]],
        [[14, 19, 23, 28, 32, 37, 41, 46], [15], [4], [5]],
        [[16], [17, 22, 28, 33, 39, 44, 50], [6], [7, 2]],
        [[17, 21, 26], [18, 23, 29, 34, 40, 45], [7, 1], [8, 3]],
        [[18, 22, 27, 31, 36], [19, 24, 30, 35], [8, 2], [9, 4]],
        [[19, 23, 28, 32, 37, 41, 46], [20, 25], [9, 3], [10, 5]],
        [[20, 24, 29, 33, 38, 42, 47], [], [10, 4], []],
        [[], [21, 27, 32, 38, 43, 49], [], [11, 7, 2]],
        [[21, 26], [22, 28, 33, 39, 44, 50], [11, 6], [12, 8, 3]],
        [[22, 27, 31, 36], [23, 29, 34, 40, 45], [12, 7, 1], [13, 9, 4]],
        [[23, 28, 32, 37, 41, 46], [24, 30, 35], [13, 8, 2], [14, 10, 5]],
        [[24, 29, 33, 38, 42, 47], [25], [14, 9, 3], [15]],
        [[26], [27, 32, 38, 43, 49], [16], [17, 12, 8, 3]],
        [[27, 31, 36], [28, 33, 39, 44, 50], [17, 11, 6], [18, 13, 9, 4]],
        [[28, 32, 37, 41, 46], [29, 34, 40, 45], [18, 12, 7, 1], [19, 14, 10, 5]],
        [[29, 33, 38, 42, 47], [30, 35], [19, 13, 8, 2], [20, 15]],
        [[30, 34, 39, 43, 48], [], [20, 14, 9, 3], []],
        [[], [31, 37, 42, 48], [], [21, 17, 12, 8, 3]],
        [[31, 36], [32, 38, 43, 49], [21, 16], [22, 18, 13, 9, 4]],
        [[32, 37, 41, 46], [33, 39, 44, 50], [22, 17, 11, 6], [23, 19, 14, 10, 5]],
        [[33, 38, 42, 47], [34, 40, 45], [23, 18, 12, 7, 1], [24, 20, 15]],
        [[34, 39, 43, 48], [35], [24, 19, 13, 8, 2], [25]],
        [[36], [37, 42, 48], [26], [27, 22, 18, 13, 9, 4]],
        [[37, 41, 46], [38, 43, 49], [27, 21, 16], [28, 23, 19, 14, 10, 5]],
        [[38, 42, 47], [39, 44, 50], [28, 22, 17, 11, 6], [29, 24, 20, 15]],
        [[39, 43, 48], [40, 45], [29, 23, 18, 12, 7, 1], [30, 25]],
        [[40, 44, 49], [], [30, 24, 19, 13, 8, 2], []],
        [[], [41, 47], [], [31, 27, 22, 18, 13, 9, 4]],
        [[41, 46], [42, 48], [31, 26], [32, 28, 23, 19, 14, 10, 5]],
        [[42, 47], [43, 49], [32, 27, 21, 16], [33, 29, 24, 20, 15]],
        [[43, 48], [44, 50], [33, 28, 22, 17, 11, 6], [34, 30, 25]],
        [[44, 49], [45], [34, 29, 23, 18, 12, 7, 1], [35]],
        [[46], [47], [36], [37, 32, 28, 23, 19, 14, 10, 5]],
        [[47], [48], [37, 31, 26], [38, 33, 29, 24, 20, 15]],
        [[48], [49], [38, 32, 27, 21, 16], [39, 34, 30, 25]],
        [[49], [50], [39, 33, 28, 22, 17, 11, 6], [40, 35]],
        [[50], [], [40, 34, 29, 23, 18, 12, 7, 1], []],
        [[], [], [], [41, 37, 32, 28, 23, 19, 14, 10, 5]],
        [[], [], [41, 36], [42, 38, 33, 29, 24, 20, 15]],
        [[], [], [42, 37, 31, 26], [43, 39, 34, 30, 25]],
        [[], [], [43, 38, 32, 27, 21, 16], [44, 40, 35]],
        [[], [], [44, 39, 33, 28, 22, 17, 11, 6], [45]]]


class Move:
    def __init__(self, hit, move):
        self.hit = hit
        self.move = move

    def __str__(self):
        st = ""
        if self.hit:
            for h in self.hit[:-1]:
                st += str(h[0])+"x"
            st += str(self.hit[-1][0])
            return st
        if self.move:
            st = str(self.move[0])+"-"+str(self.move[1])
            return st
        return "x"

    def __repr__(self):
        return self.__str__()


class Board:
    def __init__(self):
        self.dot = [_empty] * (_D * _d + 1)
        self.marker = []

    def __str__(self):
        res = ''
        lut = {_white: 'o', _white_dam: 'O', _black: 'x', _black_dam: 'X', _empty: '.'}
        for r in xrange(0, _D):
            res += '\n'
            for c in xrange(0, _D):
                if (r + c) % 2 == 1:
                    num = number(c, r)
                    if num in self.marker:
                        res += str(self.marker.index(num))
                    else:
                        res += lut[self.dot[number(c, r)]]
                else:
                    res += ' '
        return res

    def dam(self, n):
        return self.dot[n] == _white_dam or self.dot[n] == _black_dam

    def clear(self):
        for n in xrange(1, _d * _D + 1):
            self.dot[n] = _empty

    def remove_black(self, n):
        self.dot[n] = _empty

    def remove_white(self, n):
        self.dot[n] = _empty

    def set(self, state, n):
        self.dot[n] = state

    def set_white(self, w_list):
        for w in w_list:
            self.dot[w] = _white

    def set_white_dam(self, w_list):
        for w in w_list:
            self.dot[w] = _white_dam

    def set_black(self, b_list):
        for b in b_list:
            self.dot[b] = _black

    def set_black_dam(self, b_list):
        for b in b_list:
            self.dot[b] = _black_dam

    def enemies(self, n1, n2):
        s1 = self.dot[n1]
        s2 = self.dot[n2]
        return color(s1) != color(s2) and color(s2) != 0

    def empty(self, n):
        return self.dot[n] == _empty

    def owned_by(self, player, n):
        return self.dot[n] * player > 0

    def hit(self, player, n, direction):
        if len(_way[n][direction]) > 1:
            n1 = _way[n][direction][0]
            n2 = _way[n][direction][1]
            if self.owned_by(player, n1) and self.empty(n2):
                return n2, n1
        return None, None

    def hit_dam(self, player, n, direction):
        for n1 in _way[n][direction][:-1]:
            if self.empty(n1):
                continue
            elif self.owned_by(player, n1):
                res = []
                for n2 in _way[n1][direction]:
                    if self.empty(n2):
                        res.append(n2)
                    else:
                        break
                return res, n1
            else:
                break
        return [], None

    def hit_way(self, player, n, way_point):
        ways = 0
        for direction in [0, 1, 2, 3]:
            h, t = self.hit(player, n, direction)
            if h and tree.search_back(way_point, t, lambda node, v: node.value[1] == v) < 0:
                wp = way_point.append((h, t))
                sub_way = self.hit_way(player, h, wp)
                ways += sub_way + 1
                if sub_way == 0:
                    way_point.owner.value += [wp]
        return ways

    def hit_dam_way(self, player, n, way_point):
        ways = 0
        for direction in [0, 1, 2, 3]:
            hit_list, t = self.hit_dam(player, n, direction)
            if hit_list and tree.search_back(way_point, t, lambda node, v: node.value[1] == v) < 0:
                final_wp = []
                final_iteration = True
                for h in hit_list:
                    ways += 1
                    wp = way_point.append((h, t))
                    num = self.hit_dam_way(player, h, wp)
                    if num == 0:
                        final_wp.append(wp)
                    else:
                        ways += num
                        final_iteration = False
                if final_iteration:
                    way_point.owner.value += final_wp
                else:
                    for wp in final_wp:
                        wp.owner.remove(wp)
                        ways -= 1
        return ways

    @staticmethod
    def majority(way_point):
        if way_point.owner.value:
            max_level = max(node.level for node in way_point.owner.value)
            return filter(lambda n: n.level == max_level, way_point.owner.value)
        return []

    def hits(self, player):
        result = []
        way_point = tree.Tree().append((0, 0))
        way_point.owner.value = []
        for n in xrange(1, len(self.dot)):
            if self.owned_by(player, n):
                wp = way_point.append((n, -1))
                if self.dam(n):
                    self.hit_dam_way(-player, n, wp)
                else:
                    self.hit_way(-player, n, wp)
        for variant in self.majority(way_point):
            hit_path = []
            for step in variant:
                if step.value[0] > 0:
                    hit_path.insert(0, step.value)
            result.append(hit_path)
        return result

    def move(self, n):
        directions = [0, 1] if color(self.dot[n]) < 0 else [2, 3]
        for d in directions:
            if _way[n][d]:
                x = _way[n][d][0]
                if self.dot[x] == _empty:
                    yield x

    def move_dam(self, n):
        for d in [0, 1, 2, 3]:
            for x in _way[n][d]:
                if self.empty(x):
                    yield x
                else:
                    break

    def moves(self, player):
        result = []
        for n in xrange(1, len(self.dot)):
            if self.owned_by(player, n):
                gen = self.move_dam(n) if self.dam(n) else self.move(n)
                for dst in gen:
                    result.append((n, dst))
        return result

    # input m - [ from, to]
    def _apply_move(self, m):
        s = self.dot[m[0]]
        self.set(_empty, m[0])
        if s == _white and m[1] in [1, 2, 3, 4, 5]:
            s = _white_dam
        if s == _black and m[1] in [46, 47, 48, 49, 50]:
            s = _black_dam
        self.set(s, m[1])

    def _apply_hit(self, hit_path):
        self._apply_move((hit_path[0][0], hit_path[-1][0]))
        for step in hit_path[1:]:
            self.set(_empty, step[1])

    # input m - Move class
    def apply_move(self, m):
        if m.hit:
            self._apply_hit(m.hit)
        else:
            self._apply_move(m.move)

    def clone(self, _move=None):
        transformed_board = Board()
        for n in xrange(1, len(self.dot)):
            transformed_board.dot[n] = self.dot[n]
        if _move is not None:
            transformed_board.apply_move(_move)
        return transformed_board

    def play(self, player):
        hits = self.hits(player)
        if hits:
            for h in hits:
                transformed_board = Board()
                for n in xrange(1, len(self.dot)):
                    transformed_board.dot[n] = self.dot[n]
                transformed_board._apply_hit(h)
                yield transformed_board, Move(h, None)
        else:
            moves = self.moves(player)
            if moves:
                for m in moves:
                    transformed_board = Board()
                    for n in xrange(1, len(self.dot)):
                        transformed_board.dot[n] = self.dot[n]
                    transformed_board._apply_move(m)
                    yield transformed_board, Move(None, m)
            else:
                raise StopIteration()
