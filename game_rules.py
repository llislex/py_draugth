_backward = [0, 1]
_forward = [2, 3]
_all_directions = [0, 1, 2, 3]
_vector = [[-1, 1], [1, 1], [-1, -1], [1, -1]]


class BoardGeometry:
    def __init__(self, size):
        self.d = size // 2
        self.D = size
        assert(size >= 4)
        assert(size % 2 == 0)
        
    def fields(self):
        return self.D * self.D // 2

    def col_index(self, n):
        return n % self.d

    def row(self, n):
        return n // self.d

    def col(self, n):
        return self.col_index(n) * 2 + 1 - (self.row(n) % 2)

    def number(self, _col, _row):
        i = _col // 2
        return _row * self.d + i

    def near(self, n, direction):
        c = self.col(n) + _vector[direction][0]
        if 0 <= c < self.D:
            r = self.row(n) + _vector[direction][1]
            if 0 <= r < self.D:
                return self.number(c, r)
        return self.fields()
        
        
def _to_str(n):
    return chr(n + 0x30)


def _from_str(ch):
    return ord(ch) - 0x30        


class Rules:
    def __init__(self, board_size):
        g = BoardGeometry(board_size)
        self.fields = g.fields()
        self.way = []
        for i in range(0, g.fields()):
            self.way.append([g.near(i, 0), g.near(i, 1), g.near(i, 2), g.near(i, 3)])
        self.dam_target_white = [i for i in range(0, g.d)]
        self.dam_target_black = [g.d * g.D - i - 1 for i in range(0, g.d)]
        
    def _valid(self, n):
        return n < self.fields
        
    def _dam_field(self, white_turn, n):
        if white_turn:
            return n in self.dam_target_white
        else:
            return n in self.dam_target_black
        
    def _hit(self, board, player, n, direction):
        n1 = self.way[n][direction]
        if self._valid(n1) and board.owned_by(not player, n1):
            n2 = self.way[n1][direction]
            if self._valid(n2) and board.empty(n2):
                return _to_str(n1) + _to_str(n2)
        return None

    def _dam_hit(self, board, player, n, direction):
        n1 = self.way[n][direction]
        while self._valid(n1) and board.empty(n1):
            n1 = self.way[n1][direction]
        result = []            
        if self._valid(n1) and board.owned_by(not player, n1):
            n2 = self.way[n1][direction]
            while self._valid(n2) and board.empty(n2):
                result.append(_to_str(n1) + _to_str(n2))
                n2 = self.way[n2][direction]
        return result
        
    def _hit_way(self, board, white_turn, n, way):
        res = {}
        dirs = []
        for d in _all_directions:
            r = self._hit(board, white_turn, n, d)
            if r is not None:
                if r[0] not in way:
                    dirs.append(d)
                    res[d] = r
        if len(dirs) == 0:
            yield way
        for d in dirs:
            n1 = _from_str(res[d][1])
            way_generator = self._hit_dam_way if self._dam_field(white_turn, n1) else self._hit_way  # russian rule
            # way_generator = self._hit_way                                         # international rule
            for a_way in way_generator(board, white_turn, n1, way + res[d]):
                yield a_way

    def _hit_dam_way(self, board, white_turn, n, way):
        res = {}
        dirs = []
        for d in _all_directions:
            r = self._dam_hit(board, white_turn, n, d)
            if len(r) > 0:
                if r[0][0] not in way:
                    dirs.append(d)
                    res[d] = r
        if len(dirs) == 0:
            yield way
        for d in dirs:
            sub_ways = []
            final_ways = []
            for r in res[d]:
                n1 = _from_str(r[1])
                for new_way in self._hit_dam_way(board, white_turn, n1, way + r):
                    if len(new_way) == len(way+r):
                        final_ways.append(new_way)
                    else:
                        sub_ways.append(new_way)
            if len(sub_ways) == 0:
                sub_ways = final_ways
            for a_way in sub_ways:
                yield a_way
                
    def hits(self, board, white_turn):
        for i in board.units(white_turn):
            way_gen = self._hit_dam_way if board.is_dam(i) else self._hit_way
            for r in way_gen(board, white_turn, i, ""):
                if len(r) > 0:
                    yield r + _to_str(i)

    def _move(self, board, white_turn, n):
        directions = _forward if white_turn else _backward
        for d in directions:
            x = self.way[n][d]
            if self._valid(x) and board.empty(x):
                yield _to_str(x)

    def _dam_move(self, board, white_turn, n):
        for d in _all_directions:
            x = self.way[n][d]
            while self._valid(x) and board.empty(x):
                yield _to_str(x)
                x = self.way[x][d]

    def moves(self, board, white_turn):
        for i in board.units(white_turn):
            way_gen = self._dam_move if board.is_dam(i) else self._move
            for dest in way_gen(board, white_turn, i):
                yield dest + _to_str(i)

    # input m - [taken_1, move_point_1.. taken_n, move_point_n, move_point_0]
    def apply(self, board, move):
        src = _from_str(move[-1])
        dest = _from_str(move[-2])
        is_dam = board.is_dam(src)
        color = not board.is_black(src)
        assert(not board.empty(src))
        board.set_empty(src)
        is_dam |= self._dam_field(color, dest)
        if len(move) > 2:
            assert((len(move) % 2) == 1)
            for i in range(0, (len(move) - 1) // 2):
                x = _from_str(move[i*2])
                board.set_empty(x)  # empty taken units
                # russian dam rules
                y = _from_str(move[i*2+1])
                is_dam |= self._dam_field(color, y)
        board.set(dest, color, is_dam)

    def transformed_board(self, board, move):
        b = board.clone()
        self.apply(b, move)
        return b

    def play(self, board, white_turn):
        no_hit = True
        for m in self.hits(board, white_turn):
            yield m
            no_hit = False
        if no_hit:
            for m in self.moves(board, white_turn):
                yield m        
                
    def move_list(self, board, white_turn):
        move_list = []
        for a_move in self.play(board, white_turn):
            move_list.append(a_move)
        return move_list
