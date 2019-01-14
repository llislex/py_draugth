import re

# state
empty = 0
white = 1
white_dam = 2
black = -1
black_dam = -2


class Board:
    def __init__(self, size):
        self._d = size / 2
        self._D = size
        self.dot = [empty] * (self._D * self._d + 1)
        self.marker = []

    # temporary
    def number(self, _col, _row):
        i = _col / 2
        return _row * self._d + i + 1

    def __str__(self):
        res = ''
        lut = {white: 'o', white_dam: 'O', black: 'x', black_dam: 'X', empty: '.'}
        for r in xrange(0, self._D):
            res += '\n'
            for c in xrange(0, self._D):
                if (r + c) % 2 == 1:
                    num = self.number(c, r)
                    if num in self.marker:
                        res += str(self.marker.index(num))
                    else:
                        res += lut[self.dot[self.number(c, r)]]
                else:
                    res += ' '
        return res

    def load(self, text):
        st = re.sub(r'[^xXoO.]', "", text)
        dictionary = {'x': black, 'X': black_dam, 'o': white, 'O': white_dam, '.': empty}
        self.clear()
        for i in xrange(0, len(st)):
            self.dot[i+1] = dictionary[st[i]]

    def dam(self, n):
        return self.dot[n] == white_dam or self.dot[n] == black_dam

    def clear(self):
        for n in xrange(1, self._d * self._D + 1):
            self.dot[n] = empty

    def remove_black(self, n):
        self.dot[n] = empty

    def remove_white(self, n):
        self.dot[n] = empty

    def set(self, state, n):
        self.dot[n] = state

    def empty(self, n):
        return self.dot[n] == empty

    def owned_by(self, player, n):
        return self.dot[n] * player > 0

    def units(self, player):
        for i in xrange(1, len(self.dot)):
            if self.owned_by(player, i):
                yield i
        raise StopIteration()
