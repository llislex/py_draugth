import re

_n = 8         # sqrt(_N*2)  board size _n * _n
_N = _n * _n // 2  # number of fields on the board ('dots')
_mask = [1 << x for x in range(0, _N)] # bit mask of each dot in the board


def dot_index(_col, _row):
    return (_row * _n + _col) // 2


class Board:
    __slots__ = ['full','black','dam']

    def __init__(self):
        self.full = 0  # bitmap: bit[i] == 1 - a dot not empty, i = 0 .. _N -1
        self.black = 0 # bitmap: bit[i] == 1 - a dot is black
        self.dam = 0   # bitmap: bit[i] == 1 - a dot is dam

    # return dot symbol at specified position "." - empty, o - white, O - white dam, x - black, X - black dam
    def dot(self, n):
        mask = _mask[n]
        if self.full & mask == 0:
            return '.'
        else:
            is_dam = self.dam & mask != 0
            is_black = self.black & mask != 0
            if is_dam:
                return 'X' if is_black else 'O'
            else:
                return 'x' if is_black else 'o'

    def __eq__(self, d):
        return self.full == d.full and self.black == d.black and self.dam == d.dam

    # board as human-readable string
    def __str__(self):
        res = ""
        for r in range(0, _n):
            for c in range(0, _n):
                if (r + c) % 2 == 1:
                    n = dot_index(c, r)
                    res += self.dot(n)
                else:
                    res += ' '
            if r != _n - 1:
                res += '\n'
        return res

        # board as human-readable string

    def debug_print(self):
        res = "b.load("  # dbg
        for r in range(0, _n):
            res += '\"'  # dbg
            for c in range(0, _n):
                if (r + c) % 2 == 1:
                    n = dot_index(c, r)
                    res += self.dot(n)
                else:
                    res += ' '
            res += '\"'  # dbg
            res += '\n' if r != _n - 1 else ')'
            res += "       " if r != _n - 1 else ""  # dbg
        return res

    # board notation human-readable
    @staticmethod
    def notation():
        res = "b.load("  # dbg
        for r in range(0, _n):
            res += '\"'  # dbg
            for c in range(0, _n):
                if (r + c) % 2 == 1:
                    n = dot_index(c, r)
                    res += chr(n + 0x30)
                else:
                    res += ' '
            res += '\"'  # dbg
            res += '\n' if r != _n - 1 else ')'
            res += "       " if r != _n - 1 else "" # dbg
        return res
        
    def initial(self):
        self.clear()
        x = (_N - _n) // 2
        for i in range(0, x):
            b_mask = _mask[i]
            w_mask = _mask[_N - i - 1]
            self.black |= b_mask
            self.full |= b_mask | w_mask

    def load(self, text):
        st = re.sub(r'[^xXoO.]', "", text)
        self.clear()
        assert(len(st) == _N)
        for i in range(0, len(st)):
            if st[i] != '.':
                mask = _mask[i]
                self.full |= mask
                if st[i] == 'O' or st[i] == 'X':
                    self.dam |= mask
                if st[i] == 'X' or st[i] == 'x':
                    self.black |= mask 

    def is_dam(self, n):
        return self.dam & _mask[n] != 0
        
    def is_black(self, n):
        return self.black & _mask[n] != 0

    def empty(self, n):
        return self.full & _mask[n] == 0        

    def clear(self):
        self.full = 0
        self.dam = 0
        self.black = 0

    def set(self, n, _white, _dam):
        m = _mask[n] 
        self.full |= m
        if _white:
            self.black &= ~m
        else:
            self.black |= m
        if _dam:
            self.dam |= m
        else:
            self.dam &= ~m
        
    def set_empty(self, n):
        self.full &= ~_mask[n]

    def owned_by(self, white_player, n):
        m = _mask[n]
        if self.full & m == 0:
            return False
        if white_player:
            return self.black & m == 0
        else:
            return self.black & m != 0

    # side - white == True or black == False
    def units(self, side):
        for i in range(0, _N):
            if self.owned_by(side, i):
                yield i

    def clone(self):
        b = Board()
        b.full = self.full
        b.dam = self.dam
        b.black = self.black
        return b