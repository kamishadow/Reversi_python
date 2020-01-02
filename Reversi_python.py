__author__ = "Kami"
__copyright__ = "Kami 2020"
__version__ = "2.0.0"
__license__ = "WTFPL"


# import tkinter.ttk as ttk
import random
import tkinter as tk
import tkinter.messagebox
from enum import IntEnum, unique


@unique
class CB(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


RULE = u'''棋规
1．棋局开始时黑棋位于e4和d5，白棋位于d4和e5。
2．黑方先行，双方交替下棋。
3．一步合法的棋步包括：在一个空格新落下一个棋子，并且翻转对手一个或多个棋子。
4．新落下的棋子与棋盘上已有的同色棋子间，对方被夹住的所有棋子都要翻转过来。可以是横着夹，竖着夹，或是斜着夹。夹住的位置上必须全部是对手的棋子，不能有空格。
5．一步棋可以在数个方向上翻棋，任何被夹住的棋子都必须被翻转过来，棋手无权选择不去翻某个棋子。
6．除非至少翻转了对手的一个棋子，否则就不能落子。如果一方没有合法棋步，也就是说不管他下到哪里，都不能至少翻转对手的一个棋子，那他这一轮只能弃权，而由他的对手继续落子直到他有合法棋步可下。
7．如果一方至少有一步合法棋步可下，他就必须落子，不得弃权。
8．棋局持续下去，直到棋盘填满或者双方都无合法棋步可下。'''


def print_cb(cb):
    rows, cols = len(cb), len(cb[0])
    print('------------------------')
    print('  A B C D E F G H')
    for i in range(rows):
        print(i, end='')
        for j in range(cols):
            if cb[i][j] == CB.EMPTY:
                print('  ', end='')
            elif cb[i][j] == CB.BLACK:
                print(' *', end='')
            elif cb[i][j] == CB.WHITE:
                print(' -', end='')
        print('')
    print('')


class Reversi:
    def __init__(self, player_black_classname, player_white_classname):
        print('Reversi console')
        self.cb = [[0]*8 for _ in range(8)]
        self.cb[3][4] = self.cb[4][3] = CB.BLACK
        self.cb[3][3] = self.cb[4][4] = CB.WHITE
        # self.cb [0][0] = 1
        # self.cb [0][1] = 2

        # self.cb [3][0] = 2
        # self.cb [3][1] = 1
        self.turn = CB.BLACK

        self.player_black_classname = player_black_classname
        self.player_white_classname = player_white_classname

    def get_cb(self):
        return self.cb

    def __set_cb(self, cb):
        self.cb = cb

    def get_turn(self):
        return self.turn

    def __set_turn(self, turn):
        self.turn = turn

    def calc_score(self, cb=None):
        cb = cb if cb else self.cb
        score_black = sum([_.count(CB.BLACK) for _ in cb])
        score_white = sum([_.count(CB.WHITE) for _ in cb])
        return score_black, score_white

    def press_chess(self, pos, cb=None, turn=None, upd=True):
        # return False if not success
        # return new cb if success
        assert(not (upd and (cb or turn)))
        cb = cb if cb else self.cb
        turn = turn if turn else self.turn

        x, y = pos
        rows, cols = len(cb), len(cb[0])
        # print('press', x, y)
        if cb[x][y] == CB.EMPTY:
            # deepcopy
            _cb = [_.copy() for _ in cb]

            def upd_8dirs(x_dir, y_dir):
                sw = {
                    -1: {-1: min(x, y), 0: x, 1: min(x, cols-1-y)},
                    0: {-1: y, 1: cols-1-y},
                    1: {-1: min(rows-1-x, y), 0: rows-1-x, 1: min(rows-1-x, cols-1-y)}
                }
                for i in range(1, sw[x_dir][y_dir]+1):
                    if _cb[x+x_dir*i][y+y_dir*i] == CB.EMPTY:
                        break
                    elif _cb[x+x_dir*i][y+y_dir*i] == turn:
                        for j in range(1, i):
                            _cb[x+x_dir*j][y+y_dir*j] = turn
                        break

            upd_8dirs(-1, 0)  # up
            upd_8dirs(1, 0)  # dowm
            upd_8dirs(0, -1)  # left
            upd_8dirs(0, 1)  # right
            upd_8dirs(-1, -1)  # left upper
            upd_8dirs(-1, 1)  # right upper
            upd_8dirs(1, -1)  # left lower
            upd_8dirs(1, 1)  # right upper

            if cb == _cb:
                return []
            else:
                _cb[x][y] = turn
                if upd:
                    # self.set_cb(_cb)
                    self.cb = _cb
                return _cb

        elif self.cb[x][y] == CB.BLACK:
            print('already black')
            return
        elif self.cb[x][y] == CB.WHITE:
            print('already white')
            return

    def whoami(self):
        print('whoami')

    def __is_gameover(self):
        def gameover():
            b, w = self.calc_score(self.cb)
            if b > w:
                print('Black Win')
            elif b == w:
                print('Draw')
            else:
                print('White Win')
            exit(0)

        if sum([_.count(CB.EMPTY) for _ in self.cb]) == 0:
            gameover()
        else:
            # 不能下的交换棋权（外面会换）
            if self._is_end:
                gameover()
            else:
                # self.turn = CB.WHITE if self.turn == CB.BLACK else CB.BLACK
                self._is_end = True

    def __round_counter(self):
        while True:
            print_cb(self.get_cb())
            if self.turn == CB.BLACK:
                if self.player_black.round_callback():
                    self._is_end = False
                else:
                    self.__is_gameover()
            elif self.turn == CB.WHITE:
                if self.player_white.round_callback():
                    self._is_end = False
                else:
                    self.__is_gameover()

            self.turn = CB.WHITE if self.turn == CB.BLACK else CB.BLACK

    def run(self):
        self.player_black = self.player_black_classname(self, CB.BLACK)
        self.player_white = self.player_black_classname(self, CB.WHITE)
        print('%s V.S. %s' %
              (self.player_black.nickname, self.player_white.nickname))

        self.__round_counter()


"""
A simaple of AI.
StupidAI(api, turn)
you can use:
    api.get_cb()
    api.get_turn()
    api.calc_score(self, cb=None)
    api.press_chess(self, pos, cb=None, turn=None, upd=True)
you must implementation function:
    round_callback()

Have fun
OHHHHHHHHHHHHHHH
"""


class StupidAI:
    nickname = 'StupidAI'

    def __init__(self, api, turn):
        self.api = api
        self.turn = turn
        cb = self.api.get_cb()
        self.rows, self.cols = len(cb), len(cb[0])

    def whoami(self):
        print('i am StupidAI')

    def round_callback(self):
        # choose the best
        mylist = []
        myscore = []
        cb = self.api.get_cb()
        for i in range(self.rows):
            for j in range(self.cols):
                if cb[i][j] == CB.EMPTY:
                    p_cb = self.api.press_chess((i, j), upd=False)
                    if p_cb:
                        a, b = self.api.calc_score(p_cb)
                        p_score = a if self.turn == CB.BLACK else b
                        mylist.append((i, j))
                        myscore.append(p_score)

        if myscore:
            # random choice a best one
            loc = [_ for _ in range(len(myscore))
                   if myscore[_] == max(myscore)]
            pos = mylist[random.choice(loc)]
            # TODO
            # pos = mylist[myscore.index(max(myscore))]
            print('stupidAI', self.turn, pos)
            self.api.press_chess(pos)
            return True
        else:
            print('stupidAI', self.turn, 'GIVEUP')
            return False


class ReversiGUI(Reversi):
    nickname = 'Idiot'
    delay_time = 1000

    def __init__(self):
        # init cb turn
        super().__init__(None, None)

        # None means myturn
        self.player_black = None
        self.player_white = None
        self.myturn = False

        self.rows, self.cols = len(self.cb), len(self.cb[0])
        self.gap = 3
        self.boxwidth = 47
        self.borden = 5

        self.win = tk.Tk()
        self.win.title('Reversi')
        self.win.geometry("500x500+100+100")
        self.win.resizable(False, False)

        self.__page_index()
        self.win.mainloop()

    def __page_index(self):
        def single_player():
            page_index.destroy()
            self.player_white = StupidAI(self, CB.WHITE)
            # self.player_black = StupidAI(self, CB.BLACK)
            self.__page_play()

        def multi_player():
            page_index.destroy()
            self.player_white = StupidAI(self, CB.WHITE)
            self.player_black = StupidAI(self, CB.BLACK)
            self.__page_play()

        def page_index_help():
            tk.messagebox.showinfo('Rule', RULE)
            # import webbrowser
            # webbrowser.open(
            #     'https://baike.baidu.com/item/%E9%BB%91%E7%99%BD%E6%A3%8B/80689')

        page_index = tk.Frame(self.win, bg='#15ab25')
        tk.Label(page_index, text='Reversi', background='#15ab25',
                 font=("Arial", 30)).pack(pady=100)
        tk.Button(page_index, text="Single Player", background="pink", font=(
            "Arial", 12), width=18, height=2, command=single_player).pack(pady=10)
        tk.Button(page_index, text="Multiplayer", background="pink", font=(
            "Arial", 12), width=18, height=2, command=multi_player).pack(pady=10)
        tk.Button(page_index, text="Help", background="pink", font=(
            "Arial", 12), width=18, height=2, command=page_index_help).pack(pady=10)
        page_index.pack(fill=tk.BOTH, expand=True)

    def __page_play(self):
        page_play = tk.Frame(self.win)
        play_score_text = tk.StringVar()
        play_whoturn_label_text = tk.StringVar()
        cv_height = self.rows*self.boxwidth + (self.rows-1)*self.gap
        cv_width = self.cols*self.boxwidth + (self.cols-1)*self.gap
        cv = tk.Canvas(page_play, background='#23972f',
                       width=cv_width, height=cv_height)

        def onclick(event):
            # Vertical cb.row event.y
            # horizontal cb.col event.x
            # print(f"鼠标左键点击了一次坐标是:x={event.x}y={event.y}")
            if not self.myturn:
                print('not my turn')
                return False
            for i in range(self.rows):
                if (i+1)*self.gap + i*self.boxwidth < event.y < (i+1)*self.gap + (i+1)*self.boxwidth:
                    for j in range(self.cols):
                        if (j+1)*self.gap + j*self.boxwidth < event.x < (j+1)*self.gap + (j+1)*self.boxwidth:
                            if self.press_chess((i, j)):
                                print(self.nickname, '  ', self.turn, (i, j))
                                self.myturn = False
                                self.turn = CB.WHITE if self.turn == CB.BLACK else CB.BLACK
                                self.__round_counter()
                                return True
                            else:
                                return False
                        elif event.x < (j+1)*self.gap + j*self.boxwidth:
                            return False
                elif event.y < (i+1)*self.gap + i*self.boxwidth:
                    return False
            return False

        def printchessboard():
            play_score_text.set("%d:%d" % (self.calc_score(self.cb)))
            t = self.get_turn()
            if t == CB.BLACK:
                play_whoturn_label_text.set('black turn')
            elif t == CB.WHITE:
                play_whoturn_label_text.set('white turn')

            for i in range(self.rows):
                for j in range(self.cols):
                    coord = ((j+1)*self.gap + j*self.boxwidth, (i+1)*self.gap + i*self.boxwidth,
                             (j+1)*self.gap + (j+1)*self.boxwidth, (i+1)*self.gap + (i+1)*self.boxwidth)
                    cv.create_rectangle(coord, fill='#15ab25', width=0)
                    if self.cb[i][j] == CB.BLACK:
                        bbox = ((j+1)*self.gap + j*self.boxwidth + self.borden, (i+1)*self.gap + i*self.boxwidth + self.borden,
                                (j+1)*self.gap + (j+1)*self.boxwidth - self.borden, (i+1)*self.gap + (i+1)*self.boxwidth - self.borden)
                        cv.create_oval(bbox, fill="black", width=0)
                    elif self.cb[i][j] == CB.WHITE:
                        bbox = ((j+1)*self.gap + j*self.boxwidth + self.borden, (i+1)*self.gap + i*self.boxwidth + self.borden,
                                (j+1)*self.gap + (j+1)*self.boxwidth - self.borden, (i+1)*self.gap + (i+1)*self.boxwidth - self.borden)
                        cv.create_oval(bbox, fill="white", width=0)

        cv.pack()
        cv.bind('<Button-1>', onclick)
        self.upd_cb_gui = printchessboard
        self.upd_cb_gui()
        tk.Label(page_play, textvariable=play_whoturn_label_text,
                 background='yellow', font=("Arial", 12), width=15, height=2).pack()
        tk.Label(page_play, textvariable=play_score_text,
                 background='yellow', font=("Arial", 12), width=15, height=2).pack()
        page_play.pack()

        self.__round_counter()

    def __is_gameover(self):
        def gameover():
            b, w = self.calc_score(self.cb)
            if b > w:
                info = 'Black Win'
                print('Black Win')
            elif b == w:
                info = 'Draw'
                print('Draw')
            else:
                info = 'White Win'
                print('White Win')

            res = tkinter.messagebox.askyesno(
                'ReversiGUI', 'GAME OVER!\n'+info)
            exit(0)

        if sum([_.count(CB.EMPTY) for _ in self.cb]) == 0:
            gameover()
        else:
            # 不能下的交换棋权（外面会换）
            if self._is_end:
                gameover()
            else:
                # self.turn = CB.WHITE if self.turn == CB.BLACK else CB.BLACK
                self._is_end = True

    def __round_counter(self):
        self.upd_cb_gui()
        if self.turn == CB.BLACK:
            if not self.player_black:
                self.myturn = True
            else:
                def __q():
                    if self.player_black.round_callback():
                        self._is_end = False
                    else:
                        self.__is_gameover()
                    self.turn = CB.WHITE
                    self.__round_counter()
                self.win.after(self.delay_time, func=__q)
        elif self.turn == CB.WHITE:
            if not self.player_white:
                self.myturn = True
            else:
                def __w():
                    if self.player_white.round_callback():
                        self._is_end = False
                    else:
                        self.__is_gameover()
                    self.turn = CB.BLACK
                    self.__round_counter()
                self.win.after(self.delay_time, func=__w)


if __name__ == "__main__":
    Reversi(StupidAI, StupidAI).run()

    # ReversiGUI()
