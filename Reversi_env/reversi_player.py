import random


class CB:
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class StupidAI:
    """
    A simaple of AI.
    StupidAI(api, turn)
    you can use:
        api.get_cb()
        api.get_score(self, cb=None)
    you must implementation function:
        round_callback()
        gameover_callback()
    Have fun
    OHHHHHHHHHHHHHHH
    """
    nickname = 'StupidAI'

    def __init__(self, api, turn):
        self.api = api
        self.turn = turn
        cb = self.api.get_cb()
        self.rows, self.cols = len(cb), len(cb[0])

    def round_callback(self):
        pos_list, _, score_list = self.api.get_hint()

        # random choice from pos_list base on p_score
        p_score = [s[CB.BLACK-1] for s in score_list]
        pos = random.choices(pos_list, p_score)[0]

        # # random choice the best
        # loc = [i for i in range(len(score_list)) if score_list[i] == max(score_list)]
        # pos = pos_list[random.choice(loc)]

        # # choice the first best one
        # p_score = [s[CB.BLACK-1] for s in score_list]
        # pos = pos_list[p_score.index(max(p_score))]

        return pos

    def gameover_callback(self):
        pass


class SmartHuman:
    nickname = 'SmartHuman'

    def __init__(self, api, turn):
        self.api = api

    def round_callback(self):
        if self.api.nickname == 'Reversi':
            pos_list, _, _ = self.api.get_hint()
            self.api.print_cb()
            print('Hint: ', pos_list)
            intput_str = input()
            while True:
                try:
                    pos = tuple(map(int, intput_str.split(' ')))
                    if pos in pos_list:
                        return pos
                    else:
                        raise ValueError
                except ValueError:
                    print('ValueError')
                    intput_str = input()
        elif self.api.nickname == 'ReversiGUI':
            return self.api.mpos

    def gameover_callback(self):
        pass
