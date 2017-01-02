import gym
import random
import pybrain
import examples.agents.geometric_median as gm
import numpy as np
from scipy.spatial.distance import cdist, euclidean

from pybrain.datasets import ClassificationDataSet
import array
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

# import pylab
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal

from gym import wrappers


class RGB:
    red = int(0)
    green = int(0)
    blue = int(0)

    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other):
        if not isinstance(other, RGB):
            return False

        return int(self.red) == int(other.red) and int(self.green) == int(other.green) and int(self.blue) == int(
            other.blue)

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __str__(self):
        return str(self.red) + ":" + str(self.green) + ":" + str(self.blue)


class Coordinates:
    X = int(0)
    Y = int(0)

    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y

    def __str__(self):
        r = "{:.4f} :: {:.4f}".format(self.X, self.Y)
        return r

    def __eq__(self, other):
        if not isinstance(other, Coordinates):
            return False

        return int(self.X) == int(other.X) and int(self.Y) == int(other.Y)

    def __hash__(self):
        return hash((self.X, self.Y))


class Agents:
    network = pybrain.FeedForwardNetwork()
    color = RGB
    set_array = dict()

    white = RGB(236, 236, 236)
    black = RGB(0, 0, 0)

    flag_blue = RGB(66, 72, 200)

    flag_red = RGB(200, 72, 66)

    dirties = {RGB(192, 192, 192), RGB(214, 214, 214)}
    trees = {RGB(82, 126, 45), RGB(110, 156, 66), RGB(158, 208, 101)}

    avg_flag = set({})
    pos_flag = Coordinates()

    avg_tree = set({})
    pos_tree = Coordinates()

    avg_dirt = set({})
    pos_dirt = Coordinates()

    skier = RGB(214, 92, 92)
    avg_skier = np.ndarray(shape=tuple(()))
    pos_skier = Coordinates()

    angle = 270

    def __init__(self):
        return

    def make_color(self, colors):
        if colors.size != 3:
            return RGB

        return RGB(colors[0], colors[1], colors[2])

    def is_white_line(self, line):
        for j in line:
            color = RGB(j)

            if not color.__eq__(self.white):
                return False

        return True

    def skier_calc(self, pixel, x, y):

        color = self.make_color(pixel)

        if color.__eq__(self.skier):
            self.avg_skier.add([x, y])

    def skier_visible(self, pixel, x, y):

        # if x == 90:
        color = self.make_color(pixel)

        if color.__eq__(self.flag_blue) or color.__eq__(self.flag_red):
            self.avg_flag.add((x, y))

        if color in self.trees:
            self.avg_tree.add(Coordinates(x, y))

        if color in self.dirties:
            self.avg_dirt.add(Coordinates(x, y))

    def calc_avg_coordinates(self, avgs):
        ar = np.ndarray(shape=tuple((avgs.__len__(), 2)), dtype='int')
        for p in avgs:
            a2 = np.ndarray(shape=tuple(2))
            a2.__add__(p)
            ar.__add__(a2)

        point = gm.geometric_median(ar, method='weiszfeld')
        return point
        # avg_X = 0
        # avg_Y = 0
        # for c in avgs:
        #     avg_X *= c.X
        #     avg_Y *= c.Y
        #
        # if avgs.__len__() > 0:
        #     avg_X ^= 1 / avgs.__len__()
        #     avg_Y ^= 1 / avgs.__len__()

        # return Coordinates(avg_X, avg_Y)

    def skier_position(self):
        self.pos_skier = self.calc_avg_coordinates(avgs=self.avg_skier)

    def trees_position(self):
        self.pos_tree = self.calc_avg_coordinates(avgs=self.avg_tree)

    def flag_position(self):
        self.pos_flag = self.calc_avg_coordinates(avgs=self.avg_flag)

    def dirt_position(self):
        self.pos_dirt = self.calc_avg_coordinates(avgs=self.avg_dirt)

    # def act(self, observation):
    #
    #     self.set_array = dict()
    #
    #     y = 0
    #     for line in observation:
    #         x = 0
    #         for pixel in line:
    #
    #             color = self.make_color(pixel)
    #
    #             if color.__eq__(self.white) or color.__eq__(self.black):
    #                 x += 1
    #                 continue
    #
    #             if 40 < y < 90:
    #                 self.skier_calc(pixel, x, y)
    #
    #             if 120 < y < 180:
    #                 self.skier_visible(pixel, x, y)
    #
    #             x += 1
    #         y += 1
    #
    #     self.skier_position()
    #
    #     # self.trees_position()
    #     # self.dirt_position()
    #     # self.flag_position()
    #
    #     return self.compare(skier=self.pos_skier[0], flag=self.pos_flag[0])



    def compare(self, skier, flag):
        if flag == 0:
            return 0

        res = flag - skier
        alfa = 0.1

        if res > 0:
            if abs(res) > alfa * skier:
                return 1
        elif res < 0:
            if abs(res) > alfa * skier:
                return 2

        return 0


if __name__ == '__main__':

    env = gym.make('Skiing-v0')
    out = '/tmp/skiing'
    # env = wrappers.Monitor(env, out)

    # ag = agents()
    action = 0

    for i in range(20):
        observation = env.reset()
        ag = Agents()

        for t in range(1500):
            env.render()
            # print(observation)
            action = ag.act(observation)
            # action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

            print("P ", str(ag.pos_skier), " :: F ", str(ag.pos_flag), " :: T ", str(ag.pos_tree), " :: D ",
                  str(ag.pos_dirt))

            print("\n========================================\n")
            if done:
                print(reward)
                print('Episode finished after {} timesteps'.format(t + 1))
                break
