import examples.agents.geometric_median as gm
import numpy as np
from examples.skier.RGB import RGB


class agents:
    white = RGB(236, 236, 236)
    black = RGB(0, 0, 0)

    flag_blue = RGB(66, 72, 200)

    flag_red = RGB(200, 72, 66)

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

    last_length = 0
    last_delta = 0

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

                if y < 180:
                    self.get_flag(pixel, x, y)
                x += 1

            y += 1

        self.calc_pos_skier()
        self.calc_pos_flag()

        return self.compare(self.pos_skier, self.pos_flags)

    def compare(self, skier, flag):
        alfa = 0.15
        gamma = 5
        left = 250
        right = 290
        center = 270

        if flag[0] == 0:
            return 0

        delta = flag[0] - skier[0]
        length = pow((pow(flag[0] - skier[0], 2) + pow(flag[1] - skier[1], 2)), 1 / 2)

        if self.last_delta > delta:
            self.last_delta = delta
            self.last_length = length
            return 0

        if (1 - alfa) * skier[0] < flag[0] < (1 + alfa) * skier[0]:
            self.last_delta = delta
            self.last_length = length

            if self.angle == center:
                return 0

            if self.angle < center:
                self.angle += gamma
                return 2
            if self.angle > center:
                self.angle -= gamma
                return 1

            return 0

        if left < self.angle < right:
            if delta > 0:
                self.last_delta = delta
                self.last_length = length
                self.angle -= gamma
                return 1
            else:
                self.last_delta = delta
                self.last_length = length
                self.angle += gamma
                return 2
        else:
            return 0

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
