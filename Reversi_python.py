import time
import tkinter as tk
import tkinter.messagebox
from enum import IntEnum, unique

import numpy as np
import webbrowser


@unique
class CB(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class checkerboard:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Reversi')
        self.win.geometry("500x500+100+100")
        self.win.resizable(False, False)

        # checkerboard map config
        cb = np.zeros((8, 8), dtype=np.uint8)
        cb[3][4] = cb[4][3] = CB.BLACK
        cb[3][3] = cb[4][4] = CB.WHITE
        print(cb)

        page_index(self.win, cb)
        self.win.mainloop()


class page_index:
    def __init__(self, win, cb):
        self.win = win
        self.cb = cb
        self._page_index()

    def _page_index(self):
        self.index = tk.Frame(self.win, bg='#15ab25')
        tk.Label(self.index, text='Reversi', background='#15ab25',
                 font=("Arial", 30)).pack(pady=100)
        tk.Button(self.index, text="Single Player", background="pink", font=(
            "Arial", 12), width=18, height=2, command=self.SinglePlayer).pack(pady=10)
        tk.Button(self.index, text="Multiplayer", background="pink", font=(
            "Arial", 12), width=18, height=2, command=self.Multiplayer).pack(pady=10)
        tk.Button(self.index, text="Help", background="pink", font=(
            "Arial", 12), width=18, height=2, command=self.index_help).pack(pady=10)
        self.index.pack(fill=tk.BOTH, expand=True)

    def SinglePlayer(self):
        self.index.destroy()
        page_play(self.win, self.cb, CB.WHITE)

    def Multiplayer(self):
        self.index.destroy()
        page_play(self.win, self.cb, CB.EMPTY)

    def index_help(self):
        # print("当前窗口的宽度为", self.win.winfo_width())
        # print("当前窗口的高度为", self.win.winfo_height())
        webbrowser.open(
            "https://baike.baidu.com/item/%E9%BB%91%E7%99%BD%E6%A3%8B/80689")
        print('fuck')


class page_play:
    rows, cols = 0, 0
    gap = 3
    boxwidth = 47
    borden = 5

    def __init__(self, win, cb, aiturn):
        self.win = win
        self.cb = cb
        page_play.rows, page_play.cols = self.cb.shape
        self.turn = CB.EMPTY
        self.aiturn = aiturn
        # self.win.title('Reversi')
        # self.win.resizable(True, True)
        # self.win.geometry("500x500+100+100")
        self._page_play()

    def _page_play(self):
        self.gameboard1 = tk.Frame(self.win)
        self.printchessboard()

        self.play_whoturn_label_text = tk.StringVar()
        tk.Label(self.gameboard1, textvariable=self.play_whoturn_label_text,
                 background='yellow', font=("Arial", 12), width=15, height=2).pack()

        self.play_socre_text = tk.StringVar()
        self.calc_score(self.cb)
        tk.Label(self.gameboard1, textvariable=self.play_socre_text,
                 background='yellow', font=("Arial", 12), width=15, height=2).pack()

        self.gameboard1.pack()
        self.chg_turn()

    def calc_score(self, _cb, upd=True):
        score_black = np.count_nonzero(_cb == CB.BLACK)
        score_white = np.count_nonzero(_cb == CB.WHITE)
        if upd:
            self.play_socre_text.set("%d:%d" % (np.count_nonzero(
                _cb == CB.BLACK), np.count_nonzero(_cb == CB.WHITE)))
        return score_black, score_white

    def chg_turn(self):
        if self.turn == CB.EMPTY:
            self.turn = CB.BLACK
            self.play_whoturn_label_text.set('black turn')
        elif self.turn == CB.BLACK:
            self.turn = CB.WHITE
            self.play_whoturn_label_text.set('white turn')
        elif self.turn == CB.WHITE:
            self.turn = CB.BLACK
            self.play_whoturn_label_text.set('black turn')

        if self.turn == self.aiturn:
            self.stupidAI()

    def printchessboard(self):
        cv_height = page_play.rows*page_play.boxwidth + \
            (page_play.rows-1)*page_play.gap
        cv_width = page_play.cols*page_play.boxwidth + \
            (page_play.cols-1)*page_play.gap

        self.cv = tk.Canvas(self.gameboard1, background='#23972f',
                            width=cv_width, height=cv_height)
        self.cv.pack()
        self.cv.bind('<Button-1>', self.onclick)

        for i in range(page_play.rows):
            for j in range(page_play.cols):
                coord = ((j+1)*page_play.gap + j*page_play.boxwidth, (i+1)*page_play.gap + i*page_play.boxwidth,
                         (j+1)*page_play.gap + (j+1)*page_play.boxwidth, (i+1)*page_play.gap + (i+1)*page_play.boxwidth)
                self.cv.create_rectangle(coord, fill='#15ab25', width=0)
                if self.cb[i][j] == CB.EMPTY:
                    pass
                elif self.cb[i][j] == CB.BLACK:
                    bbox = ((j+1)*page_play.gap + j*page_play.boxwidth + page_play.borden, (i+1)*page_play.gap + i*page_play.boxwidth + page_play.borden,
                            (j+1)*page_play.gap + (j+1)*page_play.boxwidth - page_play.borden, (i+1)*page_play.gap + (i+1)*page_play.boxwidth - page_play.borden)
                    self.cv.create_oval(bbox, fill="black", width=0)
                elif self.cb[i][j] == CB.WHITE:
                    bbox = ((j+1)*page_play.gap + j*page_play.boxwidth + page_play.borden, (i+1)*page_play.gap + i*page_play.boxwidth + page_play.borden,
                            (j+1)*page_play.gap + (j+1)*page_play.boxwidth - page_play.borden, (i+1)*page_play.gap + (i+1)*page_play.boxwidth - page_play.borden)
                    self.cv.create_oval(bbox, fill="white", width=0)

    def gameover(self):
        str = ('balck' if np.count_nonzero(self.cb == CB.BLACK) >
               np.count_nonzero(self.cb == CB.WHITE) else 'white') + ' win!'
        # shutdown after gameover
        if tkinter.messagebox.showinfo('gameover', str):
            self.win.destroy()

    def printallchess(self):
        for i in range(page_play.rows):
            for j in range(page_play.cols):
                if self.cb[i][j] == CB.EMPTY:
                    pass
                elif self.cb[i][j] == CB.BLACK:
                    bbox = ((j+1)*page_play.gap + j*page_play.boxwidth + page_play.borden, (i+1)*page_play.gap + i*page_play.boxwidth + page_play.borden,
                            (j+1)*page_play.gap + (j+1)*page_play.boxwidth - page_play.borden, (i+1)*page_play.gap + (i+1)*page_play.boxwidth - page_play.borden)
                    self.cv.create_oval(bbox, fill="black", width=0)
                elif self.cb[i][j] == CB.WHITE:
                    bbox = ((j+1)*page_play.gap + j*page_play.boxwidth + page_play.borden, (i+1)*page_play.gap + i*page_play.boxwidth + page_play.borden,
                            (j+1)*page_play.gap + (j+1)*page_play.boxwidth - page_play.borden, (i+1)*page_play.gap + (i+1)*page_play.boxwidth - page_play.borden)
                    self.cv.create_oval(bbox, fill="white", width=0)

    def onclick(self, event):
        # Vertical cb.row event.y
        # horizontal cb.col event.x
        # print(f"鼠标左键点击了一次坐标是:x={event.x}y={event.y}")
        for i in range(page_play.rows):
            if (i+1)*page_play.gap + i*page_play.boxwidth < event.y < (i+1)*page_play.gap + (i+1)*page_play.boxwidth:
                for j in range(page_play.cols):
                    if (j+1)*page_play.gap + j*page_play.boxwidth < event.x < (j+1)*page_play.gap + (j+1)*page_play.boxwidth:
                        self.updchess((i, j))
                        return True
                    elif event.x < (j+1)*page_play.gap + j*page_play.boxwidth:
                        return False
            elif event.y < (i+1)*page_play.gap + i*page_play.boxwidth:
                return False
        return False

    def updchess(self, pos):
        x, y = pos
        # print('press', x, y)
        if self.cb[x][y] == CB.EMPTY:
            # think... hint?
            # TODO emmmmmmmm
            if self.updotherchess(self.cb, pos, self.turn).size:
                pass
            else:
                print('press this is not a good idea')
                return

            self.cb[x][y] = self.turn
            self.printallchess()

        elif self.cb[x][y] == CB.BLACK:
            print('already black')
            return
        elif self.cb[x][y] == CB.WHITE:
            print('already white')
            return

        # update score
        self.calc_score(self.cb)

        pl = self.hint_list(
            self.cb, (CB.BLACK if self.turn == CB.WHITE else CB.WHITE))
        if pl:
            # hint
            print('Hint For ' + ('black: ' if self.turn ==
                                 CB.BLACK else 'white: '), pl)
        else:
            pl = self.hint_list(self.cb, turn=self.turn)
            if not pl:
                self.gameover()

        self.chg_turn()

    def updotherchess(self, _cb, pos, turn, upd=True):
        # pos still 0
        __cb = _cb.copy()
        x, y = pos

        def upd_8dirs(x_dir, y_dir):
            sw = {
                -1: {-1: min(x, y), 0: x, 1: min(x, page_play.cols-1-y)},
                0: {-1: y, 1: page_play.cols-1-y},
                1: {-1: min(page_play.rows-1-x, y), 0: page_play.rows-1-x, 1: min(page_play.rows-1-x, page_play.cols-1-y)}
            }
            for i in range(1, sw[x_dir][y_dir]+1):
                if __cb[x+x_dir*i][y+y_dir*i] == CB.EMPTY:
                    break
                elif __cb[x+x_dir*i][y+y_dir*i] == turn:
                    for j in range(1, i):
                        __cb[x+x_dir*j][y+y_dir*j] = turn
                    break

        upd_8dirs(-1, 0)  # up
        upd_8dirs(1, 0)  # dowm
        upd_8dirs(0, -1)  # left
        upd_8dirs(0, 1)  # right
        upd_8dirs(-1, -1)  # left upper
        upd_8dirs(-1, 1)  # right upper
        upd_8dirs(1, -1)  # left lower
        upd_8dirs(1, 1)  # right upper

        if (__cb == _cb).all():  # same
            return np.array([])
        else:
            if upd:
                self.cb = __cb.copy()
            return __cb.copy()

    def hint_list(self, _cb, turn):
        mylist = []
        for i in range(page_play.rows):
            for j in range(page_play.cols):
                if _cb[i][j] == CB.EMPTY:
                    if self.updotherchess(_cb, (i, j), turn, upd=False).size:
                        mylist += [[i, j]]
        return mylist

    # stupid AI
    def stupidAI(self):
        # choose the best
        mylist = []
        myscore = []
        for i in range(page_play.rows):
            for j in range(page_play.cols):
                if self.cb[i][j] == CB.EMPTY:
                    p_cb = self.updotherchess(
                        self.cb, (i, j), self.aiturn, upd=False)
                    if p_cb.size:
                        mylist += [[i, j]]
                        a, b = self.calc_score(p_cb)
                        p_score = a if self.aiturn == CB.BLACK else b
                        myscore += [p_score]

        # not rand.......... the first max
        print('stupidAI: i wanna ', mylist[myscore.index(max(myscore))])
        self.win.update()
        self.win.after(500)
        self.updchess(mylist[myscore.index(max(myscore))])


if __name__ == '__main__':
    checkerboard()
