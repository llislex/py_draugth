import wx
import game_board
import game_rules


def col_index(n, size):
    return (n - 1) % (size / 2)


def row(n, size):
    return (n - 1) / (size / 2)


def col(n, size):
    return col_index(n, size) * 2 + 1 - (row(n, size) % 2)


class MainForm(wx.Frame):
    def __init__(self, board, rules, player):
        wx.Frame.__init__(self, None, pos=(150, 150), size=(350, 350))
        N = board.size()
        self.num_buttons = board.size() * board.size() / 2
        self.btn = []
        self.selected_btn = []
        self.move_list = []
        self.step = 0
        sz = self.GetSize()
        for i in xrange(0, self.num_buttons):
            h = sz[0] / N / 2
            w = sz[1] / N / 2
            x = col(i + 1, N) * w
            y = row(i + 1, N) * h
            btn = wx.Button(self, pos=(x, y), size=(w, h))
            self.btn.append(btn)
        self.set_board(board, rules, player)

    def set_board(self, board, rules, player):
        lut = {game_board.white: 'o', game_board.white_dam: 'O', game_board.black: 'x', game_board.black_dam: 'X',
               game_board.empty: ' '}
        for i in xrange(0, self.num_buttons):
            self.btn[i].SetLabel(lut[board.dot[i+1]])
        # build move list for the board
        self.move_list = rules.hits(board, player)
        if len(self.move_list) == 0:
            self.move_list = rules.moves(board, player)
        #
        self.init_filter()

    def _bind_button(self, btn):
        if btn not in self.selected_btn:
            self.selected_btn.append(btn)
            btn.Bind(wx.EVT_BUTTON, self.on_button_click)

    def _unbind_buttons(self):
        for btn in self.selected_btn:
            print "unbind", self.btn.index(btn)
            btn.Unbind(wx.EVT_BUTTON)
        self.selected_btn = []

    def init_filter(self):
        self.step = 0
        self.selected_btn = []
        for move in self.move_list:
            button = self.btn[move[self.step] - 1]
            self._bind_button(button)

    def set_filter(self, point):
        new_list = []
        for move in self.move_list:
            if len(move) > self.step:
                if move[self.step] == point:
                    new_list.append(move)
        self.move_list = new_list
        self.step += 1
        self._unbind_buttons()
        if not self.done():
            for move in self.move_list:
                if len(move) > self.step:       #TBD redundant?
                    num = move[self.step]
                    self._bind_button(self.btn[num - 1])
                    print "next", num

    def done(self):
        return len(self.move_list) == 1 or len(self.move_list) == 0

    def on_button_click(self, evt):
        target = evt.GetEventObject()
        n = self.btn.index(target) + 1
        print n, self.btn.index(target)
        self.set_filter(n)
        if self.done():
            print "done", self.move_list


N = 8
b = game_board.Board(N)
b.load("""
 . x . .
. . x .
 . . . .
. . . .
 . . . .
. . o .
 . . . .
. o . .
""")
r = game_rules.Rules(N)
player = -1


app = wx.App()

form = MainForm(b, r, player)
form.Show()

app.MainLoop()
