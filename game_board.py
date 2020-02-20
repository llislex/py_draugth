import re

_n = 8         #sqrt(_N*2)
_N = _n * _n // 2
_mask = [1 << x for x in range(0, _N)]

class Board:
    def __init__(self):
        self.full = 0
        self.black = 0
        self.dam = 0

    def dot_index(self, _col, _row):
        return (_row * _n + _col) // 2
        
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

    #human readable
    def __str__(self):
        res = ''
        for r in range(0, _n):
            res += '\n'
            for c in range(0, _n):
                if (r + c) % 2 == 1:
                    n = self.dot_index(c, r)
                    res += self.dot(n)
                else:
                    res += ' '
        #res += '\nfull  '+format(self.full, 'b') +'\ndam   '+format(self.dam, 'b') + '\nblack '+format(self.black, 'b')+'\n'                  
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