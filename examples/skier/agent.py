import examples.agents.geometric_median as gm
import numpy as np
from examples.skier.RGB import RGB


class agents:
    white = RGB(236, 236, 236)
    black = RGB(0, 0, 0)

    flag_blue = RGB(66, 72, 200)

    flag_red = RGB(184, 50, 50)

    dirties = {RGB(192, 192, 192), RGB(214, 214, 214)}

    trees = {RGB(82, 126, 45), RGB(110, 156, 66), RGB(158, 208, 101)}

    skier = RGB(214, 92, 92)

    avg_skier = []
    avg_flag = []

    pos_skier = [0, 0]
    pos_dirties = [0, 0]
    pos_flags = [0, 0]
    pos_trees = [0, 0]

    angle = 270
    angle_turn = 1

    last_length = 0
    last_delta = 0

    velocity = 1
    current_velocity = 0

    def __init__(self):
        return

    def make_color(self, colors):
        if colors.size != 3:
            return RGB

        return RGB(colors[0], colors[1], colors[2])

    def calc_avg_coordinates(self, avgs):
        ar = np.ndarray(shape=tuple((avgs.__len__(), 2)), dtype='int')
        for p in avgs:
            a2 = np.ndarray(shape=tuple(2))
            a2.__add__(p)
            ar.__add__(a2)

        point = gm.geometric_median(ar, method='weiszfeld')
        return point

    def act(self, observation):
        y = 0
        for line in observation:
            x = 0

            for pixel in line:

                color = RGB(pixel[0], pixel[1], pixel[2])

                if color.__eq__(self.white) or color.__eq__(self.black):
                    x += 1
                    continue

                if y < 90:
                    self.get_skier(pixel, x, y)

                if y < 221:
                    self.get_flag(pixel, x, y)
                x += 1

            y += 1

        self.calc_pos_skier()
        self.calc_pos_flag()

        return self.compare(self.pos_skier, self.pos_flags)

    def compare(self, skier, flag):
        if flag[0] == 0:
            return 0

        delta = flag[0] - skier[0]
        length = pow((pow(flag[0] - skier[0], 2) + pow(flag[1] - skier[1], 2)), 1 / 2)

        alfa = 0.13
        if (1 - alfa) * skier[0] < flag[0] < (1 + alfa) * skier[0]:
            self.save(delta, length)
            print("between flag")
            return self.alignment()

        if (self.last_length - length) < self.velocity:
            self.save(delta, length)
            print("velocity")
            return self.alignment()

        if abs(self.last_delta) > abs(delta):
            self.save(delta, length)
            print("need not turning")
            return 0

        if delta > 0:
            self.save(delta, length)
            print("left turn")
            return self.left_turn()
        else:
            self.save(delta, length)
            print("right turn")
            return self.right_turn()

    def save(self, delta, length):
        self.current_velocity = self.last_length - length
        self.last_delta = delta
        self.last_length = length

    def left_turn(self):
        if self.angle < 259:
            return self.alignment()

        self.angle -= self.angle_turn
        return 1

    def right_turn(self):
        if self.angle > 281:
            return self.alignment()

        self.angle += self.angle_turn
        return 2

    def alignment(self):
        center = 270
        #TODO проверка на равенство преращения
        if self.angle == center:
            return 0

        if self.angle < center:
            return self.right_turn()
        # if self.angle > center:
        else:
            return self.left_turn()
        # return 0

    def get_skier(self, pixel, x, y):

        color = self.make_color(pixel)

        if color.__eq__(self.skier):
            self.avg_skier.append([x, y])

    def calc_pos_skier(self):
        self.pos_skier = self.calc_pos(self.avg_skier)
        self.avg_skier = []
        return self.pos_skier

    def get_flag(self, pixel, x, y):
        color = self.make_color(pixel)

        if color.__eq__(self.flag_blue) or color.__eq__(self.flag_red):
            if self.avg_flag.__len__() > 0:
                if (self.avg_flag[self.avg_flag.__len__() - 1][1] - y) < 3:
                    self.avg_flag.append([x, y])
            else:
                self.avg_flag.append([x, y])

    def calc_pos_flag(self):
        self.pos_flags = self.calc_pos(self.avg_flag)
        self.avg_flag = []

        return self.pos_flags

    def calc_pos(self, avg_array):
        array = np.array(avg_array)

        if array.shape.__len__() > 1:
            pos = gm.geometric_median(array, method='weiszfeld')
            return pos

        return [0, 0]
