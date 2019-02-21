import re

class Board:
    def __init__(self, size):
        self.size = size
        self.dot = ['.'] * (size * size / 2)

    def dot_index(self, _col, _row):
        return (_row * self.size + _col) / 2

    #human readable
    def __str__(self):
        res = ''
        for r in xrange(0, self.size):
            res += '\n'
            for c in xrange(0, self.size):
                if (r + c) % 2 == 1:
                    index = self.dot_index(c, r)
                    res += self.dot[index]
                else:
                    res += ' '
        return res
        
    def notation(self):
        res = ''
        for r in xrange(0, self.size):
            res += '\n'
            for c in xrange(0, self.size):
                if (r + c) % 2 == 1:
                    index = self.dot_index(c, r)
                    res += chr(index + 0x30)
                else:
                    res += ' '
        return res
        
    def initial(self):
        self.clear()
        x = (self.size * self.size / 2 -  self.size) / 2
        for i in xrange(0, x):
            self.dot[i] = 'x'
            self.dot[self.size * self.size / 2 - i - 1] = 'o'

    def load(self, text):
        st = re.sub(r'[^xXoO.]', "", text)
        self.clear()
        assert(len(st) == self.size*self.size/2)
        for i in xrange(0, len(st)):
            self.dot[i] = st[i]

    def save(self):
        res = ''
        for i in xrange(0, self.size * self.size / 2):
            res += self.dot[i]
        return res

    def dam(self, n):
        return self.dot[n] == 'X' or self.dot[n] == 'O'

    def clear(self):
        self.dot = ['.'] * (self.size * self.size / 2)

    def set(self, state, n):
        self.dot[n] = state

    def empty(self, n):
        return self.dot[n] == '.'

    def owned_by(self, turn, n):
        if turn > 0:
            return self.dot[n] == 'o' or self.dot[n] == 'O'
        else:
            return self.dot[n] == 'x' or self.dot[n] == 'X'

    def units(self, side):
        for i in xrange(0, len(self.dot)):
            if self.owned_by(side, i):
                yield i
        raise StopIteration()

    def clone(self):
        b = Board(self.size)
        for n in xrange(0, self.size * self.size / 2):
            b.dot[n] = self.dot[n]
        return b