import wx
import threading
import game_board
import game_rules
import random
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
        "ai move"
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
    def __init__(self, board, rules, turn, m0, depth):
        threading.Thread.__init__(self)
        self.depth = depth
        self.board = board
        self.rules = rules
        self.turn = turn
        self.tree = m0
        self.tooktime = 0

    def run(self):
        start = time.time()
        self.tree = game_ai_player.build_game_tree(self.tree, 2, self.board, self.rules, self.turn, self.depth)
        end = time.time()
        self.tooktime = end - start


class AI(threading.Thread):
    def __init__(self, parent, board, rules, turn):
        threading.Thread.__init__(self)
        self.parent = parent
        self.board = board
        self.rules = rules
        self.turn = turn

    def run(self):
        threads = []
        game_tree = '0 x 0\n'
        depth = 4
        t0 = time.time()
        for mx in self.rules.play(self.board, self.turn):
            bx = b.clone()
            self.rules.apply(bx, mx)
            a_move = game_ai_player.move_to_str(mx, 1, -game_ai_player.max_value) + '\n'
            tx = GameTreeBuilder(bx, self.rules, not self.turn, a_move, depth - 1)
            threads.append(tx)
            tx.start()
        for tx in threads:
            tx.join()
            game_tree += tx.tree
        t1 = time.time()
        game_tree_lines = game_tree.splitlines()
        n = game_ai_player.TextNode(game_tree_lines, 0)
        r, move_list = game_ai_player.maxi(n) if self.turn else game_ai_player.mini(n)
        t2 = time.time()
        for m in move_list:
            node = game_ai_player.TextNode(game_tree_lines, m)

        print("minimax", t2 - t1, "build tree", t1 - t0)
        print("total", t2 - t0)

        if len(move_list) > 0:
            index = random.choice(move_list)
            node = game_ai_player.TextNode(game_tree_lines, index)
            evt = MoveEvent(node.move)
            wx.PostEvent(self.parent, evt)
        else:
            # resign
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
