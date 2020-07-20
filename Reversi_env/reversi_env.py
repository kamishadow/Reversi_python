import random
import tkinter as tk
import tkinter.messagebox

from stupidai import StupidAI, SmartHuman


class CB:
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


# def print_cb(cb):
#     rows, cols = len(cb), len(cb[0])
#     print('------------------------')
#     print('  A B C D E F G H')
#     for i in range(rows):
#         print(i, end='')
#         for j in range(cols):
#             if cb[i][j] == CB.EMPTY:
#                 print('  ', end='')
#             elif cb[i][j] == CB.BLACK:
#                 print(' *', end='')
#             elif cb[i][j] == CB.WHITE:
#                 print(' -', end='')
#         print('')
#     print('')


class Reversi:
    nickname = 'Reversi'
    rows = 4
    cols = 4
    player_black = None
    player_white = None

    def __init__(self, player_black=None, player_white=None):
        # print('Reversi console')
        self.__cb = [[0]*self.cols for _ in range(self.rows)]
        # self.__cb[3][4] = self.__cb[4][3] = CB.BLACK
        # self.__cb[3][3] = self.__cb[4][4] = CB.WHITE
        self.__cb[1][2] = self.__cb[2][1] = CB.BLACK
        self.__cb[1][1] = self.__cb[2][2] = CB.WHITE
        self.__turn = CB.BLACK

        self.player_black = player_black
        self.player_white = player_white

    def get_cb(self):
        return self.__cb

    def get_turn(self):
        return self.__turn

    def chg_turn(self):
        self.__turn = CB.WHITE if self.__turn == CB.BLACK else CB.BLACK

    def get_score(self, cb=None):
        cb = cb if cb else self.__cb
        score_black = sum([c.count(CB.BLACK) for c in cb])
        score_white = sum([c.count(CB.WHITE) for c in cb])
        return (score_black, score_white)

    def press_chess(self, pos, cb=None, turn=None, upd=True):
        # return False if not success
        # return new cb if success
        assert(not (upd and (cb or turn)))
        cb = [c.copy() for c in cb] if cb else \
            [c.copy() for c in self.__cb]  # deepcopy #do not cb=self.__cb
        turn = turn if turn else self.__turn

        x, y = pos
        rows, cols = len(cb), len(cb[0])
        # print('press', x, y)
        if cb[x][y] == CB.EMPTY:
            sw = {
                -1: {-1: min(x, y), 0: x, 1: min(x, cols-1-y)},
                0: {-1: y, 1: cols-1-y},
                1: {-1: min(rows-1-x, y), 0: rows-1-x, 1: min(rows-1-x, cols-1-y)}
            }

            def upd_8dirs(x_dir, y_dir):
                for i in range(1, sw[x_dir][y_dir]+1):
                    if cb[x+x_dir*i][y+y_dir*i] == CB.EMPTY:
                        break
                    elif cb[x+x_dir*i][y+y_dir*i] == turn:
                        for j in range(1, i):
                            cb[x+x_dir*j][y+y_dir*j] = turn
                        break

            upd_8dirs(-1, 0)  # up
            upd_8dirs(1, 0)  # dowm
            upd_8dirs(0, -1)  # left
            upd_8dirs(0, 1)  # right
            upd_8dirs(-1, -1)  # left upper
            upd_8dirs(-1, 1)  # right upper
            upd_8dirs(1, -1)  # left lower
            upd_8dirs(1, 1)  # right upper

            if self.__cb == cb:
                return []
            else:
                cb[x][y] = turn
                if upd:
                    # self.set_cb(_cb)
                    self.__cb = cb
                return cb

        elif cb[x][y] == CB.BLACK:
            print('already black')
            return False
        elif cb[x][y] == CB.WHITE:
            print('already white')
            return False

    def get_hint(self, cb=None, turn=None):
        cb = cb if cb else self.__cb
        turn = turn if turn else self.__turn
        pos_list = []
        cb_list = []
        score_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if cb[i][j] == CB.EMPTY:
                    p_cb = self.press_chess(
                        (i, j), cb=cb, turn=turn, upd=False)
                    if p_cb:
                        pos_list.append((i, j))
                        cb_list.append(p_cb)
                        score_list.append(self.get_score(cb=p_cb))
        return pos_list, cb_list, score_list

    def __round_counter(self):
        isgameover = 0
        while isgameover < 2:
            pos_list, _, _ = self.get_hint()
            if len(pos_list) > 0:
                isgameover = 0
                if self.__turn == CB.BLACK:
                    while True:
                        pos = self.player_black.round_callback()
                        if pos in pos_list:
                            self.press_chess(pos)
                            break
                elif self.__turn == CB.WHITE:
                    while True:
                        pos = self.player_white.round_callback()
                        if pos in pos_list:
                            self.press_chess(pos)
                            break
            else:
                isgameover += 1
            self.__turn = CB.WHITE if self.__turn == CB.BLACK else CB.BLACK
        self._gameover()

    def _gameover(self):
        b, w = self.get_score()
        if b > w:
            info = self.player_black.nickname + ' Black win!'
        elif b == w:
            info = 'Draw!'
        elif b < w:
            info = self.player_white.nickname + ' White win!'
        print('GAMEOVER!', info)
        self.player_black.gameover_callback()
        self.player_white.gameover_callback()
        return info

    def run(self):
        # print('%s V.S. %s' %
        #       (self.player_black.nickname, self.player_white.nickname))
        assert((self.player_black and self.player_white)
               or not (self.player_black or self.player_white))
        if self.player_black and self.player_white:
            self.player_black = self.player_black(self, CB.BLACK)
            self.player_white = self.player_white(self, CB.WHITE)
        else:
            self.player_black = SmartHuman(self, CB.BLACK)
            self.player_white = SmartHuman(self, CB.WHITE)
        self.__round_counter()

    def print_cb(self, cb=None):
        cb = cb if cb else self.__cb
        print('------------------------')
        print(' '.join([' ']+[chr(ord('A')+i) for i in range(self.cols)]))
        for i in range(self.rows):
            print(str(i)+' '+' '.join([str(j) for j in cb[i]]
                                      ).replace('0', ' ').replace('1', '*').replace('2', '-'))


class ReversiGUI(Reversi):
    nickname = 'ReversiGUI'
    delay_time = 1000
    gap = 3
    boxwidth = 47
    borden = 5

    def __init__(self, player_black=None, player_white=None):
        super(ReversiGUI, self).__init__(
            player_black=player_black, player_white=player_white)

    def __page_index(self):
        def single_player():
            page_index.destroy()
            self.player_black = SmartHuman(self, CB.BLACK)
            self.player_white = StupidAI(self, CB.WHITE)
            self.__page_play()

        def multi_player():
            page_index.destroy()
            self.player_black = SmartHuman(self, CB.BLACK)
            self.player_white = SmartHuman(self, CB.WHITE)
            self.__page_play()

        def page_index_help():
            tk.messagebox.showinfo('Rule', RULE)

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
            for i in range(self.rows):
                if (i+1)*self.gap + i*self.boxwidth < event.y < (i+1)*self.gap + (i+1)*self.boxwidth:
                    for j in range(self.cols):
                        if (j+1)*self.gap + j*self.boxwidth < event.x < (j+1)*self.gap + (j+1)*self.boxwidth:
                            self.mpos = (i, j)
                            # print('i press', self.mpos)
                            return True
                        elif event.x < (j+1)*self.gap + j*self.boxwidth:
                            return False
                elif event.y < (i+1)*self.gap + i*self.boxwidth:
                    return False
            return False

        def printchessboard():
            play_score_text.set("%d : %d" % (self.get_score()))
            play_whoturn_label_text.set(('Black ('+self.player_black.nickname+')')
                                        if self.get_turn() == CB.BLACK else ('White ('+self.player_white.nickname+')'))

            cb = self.get_cb()
            for i in range(self.rows):
                for j in range(self.cols):
                    coord = ((j+1)*self.gap + j*self.boxwidth, (i+1)*self.gap + i*self.boxwidth,
                             (j+1)*self.gap + (j+1)*self.boxwidth, (i+1)*self.gap + (i+1)*self.boxwidth)
                    cv.create_rectangle(coord, fill='#15ab25', width=0)
                    if cb[i][j] == CB.BLACK:
                        bbox = ((j+1)*self.gap + j*self.boxwidth + self.borden, (i+1)*self.gap + i*self.boxwidth + self.borden,
                                (j+1)*self.gap + (j+1)*self.boxwidth - self.borden, (i+1)*self.gap + (i+1)*self.boxwidth - self.borden)
                        cv.create_oval(bbox, fill="black", width=0)
                    elif cb[i][j] == CB.WHITE:
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

    def _gameover(self):
        info = super()._gameover()
        res = tkinter.messagebox.askyesno('ReversiGUI', 'GAME OVER!\n'+info)
        # exit(0)
        self.win.destroy()

    def __round_counter(self):
        isgameover = 0
        isroundend = False
        r_after_id = None

        def round_loop():
            nonlocal isgameover, isroundend
            if isgameover < 2:
                pos_list, _, _ = self.get_hint()
                if len(pos_list) > 0:
                    isgameover = 0
                    turn = self.get_turn()
                    if turn == CB.BLACK:
                        def round_black_loop():
                            nonlocal isroundend
                            pos = self.player_black.round_callback()
                            if pos in pos_list:
                                self.press_chess(pos)
                                isroundend = True
                            else:
                                self.win.after(self.delay_time,
                                               round_black_loop)
                        round_black_loop()
                    elif turn == CB.WHITE:
                        def round_white_loop():
                            nonlocal isroundend
                            pos = self.player_white.round_callback()
                            if pos in pos_list:
                                self.press_chess(pos)
                                isroundend = True
                            else:
                                self.win.after(self.delay_time,
                                               round_white_loop)
                        round_white_loop()
                else:
                    isgameover += 1
                    isroundend = True
            else:
                self._gameover()
                self.win.after_cancel(r_after_id)

        def r():
            nonlocal isroundend, r_after_id
            if isroundend:
                isroundend = False
                self.chg_turn()
                self.mpos = None
                self.upd_cb_gui()
                self.win.after(self.delay_time, round_loop)
            r_after_id = self.win.after(self.delay_time, r)

        # round_loop()
        self.win.after(self.delay_time, round_loop)
        r()

    def run(self):
        self.win = tk.Tk()
        self.win.title('Reversi')
        # self.win.geometry("500x500+100+100")
        self.win.geometry("%dx%d+600+300" % (self.cols*self.boxwidth + (self.cols-1)*self.gap+50,
                                             self.rows*self.boxwidth + (self.rows-1)*self.gap+100))
        # self.win.resizable(False, False)
        self.upd_cb_gui = None
        self.mpos = None

        assert((self.player_black and self.player_white)
               or not (self.player_black or self.player_white))
        if self.player_black and self.player_white:
            self.player_black = self.player_black(self, CB.BLACK)
            self.player_white = self.player_white(self, CB.WHITE)
            self.__page_play()
        else:
            self.__page_index()

        self.win.mainloop()


if __name__ == "__main__":
    # Reversi(StupidAI, StupidAI).run()
    Reversi(SmartHuman, StupidAI).run()
    # Reversi(SmartHuman, SmartHuman).run()

    # ReversiGUI().run()
    # ReversiGUI(StupidAI, StupidAI).run()
    # ReversiGUI(SmartHuman, StupidAI).run()
    # ReversiGUI(SmartHuman, SmartHuman).run()
