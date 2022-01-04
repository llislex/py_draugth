import wx
import threading
import game_board
import game_rules
import random
import copy
import time
import game_ai_player


def col_index(n, size):
    return (n - 1) % (size // 2)


def row(n, size):
    return (n - 1) // (size // 2)


def col(n, size):
    return col_index(n, size) * 2 + 1 - (row(n, size) % 2)


_hit = 1
_move = 0

_human = 0
_ai = 1

_black_move = False
_white_move = True


class MainForm(wx.Frame):
    def __init__(self, board, rules):
        wx.Frame.__init__(self, None, size=(400, 400))
        menu_bar = wx.MenuBar()
        menu = wx.Menu()
        menu_item = wx.MenuItem(menu, wx.ID_NEW, "New game", "Start a new game")
        menu.Append(menu_item)
        menu_bar.Append(menu, '&Game')
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.start_new_game, menu_item)

        self.num_buttons = game_board._N
        self.btn = []
        self.selected_btn = []
        self.move_type = _hit  # 0 - move 1 - hit
        self.move_list = []
        self.step = 0
        sz = self.GetSize()
        h = 3 * sz[0] // N // 4
        w = 3 * sz[1] // N // 4

        for i in range(0, self.num_buttons):
            x = col(i + 1, N) * w
            y = row(i + 1, N) * h
            btn = wx.Button(self, pos=(x, y), size=(w, h))
            btn.SetFont(btn.GetFont().MakeLarger().MakeLarger())
            self.btn.append(btn)

        self.current_turn = _white_move
        self.white_player = _human
        self.black_player = _human
        self.board = board
        self.rules = rules
        self.start_new_game(None)
        # self.set_board(board, rules, player)

    def player(self):
        return self.white_player if self.current_turn == _white_move else self.black_player

    def start_new_game(self, evt):
        self.Bind(EVT_MOVE, self.on_ai_move)
        self.current_turn = _white_move
        self.white_player = _human
        self.black_player = _ai
        self.board.initial()
        self.set_board(self.board, self.rules, self.current_turn)

    def set_board(self, board, rules, turn):
        for i in range(0, self.num_buttons):
            if board.empty(i):
                self.btn[i].SetLabel(' ')
            else:
                self.btn[i].SetLabel(board.dot(i))
        # build move list for the board
        if self.player() == _human:
            self.move_list = rules.move_list(board, turn)
            self.init_filter()
        else:
            ai_thread = AI(self, self.board, self.rules, self.current_turn)
            ai_thread.start()

    def _bind_button(self, btn):
        if btn not in self.selected_btn:
            self.selected_btn.append(btn)
            btn.Bind(wx.EVT_BUTTON, self.on_button_click)

    def _unbind_buttons(self):
        for btn in self.selected_btn:
            btn.Unbind(wx.EVT_BUTTON)
        self.selected_btn = []

    def _move_place(self, move):
        if self.step == 0:
            return game_rules._from_str(move[-1])
        else:
            return game_rules._from_str(move[-self.step * 2])

    def init_filter(self):
        self.step = 0
        self.selected_btn = []
        for move in self.move_list:
            button = self.btn[self._move_place(move)]
            self._bind_button(button)

    def set_filter(self, point):
        new_list = []
        for move in self.move_list:
            if len(move) > self.step:
                if self._move_place(move) == point:
                    new_list.append(move)
        self.move_list = new_list
        self.step += 1
        self._unbind_buttons()
        if not self.done():
            for move in self.move_list:
                if len(move) > self.step:
                    num = self._move_place(move)
                    self._bind_button(self.btn[num])

    def done(self):
        return len(self.move_list) == 1 or len(self.move_list) == 0

    def on_button_click(self, evt):
        target = evt.GetEventObject()
        n = self.btn.index(target)
        self.set_filter(n)
        if self.done():
            self._make_move(self.move_list[0])

    def _make_move(self, a_move):
        self.rules.apply(self.board, a_move)
        self.current_turn = not self.current_turn
        self.set_board(self.board, self.rules, self.current_turn)

    def on_ai_move(self, evt):
        #"ai move"
        a_move = evt.GetValue()
        self._make_move(a_move)


class MoveEvent(wx.PyCommandEvent):
    def __init__(self, value=None):
        wx.PyCommandEvent.__init__(self, EVT_MOVE_TYPE, -1)
        self._value = value

    def GetValue(self):
        return self._value


'''
class AI0(threading.Thread):
    def __init__(self, parent, board, rules, turn):
        threading.Thread.__init__(self)
        self.parent = parent
        self.board = board
        self.rules = rules
        self.turn = turn

    def run(self):
        # dumb player
        move_list = self.rules.move_list(self.board, self.turn)
        if len(move_list) > 0:
            time.sleep(1)
            a_move = random.choice(move_list)
            evt = MoveEvent(a_move)
            wx.PostEvent(self.parent, evt)
        else:
            # resign
            pass


def nodes(root):
    if root is not None:
        r = 1
        for c in root.child:
            r += nodes(c)
        return r
    else:
        return 0
'''


class GameTreeBuilder(threading.Thread):
    def __init__(self, move, board, rules, turn, depth):
        threading.Thread.__init__(self)
        self.depth = depth
        self.board = board
        self.move = move
        self.rules = rules
        self.turn = turn
        self.tooktime = 0
        self.evaluation = 0

    def run(self):
        start = time.time()
        alpha = -game_ai_player.max_value
        beta = game_ai_player.max_value
        self.evaluation = game_ai_player.negamax(self.board, self.rules, self.turn, self.depth, alpha, beta)
        end = time.time()
        self.tooktime = end - start


class AI(threading.Thread):
    def __init__(self, parent, board, rules, turn):
        threading.Thread.__init__(self)
        self.parent = parent
        self.board = board
        self.rules = rules
        self.turn = turn
        random.seed()

    def run(self):
        threads = []
        depth = 9
        t0 = time.time()
        moves = self.rules.move_list(self.board, self.turn)
        if len(moves) > 1:
            for mx in moves:
                bx = copy.deepcopy(b) #b.clone()
                self.rules.apply(bx, mx)
                tx = GameTreeBuilder(mx, bx, self.rules, not self.turn, depth - 1)
                threads.append(tx)
                tx.start()
            for tx in threads:
                tx.join()
            t1 = time.time()
            if len(threads) > 0:
                e = max(threads, key=lambda item: item.evaluation) if self.turn else min(threads, key=lambda item: item.evaluation)
                for tx in threads:
                    print(tx.board)
                    print("eval ", tx.evaluation, "move ", tx.move)
                print(e.evaluation)
                best_move_threads = list(filter(lambda x: x.evaluation == e.evaluation, threads))
                best_tx = random.choice(best_move_threads)

                evt = MoveEvent(best_tx.move)
                wx.PostEvent(self.parent, evt)
                print("build tree", t1 - t0, "depth", depth)
            else:
                # resign
                pass
        elif len(moves) == 1:
            evt = MoveEvent(moves[0])
            wx.PostEvent(self.parent, evt)
        else:
            pass


N = game_board._n
b = game_board.Board()
r = game_rules.Rules(N)

EVT_MOVE_TYPE = wx.NewEventType()
EVT_MOVE = wx.PyEventBinder(EVT_MOVE_TYPE, 1)
app = wx.App()

form = MainForm(b, r)
form.Show()

app.MainLoop()
